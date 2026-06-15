![UE Version](https://img.shields.io/badge/Unreal%20Engine-5.8-0e1128?logo=unrealengine&logoColor=white)
[![License: Fab Standard License (Fab EULA)](https://img.shields.io/badge/License-Fab%20Standard%20License%20%28Fab%20EULA%29-blue)](https://www.fab.com/eula)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/Naotsun_UE?style=social)](https://twitter.com/Naotsun_UE)

# UnrealAIIntegrationPlatform

<!--ts-->
   * [概要](#概要)
   * [動作環境](#動作環境)
   * [インストール](#インストール)
   * [セットアップ](#セットアップ)
      * [Step 1 — Python 依存パッケージをインストール](#step-1--python-依存パッケージをインストール)
      * [Step 2 — MCP サーバーを登録](#step-2--mcp-サーバーを登録)
      * [Step 3 — AI 使用ガイドを配置（推奨）](#step-3--ai-使用ガイドを配置推奨)
      * [Step 4 — セットアップを確認](#step-4--セットアップを確認)
   * [機能](#機能)
      * [Editor ドメインコマンド](#editor-ドメインコマンド)
      * [Runtime ドメインコマンド](#runtime-ドメインコマンド)
      * [シナリオ実行](#シナリオ実行)
      * [Artifacts（成果物）](#artifacts成果物)
   * [設定](#設定)
   * [ライセンス](#ライセンス)
   * [作者](#作者)
   * [履歴](#履歴)
<!--te-->

## 概要

**UnrealAIIntegrationPlatform (UAIP)** は、AI エージェントが UE Editor と Runtime を **操作・観測・実行・検証** できるようにする Unreal Engine プラグインです。

Claude Code、Cursor、Windsurf、GitHub Copilot などの AI ツールが **Model Context Protocol (MCP)** 経由で接続し、意味的なコマンドを発行できます。座標クリックや脆弱な UI スクリプトは不要です。

主な機能：
- **Editor 操作** — アセットの開閉・保存、Blueprint 編集、アクター操作、Automation Test の実行、Sequencer の制御など、200 以上の登録済みコマンドで Editor のほぼすべての機能を網羅
- **視覚的・構造的な観測** — 任意の Editor タブやビューポートのスクリーンショット取得、ワールド状態・Slate ウィジェットツリー・エディタ状態の JSON ダンプ
- **Runtime / PIE 制御** — PIE の開始・停止、アクターのスポーン、入力インジェクト、Gauntlet テストの実行、アクタープロパティのアサート
- **シナリオ実行** — 複数コマンドを順序付きリストとして一括送信。失敗時の中断・リトライ・ステップごとのタイムアウトに対応
- **マルチ Transport** — MCP・HTTP・WebSocket・CLI から操作可能
- **Safety & Capability Policy** — セッション単位の Capability ゲートとプロセス単位の SafetyPolicy スイッチ

## 動作環境

対象バージョン : UE 5.8  
対象プラットフォーム : Windows  
Python : 3.10 以降（MCP Bridge に必要）

## インストール

プロジェクトの `Plugins` フォルダに `Plugins/UnrealAIIntegrationPlatform` フォルダを入れてください。  
プラグインのインストール後に機能が使用できない場合は、**編集 > プラグイン** からプラグインが有効になっているかご確認ください。

## セットアップ

MCP Bridge（`Scripts/MCPBridge/`）は UE Editor と AI クライアントを HTTP 経由でつなぐ Python プロキシです。詳細なセットアップガイドはプラグイン内の `Scripts/MCPBridge/install/SETUP.md` にあります。そのファイルを開いて AI に手順を実行させてください。

以下は概要です。

### Step 1 — Python 依存パッケージをインストール

`Scripts/MCPBridge/install/` ディレクトリにあるインストールスクリプトを実行します：

| プラットフォーム | コマンド |
|---|---|
| Windows | `install.ps1` |
| macOS / Linux | `install.sh` |

これにより Python の依存パッケージがインストールされ、`thin_proxy.py` の隣に `config.json` が生成されます。

### Step 2 — MCP サーバーを登録

AI クライアントの MCP 設定ファイルに以下のエントリを追加してください：

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

| クライアント | 設定ファイルの場所 |
|---|---|
| **Claude Desktop** (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop** (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Code** — ユーザー共通 | `~/.claude.json` |
| **Claude Code** — プロジェクト | `.uproject` ファイルと同じ場所の `.mcp.json` |
| **Cursor** | `~/.cursor/mcp.json`（ユーザー共通）または `.cursor/mcp.json`（プロジェクト） |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **VS Code (GitHub Copilot)** | `.vscode/mcp.json`（ワークスペース） |

設定ファイルを保存したら AI クライアントを再起動してください。

### Step 3 — AI 使用ガイドを配置（推奨）

`Scripts/MCPBridge/install/guides/` ディレクトリには UAIP の使い方を AI に教えるガイドが含まれています。配置することで、毎回の会話に UAIP のコンテキストが自動的に読み込まれます。

| クライアント | 手順 |
|---|---|
| **Claude Code** | 全 `.md` ファイルを `~/.claude/rules/uaip/` にコピーし、`~/.claude/CLAUDE.md` に `@rules/uaip/usage.md` を追記 |
| **Cursor** | `.md` ファイルを `.cursor/rules/` に `.mdc` 拡張子でコピー |
| **Windsurf** | `usage.md` の内容を `.windsurfrules` に追記 |
| **GitHub Copilot** | `usage.md` の要約を `.github/copilot-instructions.md` に追記 |

### Step 4 — セットアップを確認

1. AI クライアントを再起動する
2. AI に「UAIP の HealthCheck を実行して」と聞く
3. AI が MCP 経由で `uaip_execute(CommandName="UAIP.Core.HealthCheck")` を呼び出すはずです
4. 成功すると Editor が起動（未起動の場合）し、`{"Success": true}` が返ります

## 機能

### Editor ドメインコマンド

`UAIP.Editor.*` 名前空間のコマンドで Editor のほぼすべての機能をカバーします：

| プロバイダープレフィックス | カバー範囲 |
|---|---|
| `UAIP.Editor.Workspace` | タブ管理、グラフエディタフォーカス、LiveCoding、Undo-Redo |
| `UAIP.Editor.Assets` | CreateAsset、DeleteAsset、OpenAsset、SaveAll、SearchAssets、… |
| `UAIP.Editor.Level` | PlaceActorInLevel、SetActorTransform、OpenLevel、… |
| `UAIP.Editor.Blueprint` | Blueprint の変数・関数・グラフ編集 |
| `UAIP.Editor.Property` | Get/SetActorProperty |
| `UAIP.Editor.UMG` | ウィジェットツリー編集 |
| `UAIP.Editor.Material` | マテリアルグラフ編集 |
| `UAIP.Editor.Niagara` | Niagara VFX 編集 |
| `UAIP.Editor.Physics` | 物理アセット編集 |
| `UAIP.Editor.Dataflow` | データフローグラフ編集 |
| `UAIP.Editor.Skeleton` | スケルトン・スケルタルメッシュ編集 |
| `UAIP.Editor.AnimBlueprint` | アニムブループリント・ステートマシン編集 |
| `UAIP.Editor.BehaviorTree` | ビヘイビアツリー・ブラックボード編集 |
| `UAIP.Editor.EQS` | EQS クエリ編集 |
| `UAIP.Editor.MetaSound` | MetaSound グラフ編集 |
| `UAIP.Editor.Sequencer` | レベルシーケンス編集 |
| `UAIP.Editor.StateTree` | StateTree 編集 |
| `UAIP.Editor.ControlRig` | ControlRig 階層・RigVM グラフ |
| `UAIP.Editor.GameplayTags` | GameplayTag 管理 |
| `UAIP.Editor.GameFeatures` | GameFeature プラグイン管理 |
| `UAIP.Editor.EnhancedInput` | Input Action・Mapping Context 編集 |
| `UAIP.Editor.PCG` | PCG グラフ編集 |
| `UAIP.Editor.Observation` | CaptureActiveWindowImage、DumpEditorState、DumpSlateTree、… |
| `UAIP.Editor.Execution` | RunAutomationTest、RunEditorPythonScript、RunEditorUtility |
| `UAIP.Editor.UIAutomation` | ClickWidget、PressKey、FillForm、WaitForWidget、… |

### Runtime ドメインコマンド

`UAIP.Runtime.*` 名前空間のコマンドでゲームの実行状態を制御します：

| プロバイダープレフィックス | カバー範囲 |
|---|---|
| `UAIP.Runtime.PIE` | StartPIE、StopPIE、LoadMap |
| `UAIP.Runtime.World` | SpawnActor、TeleportActor、ExecuteConsoleCommand |
| `UAIP.Runtime.Observation` | DumpWorldState、CaptureViewportImage、CapturePerformanceSnapshot |
| `UAIP.Runtime.GAS` | GetAttributeValues、FindAttributeSetClasses、… |
| `UAIP.Runtime.Input` | InjectInputKey、InjectEnhancedInputAction |
| `UAIP.Runtime.Assertion` | WaitSeconds、WaitForCondition、AssertActorProperty（シナリオのプリミティブ） |
| `UAIP.Runtime.Execution` | RunGauntletTest、RunRuntimeAutomationTest |

### シナリオ実行

`uaip_run_scenario` は複数コマンドを順序付きリストとして一括送信します。各ステップはゲームスレッド上で順番に実行され、失敗時の中断・リトライ・ステップごとのタイムアウトを宣言的に設定できます。

例 — PIE バリデーションの完全なフロー：

```json
{
  "ScenarioName": "PIE_HealthCheck",
  "Steps": [
    { "StepName": "Load",   "CommandName": "UAIP.Runtime.PIE.LoadMap",    "Params": { "MapPath": "/Game/Maps/TestMap" } },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE",   "Params": {} },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds", "Params": { "Seconds": 2 } },
    { "StepName": "Cap",    "CommandName": "UAIP.Runtime.Observation.CaptureViewportImage", "Params": {} },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE",    "Params": {}, "AbortOnFailure": false }
  ]
}
```

シナリオ実行を有効にするには `config.json` に `"enable_scenario": true` を追加してください。

### Artifacts（成果物）

すべてのコマンドは成果物（PNG スクリーンショット、JSON 状態ダンプ、ログ、レポート）を返します。成果物は `Saved/UAIP/<SessionId>/` 以下に保存され、AI はユーザーに確認を取らずに直接読み取れます。

## 設定

Safety とCapability の制御は `Config/DefaultUAIP.ini` で設定します：

```ini
[UAIP.SafetyPolicy]
ReadOnly=False
DisableSave=False
AllowLogDump=True
AllowContextMenuMutation=True
AllowKeyboardInput=True
AllowKeyboardModifierInput=True

; DefaultDenied の Capability を解除する場合：
; +AllowedCapabilities=BlueprintEdit
; +AllowedCapabilities=SkeletonAssetEdit
```

| キー | デフォルト | 効果 |
|---|---|---|
| `ReadOnly` | `False` | すべての書き込みコマンドを拒否 |
| `DisableSave` | `False` | ディスク書き込みコマンドを拒否 |
| `AllowLogDump` | `False` | `DumpOutputLog` / `DumpMessageLog` を許可 |
| `AllowContextMenuMutation` | `False` | `InvokeContextMenuAction` を許可 |
| `AllowKeyboardInput` | `False` | `PressKey` を許可 |
| `AllowKeyboardModifierInput` | `False` | `PressKey` 内の Ctrl/Alt/Shift を許可 |
| `AllowPasswordFieldWrite` | `False` | `FillForm` でパスワードフィールドへの書き込みを許可 |
| `DisablePIEStart` | `False` | PIE 起動を拒否 |
| `AllowedCapabilities` | 空 | DefaultDenied の Capability を解除（1行に1つ） |
| `DeniedCommands` | 空 | ブロックするコマンドの完全修飾名 |

## ライセンス

本リポジトリの Releases で配布するデモバイナリは、リリースアーカイブに同梱の `EULA.txt` に従って提供されます。  
Fab で配布される製品版は [Fab Standard License (Fab EULA)](https://www.fab.com/ja/eula) に基づいて提供されます。  
特に明記がない限り、本リポジトリ内のドキュメントの著作権は © 2026 Naotsun に帰属し、無断転載は禁止です。

## 作者

[Naotsun](https://twitter.com/Naotsun_UE)

## 履歴

- (2026/06/16) v1.0  
  初版公開
