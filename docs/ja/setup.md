**[English](../en/setup.md)** | [概要に戻る](overview.md)

# セットアップガイド

このガイドでは、UAIP MCP Bridge を使って AI クライアントを UE Editor に接続する手順を説明します。

---

## 前提条件

- `Plugins/UnrealAIIntegrationPlatform` フォルダをプロジェクトの `Plugins` フォルダに入れ、プラグインを有効化済みであること
- Python 3.10 以降がインストール済みで `PATH` が通っていること

---

## Step 1 — インストールスクリプトを実行

UE プロジェクトのルートでターミナルを開き、インストールスクリプトを実行します。スクリプトは Python バージョンを確認し、依存パッケージをインストールしたあと、**対話的に 2 つのパスを入力させて** `config.json` を生成します。

**Windows（PowerShell）:**
```powershell
.\Plugins\UnrealAIIntegrationPlatform\Scripts\MCPBridge\install\install.ps1
```

**macOS / Linux:**
```bash
bash Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/install.sh
```

スクリプトは内部で 3 つのステップを実行します：

| ステップ | 内容 |
|---|---|
| 1/3 | Python 3.10 以降が利用可能か確認 |
| 2/3 | `pip install -r requirements.txt` を実行（`mcp` パッケージをインストール） |
| 3/3 | 2 つのパスを対話的に入力させ、`config.json` を生成 |

### 入力を求められるパス

**UE Editor の実行ファイル**

| プラットフォーム | 入力例 |
|---|---|
| Windows | `E:\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` |
| macOS | `/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor` |
| Linux | `/home/user/UnrealEngine/Engine/Binaries/Linux/UnrealEditor` |

**`.uproject` ファイル**

```
E:\MyProjects\MyGame\MyGame.uproject
```

スクリプトが完了すると、`thin_proxy.py` の隣に `config.json` が作成されます：

```
Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json
```

---

## Step 2 — MCP サーバーキーを決める

サーバーキーは AI クライアントの設定でこのブリッジを識別するための名前です。

| プラグインの場所 | キーの形式 | 例 |
|---|---|---|
| プロジェクトプラグイン | `uaip-<ProjectName>` | `uaip-MyGame` |
| エンジンプラグイン | `uaip-<version>` | `uaip-5.8` |

`<ProjectName>` は `.uproject` ファイルの名前（拡張子なし）です。

---

## Step 3 — MCP サーバーを登録

AI クライアントの MCP 設定ファイルに以下のエントリを追加します。キーは Step 2 で決めたもの、パスは `config.json` に記載されているものを使います。

```json
{
  "mcpServers": {
    "uaip-<ProjectName>": {
      "command": "python",
      "args": ["<絶対パス>/Scripts/MCPBridge/thin_proxy.py"],
      "env": {
        "UAIP_UE_EDITOR_PATH": "<UnrealEditor.exe への絶対パス>",
        "UAIP_UPROJECT_PATH":  "<MyProject.uproject への絶対パス>"
      }
    }
  }
}
```

### クライアント別 設定ファイルの場所

| クライアント | 設定ファイル |
|---|---|
| **Claude Desktop**（Windows） | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop**（macOS） | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Code** — ユーザー共通 | `~/.claude.json` |
| **Claude Code** — プロジェクト | `.uproject` ファイルと同じ場所の `.mcp.json` |
| **Cursor** | `~/.cursor/mcp.json`（ユーザー共通）または `.cursor/mcp.json`（プロジェクト） |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **VS Code（GitHub Copilot）** | `.vscode/mcp.json`（ワークスペース） |

設定ファイルを保存したら AI クライアントを再起動してください。

---

## Step 4 — AI 使用ガイドを配置（推奨）

`Scripts/MCPBridge/install/guides/` ディレクトリには UAIP の使い方を AI に教えるガイドが含まれています。配置することで毎回の会話に UAIP のコンテキストが自動的に読み込まれます。

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
3. AI が MCP 経由で `uaip_execute(CommandName="UAIP.Core.HealthCheck")` を呼び出す
4. 成功すると Editor が起動（未起動の場合）し、`{"Success": true}` が返る

---

## シナリオ実行を有効にする（任意）

`uaip_run_scenario` はデフォルトで無効です。`config.json` を開いて `"enable_scenario": true` を追加し、MCP クライアントを再接続してください：

```json
{
  "editor_path":                  "...",
  "uproject_path":                "...",
  "http_startup_timeout_seconds": 120,
  "command_timeout_seconds":      60,
  "log_level":                    "INFO",
  "enable_scenario":              true
}
```

詳細は [シナリオ実行](scenario.md) を参照してください。

---

## トラブルシューティング

| 症状 | 考えられる原因 | 対処 |
|---|---|---|
| `install.ps1` が実行ポリシーでブロックされる | PowerShell の実行ポリシー | 先に `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` を実行 |
| AI クライアントにツールが表示されない | MCP サーバーが接続されていない | キーと `thin_proxy.py` のパスを確認して再起動 |
| 初回コマンドで約 120 秒タイムアウト | Editor の起動失敗 | `config.json` の `editor_path` と `uproject_path` を確認 |
| 起動時に Python エラー | 依存パッケージ未インストール | インストールスクリプトを再実行 |
| コマンドで `PolicyViolation` | Capability が付与されていない | [Safety & Capabilities](safety.md) を参照 |
| `CommandNotFound` | コマンド名が間違っている | `uaip_list_commands` で正しい完全修飾名を確認 |
