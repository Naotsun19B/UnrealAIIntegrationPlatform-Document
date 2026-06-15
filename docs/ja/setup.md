**[English](../en/setup.md)** | [概要に戻る](overview.md)

# セットアップガイド

このガイドでは、UAIP MCP Bridge を使って AI クライアントを UE Editor に接続する手順を説明します。

---

## 前提条件

- `Plugins/UnrealAIIntegrationPlatform` フォルダをプロジェクトの `Plugins` フォルダに入れ、プラグインを有効化済みであること
- Python 3.10 以降がインストール済みであること

---

## Step 1 — Python 依存パッケージをインストール

プラグイン内の `Scripts/MCPBridge/install/` ディレクトリにあるインストールスクリプトを実行します：

| プラットフォーム | コマンド |
|---|---|
| Windows | `install.ps1` |
| macOS / Linux | `install.sh` |

これにより Python の依存パッケージがインストールされ、`thin_proxy.py` の隣に `config.json` が生成されます。

---

## Step 2 — MCP サーバーキーを決める

サーバーキーは AI クライアントの設定でブリッジを識別するために使います。

| プラグインの場所 | キーの形式 | 例 |
|---|---|---|
| プロジェクトプラグイン | `uaip-<ProjectName>` | `uaip-MyGame` |
| エンジンプラグイン | `uaip-<version>` | `uaip-5.8` |

---

## Step 3 — MCP サーバーを登録

AI クライアントの MCP 設定ファイルに以下のエントリを追加します。キーは Step 2 で決めたもの、パスは `config.json` の値を使います。

```json
{
  "mcpServers": {
    "uaip-<ProjectName>": {
      "command": "python",
      "args": ["<bridge-rootへの絶対パス>/thin_proxy.py"],
      "env": {
        "UAIP_UE_EDITOR_PATH": "<UnrealEditor.exeへの絶対パス>",
        "UAIP_UPROJECT_PATH":  "<MyProject.uprojectへの絶対パス>"
      }
    }
  }
}
```

### クライアント別 設定ファイルの場所

| クライアント | 設定ファイル |
|---|---|
| **Claude Desktop** (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop** (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Code** — ユーザー共通 | `~/.claude.json` |
| **Claude Code** — プロジェクト | `.uproject` ファイルと同じ場所の `.mcp.json` |
| **Cursor** | `~/.cursor/mcp.json`（ユーザー共通）または `.cursor/mcp.json`（プロジェクト） |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **VS Code (GitHub Copilot)** | `.vscode/mcp.json`（ワークスペース） |

設定ファイルを保存したら AI クライアントを再起動してください。

---

## Step 4 — AI 使用ガイドを配置（推奨）

`Scripts/MCPBridge/install/guides/` ディレクトリには UAIP の使い方を AI に教えるガイドが含まれています。配置することで、毎回の会話に UAIP のコンテキストが自動的に読み込まれます。

| クライアント | 手順 |
|---|---|
| **Claude Code** | 全 `.md` ファイルを `~/.claude/rules/uaip/` にコピーし、`~/.claude/CLAUDE.md` に `@rules/uaip/usage.md` を追記 |
| **Cursor** | `.md` ファイルを `.cursor/rules/` に `.mdc` 拡張子でコピー |
| **Windsurf** | `usage.md` の内容を `.windsurfrules` に追記 |
| **GitHub Copilot** | `usage.md` の要約を `.github/copilot-instructions.md` に追記 |

---

## Step 5 — セットアップを確認

1. AI クライアントを再起動する
2. AI に「UAIP の HealthCheck を実行して」と聞く
3. AI が MCP 経由で `uaip_execute(CommandName="UAIP.Core.HealthCheck")` を呼び出すはずです
4. 成功すると Editor が起動（未起動の場合）し、`{"Success": true}` が返ります

---

## シナリオ実行を有効にする（任意）

`uaip_run_scenario` はデフォルトで無効です。`config.json` に `"enable_scenario": true` を追加して MCP クライアントを再接続すると有効になります：

```json
{
  "editor_path":    "...",
  "uproject_path":  "...",
  "enable_scenario": true
}
```

詳細は [シナリオ実行](scenario.md) を参照してください。

---

## トラブルシューティング

| 症状 | 考えられる原因 | 対処 |
|---|---|---|
| AI クライアントにツールが表示されない | MCP サーバーが接続されていない | サーバーキーと設定ファイルのパスを確認して再起動 |
| 約 120 秒でタイムアウト | Editor の起動失敗 | `config.json` のエディタパスと `.uproject` パスを確認 |
| 起動時に Python エラー | 依存パッケージ未インストール | `install.ps1`（または `install.sh`）を再実行 |
| 初回コマンドで `PolicyViolation` | Capability が付与されていない | [Safety & Capabilities](safety.md) を参照 |
| `CommandNotFound` | コマンド名が間違っている | `uaip_list_commands` で正しい完全修飾名を確認 |
