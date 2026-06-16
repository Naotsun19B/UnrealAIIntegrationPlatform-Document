**[English](../en/architecture.md)** | [概要に戻る](overview.md)

# アーキテクチャ

このページは UAIP の内部構造を解説します。UAIP を使うだけなら [クイックスタート](quickstart.md) と [コマンドリファレンス](commands.md) で十分です。本ページはツールプログラマー・プラグイン拡張者・レビュアー向けです。

---

## 1. レイヤー構成

```mermaid
flowchart TB
    subgraph Clients["外部クライアント"]
        AI["AI クライアント<br/>(Claude Code, Cursor, …)"]
        Tool["カスタムツール / CI"]
    end

    subgraph TransportLayer["Transport レイヤー"]
        MCP["MCP Bridge<br/>(thin_proxy.py)"]
        HTTP["HTTP transport<br/>:8765 / :8767"]
        WS["WebSocket transport<br/>:8766 / :8768"]
        CLI["CLI transport<br/>-uaip-request / -uaip-stdin-stream"]
    end

    subgraph CoreLayer["Core レイヤー (UAIPCore)"]
        Auth["Auth + Session"]
        Dispatcher["CommandDispatcher"]
        Policy["FSafetyPolicy<br/>+ FCapabilitySet"]
        Registry["CommandRegistry"]
        Artifacts["ArtifactManager"]
    end

    subgraph Domains["Domain レイヤー"]
        EditorDom["UAIPEditor*<br/>(Workspace, Observation,<br/>Assets, Blueprint, …)"]
        RuntimeDom["UAIPRuntime*<br/>(PIE, Observation,<br/>Input, GAS, …)"]
        Scenario["UAIPScenario"]
    end

    subgraph UE["Unreal Engine"]
        EngineEd["UnrealEd / Slate /<br/>AssetTools / Sequencer / …"]
        EngineRt["UWorld / GameInstance /<br/>Subsystem / Input / …"]
    end

    AI --> MCP
    Tool --> HTTP
    Tool --> CLI
    Tool --> WS
    MCP --> HTTP
    HTTP --> Auth
    WS --> Auth
    CLI --> Auth
    Auth --> Dispatcher
    Dispatcher --> Policy
    Policy --> Registry
    Registry --> EditorDom
    Registry --> RuntimeDom
    Registry --> Scenario
    EditorDom --> EngineEd
    RuntimeDom --> EngineRt
    EditorDom --> Artifacts
    RuntimeDom --> Artifacts
    Scenario --> Dispatcher
```

絶対ルール：**依存は下位方向のみ**。Transport レイヤーは Domain ハンドラをインポートしないし、Domain ハンドラは Transport をインポートしない。Core が中央。

---

## 2. モジュールマップ

| レイヤー | モジュール | 役割 |
|---|---|---|
| **Core** | `UAIPCore` | セッション・Capability・Policy・コマンドレジストリ・Artifact マネージャ。全構成でロード |
| **Shared** | `UAIPEditorShared`, `UAIPRuntimeShared`, `UAIPExecutionShared`, `UAIPArtifacts`, `UAIPBuildSupport`, `UAIPWatchdogSupport` | ドメイン横断のユーティリティ — コマンドは直接持たない |
| **Transports** | `UAIPTransportHTTP`, `UAIPTransportWS`, `UAIPTransportCLI` | 各 transport リスナー（MCP はエディタ外部の Python Bridge） |
| **Editor ドメイン** | `UAIPEditor*`（Workspace, Observation, Execution, UIAutomation, Assets, Level, Property, Blueprint, UMG, Material, GameplayTags, GameFeatures, Niagara, Physics, Dataflow, Skeleton, DataTable, AnimBlueprint, SoundCue, BehaviorTree, MetaSound, EQS, Sequencer, StateTree, Curve, PCG, WorldConditions, Conversation, ControlRig, EnhancedInput, GAS, PythonExtension） | エディタ側意味的コマンド。`EditorNoCommandlet` フェーズでロード |
| **Runtime ドメイン** | `UAIPRuntimePIE`, `UAIPRuntimeObservation`, `UAIPRuntimeExecution`, `UAIPRuntimeAssertion`, `UAIPRuntimeWorld`, `UAIPRuntimeGAS`, `UAIPRuntimeInput`, `UAIPRuntimeNiagara` | Runtime / PIE 側コマンド。一部は Gauntlet 用にパッケージビルドへ opt-in 可能 |
| **Scenario** | `UAIPScenario` | シナリオルート — `uaip_execute` と独立だが `CommandDispatcher` を再利用 |

登録済みコマンドの完全な数は [コマンドリファレンス](commands.md) を参照。

---

## 3. 依存方向

```mermaid
flowchart LR
    A[Transport] -.->|"CommandRequest 送信"| B[Core]
    B -->|"ディスパッチ"| C[Domain handler]
    C -->|"使用"| D[UE Engine API]
    C -.->|"書き込み"| E[ArtifactManager]
    E -.->|"id / path"| B
    B -.->|"CommandResponse"| A
```

- Transport は Domain を直接呼ばない
- Domain は他の Domain をインポートしない（例: `UAIPEditorBlueprint` は `UAIPEditorMaterial` に依存しない）
- ドメイン横断の共通処理は `UAIPEditorShared` / `UAIPRuntimeShared` 経由
- `UAIPScenario` は `uaip_execute` と並列のルート。各 step は Domain を直接叩かず `CommandDispatcher` 経由で再送

循環依存は禁止。UE の `.Build.cs` システムが強制するため、循環を作るとコンパイルが通らない。

---

## 4. コマンドディスパッチシーケンス

```mermaid
sequenceDiagram
    autonumber
    participant Cli as AI クライアント
    participant Br as MCP Bridge<br/>(or HTTP/WS/CLI)
    participant Tr as Transport
    participant Au as Auth + Session
    participant Di as CommandDispatcher
    participant Po as Capability + SafetyPolicy
    participant Re as Registry
    participant Hd as Domain handler
    participant Ar as ArtifactManager

    Cli->>Br: uaip_execute(...)
    Br->>Tr: POST /uaip/commands
    Tr->>Au: トークン検証、SessionId 確認
    Au-->>Tr: ok（Session ロード済み）
    Tr->>Di: DispatchAsync(request)
    Di->>Po: IsCommandAllowed(name, session)
    alt 拒否
        Po-->>Di: CapabilityNotAvailable / PolicyViolation
        Di-->>Tr: エラーレスポンス
        Tr-->>Cli: ErrorCode + ErrorMessage
    else 許可
        Di->>Re: ResolveHandler(name)
        Re-->>Di: handler
        Di->>Hd: Execute(params)
        Hd->>Ar: WriteArtifact(...)
        Ar-->>Hd: ArtifactId
        Hd-->>Di: CommandResponse(Data, Artifacts)
        Di-->>Tr: CommandResponse
        Tr-->>Cli: Success + Data + Artifacts
    end
```

**デフォルトはすべてゲームスレッド実行**。長時間処理が必要なハンドラは自身を非同期マークし、完了時にゲームスレッドへポストバックしてからコールバックを呼ぶ。

---

## 5. 認可決定フロー

```mermaid
flowchart TB
    Start([CommandRequest 受信])
    A{コマンドが<br/>SafetyPolicy.DeniedCommands に含まれる?}
    B{セッションに必要 Capability が<br/>含まれる?}
    C{必要 Capability が<br/>DeniedCapabilities に含まれる?}
    D{必要 SafetyPolicy<br/>フラグが有効?}
    E([実行])
    F1([PolicyViolation:<br/>コマンドブロック])
    F2([CapabilityNotAvailable])
    F3([PolicyViolation:<br/>Capability 拒否])
    F4([PolicyViolation:<br/>ポリシーフラグ OFF])

    Start --> A
    A -- はい --> F1
    A -- いいえ --> B
    B -- いいえ --> F2
    B -- はい --> C
    C -- はい --> F3
    C -- いいえ --> D
    D -- いいえ --> F4
    D -- はい --> E
```

ゲート 2 種類（Capability と SafetyPolicy）、結果コード 3 種類（`CapabilityNotAvailable`・`PolicyViolation`・`Success`）。`ErrorMessage` には常に該当する Capability 名やフラグ名が含まれ、AI / ユーザーが推測なく対処できます。詳細は [Safety & Capabilities](safety.md)。

---

## 6. セッションライフサイクル

```mermaid
stateDiagram-v2
    [*] --> Spawning: クライアントが新規 SessionId で<br/>最初のリクエスト送信
    Spawning --> Active: Session レコード作成
    Active --> Active: 後続コマンドが<br/>セッション状態を共有
    Active --> GC: EndSession または TTL 切れ
    GC --> [*]: artifact が GC 対象に
```

セッションは以下を所有する単位：
- Capability セット（spawn 時に SafetyPolicy から決定）
- Widget 観測キャッシュ（`ObserveWidget` 用）
- Artifact サブフォルダ（`Saved/UAIP/<SessionId>/`）
- セッション単位レートリミタ（例：シナリオ submit）

匿名セッション（`SessionId` 未指定）は自動生成 `MCP-Anonymous-<guid>` ID — 単発呼び出しには便利ですが、タスク単位でセッションを分けると artifact 検索が容易。

---

## 7. Artifact ライフサイクル

出力を生成するコマンド（キャプチャ・ダンプ・ログ・レポート）はすべて、1 つ以上の **artifact** を `Saved/UAIP/<SessionId>/` に書き出し、レスポンスに artifact ID を返します。クライアントは ID 経由で内容を取得 — ファイルパスはレスポンスペイロードに含めません。これにより path leak 攻撃を防ぎ、transport 間で契約を一貫させます。

詳細は [Artifacts](artifacts.md) を参照（ディスクレイアウト・インライン vs フェッチの挙動・型ごとのポリシー）。

---

## 8. エディタライフサイクル（Bridge が管理）

```mermaid
sequenceDiagram
    participant Cli as AI クライアント
    participant Br as MCP Bridge
    participant Ed as UE Editor

    Cli->>Br: 最初の uaip_execute(...)
    alt エディタ未起動
        Br->>Ed: 起動（-uaip-stdin-stream 付き）
        Br->>Br: __UAIP_STREAM_READY__ を待機
    end
    Br->>Ed: stdio 経由でリクエスト転送
    Ed-->>Br: レスポンス
    Br-->>Cli: レスポンス

    Note over Br,Ed: Bridge は呼び出し間でエディタを生存維持

    alt エディタクラッシュ / ハング
        Br->>Br: 検出（crashmarker / 接続断 / 30秒無応答）
        Br->>Ed: 再起動（60秒に最大3回）
    end
```

Bridge がエディタプロセスのライフサイクルを所有するため、クライアントは管理不要。AI クライアントは **`taskkill` / `Stop-Process` を使ってはいけません** — 他プロジェクトのエディタも巻き込みで落ちます。代わりに `UAIP.Workspace.RestartEditor` を使用してください。詳細は [トラブルシューティング → MCP が固まっている](troubleshooting.md#mcp-が固まっている--エディタを-kill-すべき)。

---

## 9. 拡張ポイント

UAIP はフォークせずにプロジェクト独自のコマンドを追加できる小さな拡張フックを公開しています：

- **`ICommandProvider`** — モジュール起動時に実装・登録することで、独自ハンドラ付きの新規コマンドグループを追加
- **`ICaptureProvider`** — 外部のグラフ画像ソース（GraphPrinter など）をブリッジし、`CaptureCanonicalGraphImage` から利用可能に
- **`IToolsetCommandHandler`** — Toolset フレームワークコマンドを UAIP のリクエスト / レスポンス形式に適応（製品版、UE 5.8+）
- **Python `@uaip_command`** — Python 関数を UAIP コマンドとして登録（`PythonScriptPlugin` + `PythonExtensionReload` Capability が必要）

プロジェクト固有の拡張は **別プラグイン / 別モジュール** に置くこと（UAIP のソースツリーに入れない）。UAIP アップデート時の `git pull` をクリーンに保つためです。

---

## 10. 次に読む

| 目的 | 移動先 |
|---|---|
| 新規コマンドを実装したい | [コマンドリファレンス](commands.md)（命名規則）+ 該当 `UAIPEditor*` モジュールの既存ハンドラソース |
| 認可機構を深く理解したい | [Safety & Capabilities](safety.md)、[セキュリティ](security.md) |
| シナリオ内部を理解したい | [シナリオ実行](scenario.md) |
| Artifact のストレージ / 取得を理解したい | [Artifacts](artifacts.md) |
| 用語を調べたい | [用語集](glossary.md) |
