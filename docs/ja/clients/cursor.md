**[English](../../en/clients/cursor.md)** | [接続方法に戻る](../connections.md#mcp-bridge)

# Cursor

[Cursor](https://cursor.sh/) は VS Code ベースの AI ファースト IDE です。MCP サーバの登録は `mcp.json` 経由で行います。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ユーザー全体 | `~/.cursor/mcp.json` |
| プロジェクト | `.cursor/mcp.json`（`.uproject` の隣） |

プロジェクトスコープがおすすめです — 複数の UE プロジェクトを使い分けても衝突しません。

---

## 設定

インストーラが表示したスニペットを貼り付けます：

```json
{
  "mcpServers": {
    "uaip-MyGame": {
      "command": "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/.venv/Scripts/python.exe",
      "args": [
        "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/thin_proxy.py"
      ],
      "env": {
        "UAIP_UE_EDITOR_PATH": "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe",
        "UAIP_UPROJECT_PATH":  "E:/MyProjects/MyGame/MyGame.uproject"
      }
    }
  }
}
```

- `uaip-MyGame` は自分のサーバキーに置き換えてください
- パスは **絶対パスを、フォワードスラッシュ区切りで** JSON に書いてください
- `command` にはインストーラが作成した venv の Python を指定するため、system-wide な Python が `PATH` に通っている必要はありません

保存できたら、**Cursor → Settings → Cursor Settings → Features → MCP** に `uaip-MyGame` が表示されているはずです。表示されない場合は、更新アイコンをクリックするか Cursor を再起動してみてください。

---

## AI 利用ガイド

ガイドファイルはそのまま `.cursor/uaip/guides/` にコピーします。`.cursor/rules/` には **置きません**：

```powershell
mkdir -Force .cursor/uaip/guides
cp Plugins/UAIPMCPBridge/install/guides/*.md .cursor/uaip/guides/
```

続いて、ガイドの場所を案内するルールを 1 つだけ `.cursor/rules/uaip.mdc` として作成します：

```markdown
---
description: UAIP — driving and observing the Unreal Editor through the uaip_* MCP tools
alwaysApply: true
---
The UAIP usage guides are in `.cursor/uaip/guides/` at the project root.
Before the first uaip_* tool call in a conversation, read `.cursor/uaip/guides/index.md`,
then open only the guides it points to for the task at hand. Do not read every guide.
```

`.cursor/rules/` に置かない理由：`alwaysApply: true` のルールはすべてのチャットに含まれるため、ガイドを 1 つずつルールにすると、ガイド全体（15 万字超）が毎回の会話に入ります。この案内ルールは数行で済み、ガイド本体はタスクに必要なときだけ読まれます。パスは平文で書いてください。ルール内の `@ファイル` 参照は、参照先の中身を展開します。

Bridge を更新したら、`python Plugins/UAIPMCPBridge/install/check_guides.py --deployed .cursor/uaip/guides` で配置済みのガイドが最新か確認できます（`--apply` を付けると更新します）。

### 旧配置からの移行

以前のこのページの手順では、すべてのガイドを `.mdc` として `.cursor/rules/` にコピーしていました。`uaip.mdc` を作る前に、それらを削除してください：

```powershell
Get-ChildItem Plugins/UAIPMCPBridge/install/guides/*.md | ForEach-Object {
    Remove-Item -ErrorAction SilentlyContinue ".cursor/rules/$($_.BaseName).mdc"
}
```

---

## 動作確認

1. Cursor を再起動するか、サーバ横の更新アイコンをクリックする
2. Cursor のチャットパネルを開く
3. 「UAIP の HealthCheck を実行して」と依頼する
4. Cursor が UAIP を呼び出すタイミングで、tool-use インジケータが表示されます

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| サーバが Settings → MCP に表示されない | JSON の構文エラーかパスの誤りが原因です。JSON を検証してから Cursor を再起動してください |
| サーバは表示されるが "Failed to start" になる | サーバ名をクリックすると stderr を確認できます。Python のパス誤りや `mcp` パッケージ未導入がよくある原因です |
| ツール呼び出しは成功するが、AI がガイドに従わない | `.cursor/rules/uaip.mdc` が無い、拡張子が `.mdc` でない、または `alwaysApply: true` が無い可能性があります。修正してから再起動してください |
| 初回呼び出しでエディタが起動しない | `env` ブロックの `UAIP_UE_EDITOR_PATH` と `UAIP_UPROJECT_PATH` を再確認してください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。
