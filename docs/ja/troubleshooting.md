**[English](../en/troubleshooting.md)** | [概要に戻る](overview.md)

# トラブルシューティング

UAIP のコマンドが失敗すると、レスポンスに `ErrorCode` と `ErrorMessage` が含まれます。本ページではエラーコードごとの対処方法と、環境周りでよく遭遇する問題への対処をまとめています。

> 本ページで参照する記号の意味：**🆓** = デモバイナリで利用可能 / **🧩** = オプションプラグイン必須（[コマンドリファレンス](commands.md#凡例) と同じ凡例）。

---

## エラーコード一覧

| ErrorCode | 何が起きているか | 主な対処 |
|---|---|---|
| `CommandNotFound` | 完全修飾コマンド名が登録されていない | `uaip_list_commands(ProviderPrefix="UAIP.Core")` で正しい名前を確認してください。🧩 マーク付きのコマンドはオプションプラグインの有効化が必要です |
| `CapabilityNotAvailable` | セッションに必要な Capability がない | `ErrorMessage` に不足している Capability 名が含まれます。`Config/DefaultUAIP.ini` の `[UAIP.SafetyPolicy] +AllowedCapabilities=<名前>` に追加し、エディタを再起動するか `UAIP.Core.ReloadCapabilities` を呼び出してください |
| `PolicyViolation` | SafetyPolicy ゲートで拒否された | `"is denied by SafetyPolicy"` の場合は ini フラグがオフ、`"is not enabled"` の場合は CLI の opt-in フラグ（`-uaip-enable-scenario`・`-uaip-http-enable` など）が起動時に指定されていません |
| `InvalidParams` | パラメータの誤りや欠落 | `uaip_describe_command(CommandName="...")` でスキーマを再確認してください |
| `NotFound` | 対象のアセット・アクター・オブジェクトが存在しない | パスや名前を確認し、`SearchAssets` や `ListLevelActors` で実在を確かめてください |
| `ExecutionFailed` | コマンド内部の Runtime 処理で失敗 | `ErrorMessage` の詳細を確認してください。シナリオの中で起きた場合は該当ステップに `RetryCount` を設定するのが有効です |
| `NotAllowed` | 禁止パス（`/Engine/` など）や禁止タイミング（PIE 中の Editor 編集） | 別のパスを選ぶか、PIE を停止してから再試行してください |
| `Timeout` | 壁時計の上限を超えた | シナリオステップの `TimeoutSeconds` を増やすか、シナリオ自体を分割してください |
| `TooManyRequests` | 並行性制限に達した（シナリオは同時 1 つまで） | 先行する送信の完了を待ってください |
| `InternalError` | プロセス障害レベルの問題 | まずは `UAIP.Editor.Workspace.RestartEditor` を試してください。それでも続く場合は `Saved/Crashes/` のクラッシュログを添えて Issue を起票してください |

---

## よくあるケース

### コマンドを呼んでもエディタが起動しない

MCP Bridge は最初の呼び出しでエディタを立ち上げます。立ち上がらない場合は以下を確認してください：

1. Bridge の設定を確認する：`Plugins/UAIPMCPBridge/config.json` の `ue_editor_path` と `uproject_path` が絶対パスで正しく設定されているか。一般的には MCP クライアントの `env` ブロック（`UAIP_UE_EDITOR_PATH` / `UAIP_UPROJECT_PATH`）が優先されるのでそちらも確認
2. 同じ `uproject` を手動でエディタから開けるか確認する：開けない場合は UE 側の問題で、UAIP の問題ではありません
3. Python が `PATH` に通っているか、`python --version` が 3.10 以上を返すかを確認する
4. `"Editor restart limit exceeded"` と出る場合は、60 秒に 3 回までの再起動ガードに引っかかっています。60 秒待ってから再試行してください

### 初回呼び出しはタイムアウトするが、それ以降は動く

初回のエディタ起動には 30〜90 秒かかります（シェーダーの再コンパイルとプラグインのロードのため）。デフォルトの MCP タイムアウトは初回向けに余裕を持たせていますが、非常に重いプロジェクトでは超過することがあります。最初の AI 呼び出し前にエディタを手動で起動して暖機しておくか、Bridge はタイムアウト後もエディタを生かしたままなので、もう一度同じコマンドを呼んでみてください。

### スクリーンショットが真っ黒になる

主な原因は次の 3 つです：

- キャプチャ対象のウィンドウがフォーカスされていない → タブベースのキャプチャでは先に `FocusEditorTab` を呼んでください
- エディタが `-nullrhi` / `-RenderOffscreen` で起動されている → キャプチャコマンドは実 RHI が必要です
- PIE キャプチャ（`CaptureViewportImage`）を呼んだが、実際には PIE が動いていない → `DumpEditorState` で確認してください

### アセット編集を依頼したのに `PolicyViolation: Capability '...' is denied by SafetyPolicy` が返る

その Capability が `[UAIP.SafetyPolicy] DeniedCapabilities=...` に含まれており、`AllowedCapabilities` よりも deny-wins で優先されています。`DeniedCapabilities` から削除してエディタを再起動してください。

### シナリオが常に `PolicyViolation: Scenario execution is not enabled in this environment` で拒否される

シナリオルートは **安全のためデフォルトで無効** になっています。`-uaip-enable-scenario` を付けてエディタを再起動するか、MCP Bridge 経由なら `Plugins/UAIPMCPBridge/config.json` に `"enable_scenario": true` を追加して Bridge を再起動してください。

### キャプチャ / ダンプが理由不明の `ExecutionFailed` で返る

`Saved/UAIP/<session>/Logs/` に該当コマンドの最新ログがあり、UE 側の正確な失敗理由が記録されています。よくある原因は次のとおりです：

- デモ版のキャプチャで透かしの合成に失敗（フォントキャッシュ破損、`Saved/UAIP/` への書き込み不可など）→ フェイルクローズします
- Slate ツリーダンプの `RootWidgetPath` フィルタが何にもマッチしていない → `RootWidgetPath` なしで試してください
- 非同期ロード中のワールドダンプ：ワールドがまだ準備できていない → シナリオで `LoadMap` の完了を待ってから実行してください

### AI の編集がファイルに反映されているのか分からない

UAIP の編集は `MarkPackageDirty`（または同等の処理）を呼んでいますが、ディスク上のファイルが実際に変わるのは保存時です。対処は以下のとおりです：

- シナリオの最後に `UAIP.Editor.Workspace.SaveAllPackages` のステップを追加する
- 操作後に `git status` で確認する（バージョン管理下にあるプロジェクトの場合）
- `DumpEditorState` を使う — `OpenAssets` フィールドに Dirty フラグが含まれています

### Live Coding のリビルドがブロックされる

Live Coding がビルド中でエディタが他のコマンドを受け付けないときは、まず AI に `UAIP.Editor.Workspace.GetLiveCodingStatus` を呼ばせて、ビルド中なら待たせるようにしてください。Live Coding のビルド中に他の操作を強引に実行すると未定義の動作になります。フルリビルドのために一度シャットダウンしたい場合は、`taskkill` ではなく `UAIP.Editor.Workspace.ShutdownEditor` を使ってください — `taskkill` だと `mcp_proxy.lock` が残ってしまい、次のセッションで MCP が切断する原因になります。

### ドキュメントに載っているコマンドが `CommandNotFound` になる

考えられる原因は次のとおりです：

- そのコマンドのオプションプラグインが `.uproject` で有効になっていない（[コマンドリファレンス](commands.md) の 🧩 マークを参照）
- デモ版で製品版限定のコマンドを呼んでいる（🆓 マークが付いていないもの）
- Toolset ブリッジコマンド（例：`Toolset.Editor.UMG.GetWidgets`）は UE 5.8+ と対応する Toolset プラグインが必要

`uaip_describe_command(CommandName="...")` で確認すると、`Available: false` だった場合に前提条件が欠けていることが分かります。

### MCP が固まったように見える — エディタを kill するべき？

**`taskkill` は避けてください。** 同一ホストの UE エディタが全インスタンス（他プロジェクト分も含む）落ちてしまい、`mcp_proxy.lock` が残ります。正しい順序は次のとおりです：

1. まず `uaip_execute(CommandName="UAIP.Editor.Workspace.RestartEditor")` を試す — Bridge がきれいに再起動処理を行います
2. MCP 自体が応答しない場合は、Bridge プロセスだけを再起動する（エディタは生かしたままで OK）
3. 最終手段として、AI クライアントを閉じてから対象エディタの PID を狙って `Stop-Process` を呼ぶ

---

## パフォーマンスとリソース

### Artifact がディスクを圧迫する

`Saved/UAIP/` は時間とともに肥大化していきます。手動で削除しても問題ありません — セッション終了後の Artifact は参照されないためです。セッション単位での保持を確実にしたい場合は `UAIP.Core.EndSession` を明示的に呼んでください。

### コマンドを大量に呼ぶとエディタのメモリ使用量が増えていく

AI セッションを長時間続けると、Widget の観測登録やキャッシュされた Slate ツリーが蓄積していくことがあります。定期的に `UAIP.Core.EndSession` を呼んで Artifact を GC し、Widget の参照を解放しましょう。大きなタスクごとに新しい `SessionId` を割り当てるのも有効です。

### コマンドが遅い

「遅い」と感じるケースの大半は、実際にはエディタ自体の処理コストです（シェーダーコンパイル・アセットロード・PIE 起動など）。`uaip_describe_command` で確認できますが、読み取り専用のコマンドは通常 100ms 未満、キャプチャはフレーム予算依存、PIE 起動は秒単位かかります。

---

## それでも解決しない場合

1. 該当する `ErrorCode` と `ErrorMessage` を控える
2. `Saved/UAIP/<session>/Logs/` で該当コマンドのログを確認する
3. UE バージョン・プラグインバージョン（`UAIP.Core.GetSystemInfo`）・デモ版か製品版かを確認する
4. これらの情報を添えて [Issue](../../issues) を起票してください。エディタがクラッシュした場合は `Saved/Crashes/` のダンプも添付してください
