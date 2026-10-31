**[English](../en/uaip-result-view.md)** | [概要に戻る](overview.md)

# Result View — Claude Code の Mod（`uaip-result-view`）

UAIP の MCP ツール呼び出しの行を、トランスクリプト上で描き替える Claude Code の Mod です。Claude Code の
既定の表示は、呼び出しごとに応答 JSON の先頭の数文字だけなので、セッションを見ている人にはどのコマンドを
呼び、どう終わったかが分かりません。この Mod はその行を要約に描き替えます。
**変わるのは描画だけで、モデルが読む結果はブリッジが返したままです。**

Claude Code から [MCP Bridge](connections.md#mcp-bridge) 経由で UAIP を使うセッション向けです。
[Claude Code Plugin](claude-code-plugin.md)（HTTP API を使う `/uaip:*` スキル群）は不要で、その一部でもありません。
両者が共有しているのは marketplace だけです。

---

## 表示

```
UAIP ▸ Execute  UAIP.Editor.Observation.CaptureActiveWindowImage
  ✓ Success
    📎 Image  MCP-…/Captures/CaptureActiveWindowImage-….png
    ▸ Details          ← 押すと Result の主要フィールドを開く（失敗時は最初から開いている）
```

| ツール | 見出し | その下に常に出る行 |
|---|---|---|
| `uaip_execute` | `✓ Success`、または赤字の `✗ <ErrorCode>: <ErrorMessage>` | Artifacts（種類とパス） |
| `uaip_run_scenario` | `✓ Completed (n/n steps)` / `✗ Failed (n/m steps)` | ステップごとの行と Artifact の件数 |
| `uaip_get_editor_status` | `✓ Success · <State>` | `RecommendedAction` |
| その他のブリッジツール | 成否 | Artifacts があれば |

- **Details** は `Result`（ブリッジが直接答えるツールでは `Data`）の各フィールドを `Key: value` で出します。
  入れ子のオブジェクトは 1 段だけ開き、配列は件数だけを出します。最大 16 行です
- 呼び出しの行には、コマンド名（シナリオ名）と引数を `Key=Value` で出します
- 結果を読めなかったときは、テキストの 1 行目をそのまま出します

VS Code 拡張とデスクトップアプリでは、要約を呼び出しの行の中に描きます。ターミナルでは、呼び出しの行は
1 行で、要約はその下の結果の行に描きます。

---

## 動作環境

- **Mod に対応した Claude Code**。Mod の API は Claude Code 側で **EARLY ACCESS** とされており、Claude Code の
  リリースごとに変わりえます。この Mod の版が `0.x` なのはそのためです。Claude Code の更新後に UAIP の行が
  生の JSON に戻ったら、`claude --debug` で起動し、ログの `ui.render (ToolUse)` の行を見てください。描画が
  拒否された理由が書かれています
- **UAIP の MCP Bridge**。インストーラーが Claude Code に登録したもの。Mod が認識するサーバー名は、`uaip`
  そのもの、または `uaip-` か `uaip_` で始まる名前です（大文字小文字は問いません。例: `UAIP_MyProject`）。
  それ以外の名前のサーバーへの呼び出しは通常どおりに表示されます。ブリッジのセットアップは
  [Claude Code](clients/claude-code.md) を参照してください

---

## インストール

この Mod は独自の zip で配布しますが、[Claude Code Plugin](claude-code-plugin.md) と同じ `uaip-tools`
marketplace に属します。2 つの zip は同じ `UAIPClaudeCodePlugin` フォルダに展開され、同じ marketplace の
ファイルを持つので、どちらか一方だけでも両方でもインストールできます。

1. このリポジトリの [Releases](../../../releases)（タグ `ResultView-v<X.Y.Z>`）から
   `UAIP-ResultView-<X.Y.Z>.zip` と `.sha256` ファイルをダウンロードし、検証します（下記
   [ダウンロードの検証](#ダウンロードの検証) 参照）
2. 自分だけが書き込める恒久的なフォルダに展開します。UE プロジェクトのフォルダや Claude Code の作業
   ディレクトリの外にしてください。Claude Code Plugin を使っている場合は、その zip を展開したフォルダに
   展開します
3. `uaip-tools` marketplace をまだ登録していなければ
   `/plugin marketplace add <展開した UAIPClaudeCodePlugin フォルダのパス>` を実行します。
   登録済みなら `/plugin marketplace update uaip-tools` を実行します
4. `/plugin install uaip-result-view@uaip-tools` を実行し、Claude Code を再起動します

どちらの zip を展開しても、marketplace には両方のプラグインが載ります。展開していない方の zip の
プラグインをインストールしようとすると「Source path does not exist」で失敗しますが、他には影響しません。

---

## ダウンロードの検証

各リリースは zip の隣に `.sha256` ファイルを公開します。中身は 2 行です。

```
<sha-256 の 16 進、小文字>  UAIP-ResultView-<version>.zip
commit <リリースのビルド元のコミット>
```

同じ SHA-256 を、独立した第二の情報源としてこのページにも記録します（下記
[リリースのチェックサム](#リリースのチェックサム) 参照）。zip を信頼する前に両方と照合してください。

```powershell
Get-FileHash UAIP-ResultView-<version>.zip -Algorithm SHA256
```

---

## アップデート・ロールバック

1. 展開した `UAIPClaudeCodePlugin` フォルダの中の `plugins/uaip-result-view` フォルダを削除します。
   他は消さないでください。`plugins/uaip` は Claude Code Plugin のものです
2. 目的のバージョンの zip を展開します
3. `/plugin marketplace update uaip-tools` を実行し、続けて `/plugin update uaip-result-view@uaip-tools` を
   実行してから、Claude Code を再起動します

---

## リリースのチェックサム

| バージョン | SHA-256（`UAIP-ResultView-<version>.zip`） |
|---|---|
| 0.1.1 | `959d04947832f386ff486d971218e90908c4aa08de0f7032e9949eb138cb0d3b` |
| 0.1.0 | `8c30b0a40bc525e62bdbabdaf28ac629718fb9622c432ec0b59a9a6ea74cc39b` |

---

## ライセンス

MIT。ライセンス全文はリリースアーカイブ内に `LICENSE` として同梱されています。
