**[English](../../en/clients/codex.md)** | [接続方法に戻る](../connections.md#mcp-bridge)

# OpenAI Codex CLI

[Codex CLI](https://github.com/openai/codex) は OpenAI が提供する公式の AI コーディング CLI です。MCP サーバの登録は `~/.codex/config.toml`（JSON ではなく TOML）で行います。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ユーザー全体 | `~/.codex/config.toml` |

Codex は同じ `mcp_servers` ブロックをすべてのプロジェクトに適用します。プロジェクトごとに別の Bridge を登録したい場合は、サーバキーを区別してください（例：`uaip-GameA`・`uaip-GameB`）。

---

## 設定

インストーラが出力した JSON スニペットを TOML に書き換えます：

```toml
[mcp_servers.uaip-MyGame]
command = "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/.venv/Scripts/python.exe"
args = [
    "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/thin_proxy.py",
]

[mcp_servers.uaip-MyGame.env]
UAIP_UE_EDITOR_PATH = "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe"
UAIP_UPROJECT_PATH  = "E:/MyProjects/MyGame/MyGame.uproject"
```

> **注意**：Codex は TOML を使い、セクション見出しは `[mcp_servers.<サーバキー>]` です。Claude / Cursor / Windsurf の `"mcpServers"` JSON オブジェクトとも、GitHub Copilot の `"servers"` JSON オブジェクトとも形式が異なります。他クライアントのスニペットをそのまま流用しないでください。

- `uaip-MyGame` は自分のサーバキーに置き換えてください
- パスは絶対パスを、フォワードスラッシュ区切りで書いてください（Windows でも TOML 文字列ではフォワードスラッシュを受け付けます）
- `command` にはインストーラが作成した venv の Python を指定するため、system-wide な Python が `PATH` に通っている必要はありません

保存できたら、Codex CLI を再起動してください。

---

## AI 利用ガイド（`AGENTS.md`）

Codex はプロジェクトルートの `AGENTS.md`（プロジェクト固有の指示）と、`~/.codex/AGENTS.md`（ユーザー全体の指示）を読み込みます。UAIP の利用ガイドを次のように配置してください：

```powershell
# プロジェクト単位（推奨）：プロジェクトの AGENTS.md に utility ガイドを追記
Get-Content Plugins/UAIPMCPBridge/install/guides/usage.md `
    | Add-Content AGENTS.md

# あるいはユーザー全体：このマシン上のすべての Codex セッションに適用
mkdir -Force ~/.codex
Get-Content Plugins/UAIPMCPBridge/install/guides/usage.md `
    | Add-Content ~/.codex/AGENTS.md
```

シナリオや Capability などのコンテキストも追加したい場合は、`guides/` 配下の他の `.md` ファイルも同じ要領で `AGENTS.md` に追記してください。

---

## 動作確認

1. プロジェクトディレクトリで Codex CLI を再起動する
2. サーバが認識されているか確認する：Codex の MCP 一覧コマンドに `uaip-MyGame` が connected と表示される
3. Codex に「UAIP の HealthCheck を実行して」と依頼する
4. 初回の呼び出しでエディタが起動します（30〜60 秒ほど）。次回以降は高速です

期待されるレスポンス：

```json
{
  "Success": true,
  "Data": {
    "Status": "Healthy",
    "UAIPVersion": "1.0.0",
    "EngineVersion": "5.8.0"
  }
}
```

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| Codex でサーバが Failed と表示される | `python <thin_proxy.py のパス>` を直接実行してみてください。stderr にエラーが出力されます |
| Codex に MCP 関連の機能が出てこない | Codex CLI のバージョンが MCP サーバに対応しているか確認してください（`codex --version`）。古い場合はアップデート |
| Codex 起動時に TOML パースエラー | セクション見出しは `[mcp_servers.<キー>]` と `[mcp_servers.<キー>.env]` の形式が必要です。文字列はダブルクォートで囲んでください |
| エディタが起動しない | `[mcp_servers.<キー>.env]` ブロックの `UAIP_UE_EDITOR_PATH` と `UAIP_UPROJECT_PATH` を再確認してください |
| Codex が UAIP のガイダンスを無視する | `AGENTS.md` が作業ディレクトリまたは `~/.codex/` に置かれていない可能性があります。Codex が読み取っている場所にあるか確認してください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照してください。
