**[English](../en/troubleshooting.md)** | [概要に戻る](overview.md)

# トラブルシューティング

失敗時はレスポンスに `ErrorCode` と `ErrorMessage` が含まれます。本ページではこれらのコードと対処方法、よくある環境的問題をまとめます。

---

## エラーコード一覧

| ErrorCode | 意味 | 主な対処 |
|---|---|---|
| `CommandNotFound` | 完全修飾コマンド名が未登録 | `uaip_list_commands(ProviderPrefix="UAIP.Core")` で名前確認。**†** マークのコマンドはオプションプラグインが必要 |
| `CapabilityNotAvailable` | セッションに必要 Capability がない | `ErrorMessage` から不足 Capability 名を読み、`Config/DefaultUAIP.ini` の `[UAIP.SafetyPolicy] +AllowedCapabilities=<名前>` に追加。エディタ再起動か `UAIP.Core.ReloadCapabilities` を呼び出す |
| `PolicyViolation` | SafetyPolicy ゲートによる拒否 | `"is denied by SafetyPolicy"` → ini フラグが OFF；`"is not enabled"` → CLI opt-in（`-uaip-enable-scenario`、`-uaip-http-enable` 等）が起動時に未指定 |
| `InvalidParams` | パラメータの誤り / 不足 | `uaip_describe_command(CommandName="...")` でスキーマを再確認 |
| `NotFound` | 対象アセット / アクター / オブジェクトが存在しない | パスや名前を確認、`SearchAssets` や `ListLevelActors` で確認 |
| `ExecutionFailed` | コマンド内部での Runtime 失敗 | `ErrorMessage` を確認。シナリオでは step に `RetryCount` を設定 |
| `NotAllowed` | 禁止パス（`/Engine/`）または禁止タイミング（PIE 中の Editor 編集） | 別のパス、または PIE 停止後に再試行 |
| `Timeout` | 壁時計上限を超過 | シナリオ step の `TimeoutSeconds` を増やすかシナリオを分割 |
| `TooManyRequests` | 並行性制限（シナリオは同時に 1 つ） | 先行 submit の完了を待つ |
| `InternalError` | プロセス障害レベル | まず `UAIP.Workspace.RestartEditor` を試す。継続するなら `Saved/Crashes/` のクラッシュログを添えて Issue 起票 |

---

## よくあるケース

### 「コマンドを呼んだのにエディタが起動しない」

MCP Bridge は初回呼び出し時にエディタを立ち上げます。立ち上がらない場合：

1. Bridge の設定を確認: `Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json` — `editor_path` と `uproject_path` が絶対パスで正しいか
2. 同じ `uproject` を手動でエディタを起動して開けるか確認。開けないなら UE 側の問題で UAIP の問題ではない
3. Python が PATH に通っており、`python --version` が 3.10+ を返すか確認
4. "Editor restart limit exceeded" と出たら、60 秒に 3 回までの再起動ガードに引っかかっている。60 秒待って再試行

### 「初回呼び出しはタイムアウトするが、それ以降は動く」

初回エディタ起動は 30〜90 秒かかります（シェーダー再コンパイル、プラグインロード）。デフォルトの MCP タイムアウトは初回に余裕を持たせていますが、非常に重いプロジェクトでは超過することもあります。最初の AI 呼び出し前にエディタを手動起動して暖機するか、Bridge はタイムアウト後もエディタを生かしているので再試行してください。

### 「スクリーンショットが真っ黒」

主な原因：
- キャプチャ対象ウィンドウがフォーカスされていない → タブベースのキャプチャでは先に `FocusEditorTab` を実行
- エディタが `-nullrhi` / `-RenderOffscreen` で起動された → キャプチャコマンドは実 RHI が必要
- PIE キャプチャ（`CaptureViewportImage`）で実際には PIE が動いていない → `DumpEditorState` で確認

### 「アセット編集を依頼したが `PolicyViolation: Capability '...' is denied by SafetyPolicy`」

その Capability が `[UAIP.SafetyPolicy] DeniedCapabilities=...` にあり、`AllowedCapabilities` よりも deny-wins で優先されています。`DeniedCapabilities` から削除してエディタを再起動してください。

### 「シナリオが常に `PolicyViolation: Scenario execution is not enabled in this environment` で拒否される」

シナリオルートは **安全のためデフォルト無効** です。`-uaip-enable-scenario` を付けてエディタを再起動するか、MCP Bridge 経由なら `Scripts/MCPBridge/config.json` に `"enable_scenario": true` を追加して Bridge を再起動してください。

### 「キャプチャ / ダンプが理由不明の `ExecutionFailed` で返る」

`Saved/UAIP/<session>/Logs/` 内のそのコマンドの最新ログ行を確認すると、UE 側の正確な失敗理由が記録されています。よくある原因：

- デモ版キャプチャ: 透かし合成失敗（フォントキャッシュ破損、`Saved/UAIP/` 書き込み不可）— フェイルクローズします
- Slate ツリーダンプ: root widget path フィルタが何にもマッチしなかった → `RootWidgetPath` なしで試す
- 非同期ロード中のワールドダンプ: ワールドが未準備 → シナリオフロー内で `LoadMap` 完了を待つ

### 「AI の編集が本当にファイルに反映されたのか分からない」

UAIP の編集は `MarkPackageDirty`（または同等）を呼びますが、ディスク上のファイルが変わるのは保存時です。対処：

- シナリオの最後に `UAIP.Editor.Workspace.SaveAllPackages` ステップを追加
- 操作後に `git status` で確認（プロジェクトがバージョン管理下にある場合）
- `DumpEditorState` を使用 — `OpenAssets` フィールドに Dirty フラグが含まれる

### 「Live Coding リビルドがブロックされる」

Live Coding がビルド中でエディタが他のコマンドを受け付けない場合、AI に先に `UAIP.Workspace.GetLiveCodingStatus` を呼ばせて、ビルド進行中なら待たせます。Live Coding ビルド中に他の操作を強制すると未定義動作になります。フルリビルドのためにシャットダウンする場合は `taskkill` ではなく `UAIP.Workspace.ShutdownEditor` を使ってください — `taskkill` だと `mcp_proxy.lock` が残り、次回セッションが MCP 切断します。

### 「ドキュメントに載っているコマンドが `CommandNotFound` になる」

考えられる原因：
- そのコマンドのオプションプラグインが `.uproject` で未有効（[コマンドリファレンス](commands.md) の **†** マーク参照）
- デモ版で Pro 版限定のコマンドを呼んでいる（🆓 マークなし）
- Toolset ブリッジコマンド（例: `Toolset.Editor.UMG.GetWidgets`）は UE 5.8+ と対応 Toolset プラグインが必要

`uaip_describe_command(CommandName="...")` で確認 — `Available: false` だと前提条件が欠けていることが分かります。

### 「MCP が固まっている — エディタを kill すべき？」

**`taskkill` で kill するのは避けてください。** 同一ホストの UE エディタ全インスタンス（他プロジェクト含む）が落ち、`mcp_proxy.lock` が残ります。正しい順序：

1. まず `uaip_execute(CommandName="UAIP.Workspace.RestartEditor")` を試す — Bridge がきれいに再起動を処理
2. MCP 自体が応答しないなら Bridge プロセスだけを再起動（エディタは生かしたまま）
3. 最終手段として、AI クライアントを閉じてから対象エディタの PID を狙って `Stop-Process`

---

## パフォーマンス・リソース

### 「Artifact がディスクを食いつぶす」

`Saved/UAIP/` は時間とともに肥大化します。手動削除で問題ありません — セッション終了後の artifact は参照されません。セッション単位での保持を強制したい場合は `UAIP.Core.EndSession` を明示的に呼んでください。

### 「コマンドを大量に呼ぶとエディタのメモリ使用量が増える」

長時間の AI セッションでは Widget 観測登録・キャッシュされた Slate ツリー等が蓄積する可能性があります。定期的に `UAIP.Core.EndSession` を呼んで artifact を GC し Widget 参照を解放しましょう。大きなタスク毎に新しい `SessionId` を発行するのも有効。

### 「コマンドが遅い」

「遅い」の大半は実際にエディタの処理コストです（シェーダーコンパイル、アセットロード、PIE 起動）。`uaip_describe_command` で確認 — 読み取り専用コマンドは通常 100 ms 未満、キャプチャはフレーム予算依存、PIE 起動は秒オーダーかかります。

---

## それでも解決しない場合

1. 該当する `ErrorCode` + `ErrorMessage` を控える
2. `Saved/UAIP/<session>/Logs/` で該当コマンドのログを確認
3. UE バージョン、プラグインバージョン（`UAIP.Core.GetSystemInfo`）、デモ / Pro を確認
4. 上記情報を添えて [Issue](../../issues) 起票。エディタクラッシュ時は `Saved/Crashes/` のダンプも添付してください
