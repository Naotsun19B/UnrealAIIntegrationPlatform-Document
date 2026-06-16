**[English](../en/setup.md)** | [概要に戻る](overview.md)

# セットアップガイド

本ページは、UAIP のインストールと MCP Bridge の AI クライアント登録までを扱うハブです。5 分で動かすところまで進めたい場合は、先に [クイックスタート](quickstart.md) を参照してください。HTTP API・WebSocket・CLI 経由の接続については [接続方法](connections.md) を参照してください。

---

## 前提条件

- `Plugins/UnrealAIIntegrationPlatform` フォルダがプロジェクトの `Plugins` 配下に配置され、プラグインが有効化されている
- Python 3.10 以降がインストールされ `PATH` に通っている
- 対応 AI クライアントのいずれか（Claude Code・Claude Desktop・Cursor・Windsurf・GitHub Copilot）

---

## ステップ 1 — インストールスクリプトを実行

UE プロジェクトルートでターミナルを開き、インストールスクリプトを実行します。Python の確認、依存導入、対話的に **2 つのパスを尋ねて** `config.json` を生成します。

**Windows（PowerShell）:**
```powershell
.\Plugins\UnrealAIIntegrationPlatform\Scripts\MCPBridge\install\install.ps1
```

**macOS / Linux（製品版）:**
```bash
bash Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/install.sh
```

スクリプトの動作：

| ステップ | アクション |
|---|---|
| 1/3 | Python 3.10+ の確認 |
| 2/3 | `pip install -r requirements.txt`（`mcp` パッケージ導入） |
| 3/3 | `editor_path` + `uproject_path` を尋ね、`config.json` を生成 |

### 入力を求められるパス

**UE Editor 実行ファイル**

| プラットフォーム | 例 |
|---|---|
| Windows | `E:\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` |
| macOS | `/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor` |
| Linux | `/home/user/UnrealEngine/Engine/Binaries/Linux/UnrealEditor` |

**`.uproject` ファイル**

```
E:\MyProjects\MyGame\MyGame.uproject
```

`config.json` は `Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json` に生成されます。

---

## ステップ 2 — MCP サーバーキーを決定

サーバーキーは AI クライアント設定内で本 Bridge インスタンスを識別するためのもの。

| プラグイン配置 | キー形式 | 例 |
|---|---|---|
| プロジェクトプラグイン | `uaip-<プロジェクト名>` | `uaip-MyGame` |
| エンジンプラグイン | `uaip-<バージョン>` | `uaip-5.8` |

プロジェクト名は `.uproject` ファイル名から拡張子を除いたものを使ってください。このキーは AI クライアント上でのサーバ表示にだけ影響するもので、Bridge 側と一致させる必要はありません。

---

## クライアント別設定ファイル

使用するクライアントを選び、対応ページに進んでください：

| クライアント | ページ | 備考 |
|---|---|---|
| **Claude Code**（CLI / VS Code 拡張） | [claude-code.md](clients/claude-code.md) | 最良サポート。プロジェクト毎の `.mcp.json` またはグローバル `~/.claude.json` |
| **Claude Desktop** | [claude-desktop.md](clients/claude-desktop.md) | `claude_desktop_config.json` |
| **Cursor** | [cursor.md](clients/cursor.md) | `~/.cursor/mcp.json` または `.cursor/mcp.json` |
| **Windsurf** | [windsurf.md](clients/windsurf.md) | `~/.codeium/windsurf/mcp_config.json` |
| **GitHub Copilot（VS Code）** | [copilot.md](clients/copilot.md) | `.vscode/mcp.json` |

各クライアント別ページには、設定 JSON のサンプル、`Scripts/MCPBridge/install/guides/` 配下にある AI 利用ガイドの配置方法、動作確認の手順（「AI に HealthCheck を実行させる」）がそろっています。

---

## ステップ 4 — シナリオ実行を有効化（オプション）

`uaip_run_scenario` はデフォルトでは無効です。有効化するには `config.json` を以下のように編集してください：

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

変更したあとは MCP クライアントを再接続してください。シナリオで何ができるかは [シナリオ実行](scenario.md) を参照してください。

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| `install.ps1` が実行ポリシーでブロック | PowerShell 実行ポリシー | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 後に再実行 |
| AI クライアントでツール未検出 | MCP サーバー未接続 | キーと `thin_proxy.py` パスを確認、クライアント再起動 |
| 初回コマンドで 120 秒タイムアウト | エディタ起動失敗 | `config.json` の `editor_path` と `uproject_path` を検証 |
| Python 起動エラー | 依存不足 | インストールスクリプト再実行 |
| コマンドで `PolicyViolation` | Capability 未付与、または SafetyPolicy フラグ OFF | [Safety & Capabilities](safety.md) 参照 |
| `CommandNotFound` | コマンド名間違い | `uaip_list_commands(ProviderPrefix="UAIP.Core")` |

詳細な診断は [トラブルシューティング](troubleshooting.md) を参照。
