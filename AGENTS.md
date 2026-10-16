# AGENTS.md

このファイルは、AIツール共通の入口です。詳細な本文をここへ重複して書かず、正本を各参照先に置きます。

## 作業開始時

1. `PROJECT.md` を読み、「状態」を確認する。
2. 状態が `template` の場合は、他の作業より先に、ユーザーへ「初期設定（`SETUP.md`）を始めるか、テンプレート自体の保守か」を1回確認する。初期設定が選ばれた場合だけ `SETUP.md` を実行する。保守が選ばれた場合、または依頼内容が最初からテンプレート自体の保守である場合は、確認せずに `SETUP.md` を実行しない。依頼文が「初期設定してください」でも、この確認を省略しない。
3. 状態が `configured` の場合は、`PROJECT.md` の目的・範囲・非対象を確認してから作業する。
4. 作業に入る前に `references/safety-baseline.md` を読み、適用する。
5. 現在の作業に直接関係するファイルだけを読む。

## 読み取りルール

- 作業と無関係なファイルを推測で読まない。
- `templates/` は、雛形を使って agent 定義や skill を作る・改修するときだけ読む。通常タスクでは参照も変更もしない。
- 認証情報のファイル（`.env*`、`*.key`、`*.pem` など）を読まない。

## 運用開始後の追加・変更

状態が `configured` で agent 定義や skill を新規追加・変更する場合は、`references/agent-anatomy.md` と、使うツールの `references/agents/` の文書（skill は `references/skills.md`）と `templates/` に従い、追加・変更したパスを `PROJECT.md` の「Canonical locations」に記録する。

## 書き込みルール

- 既存ファイルを上書きしない。衝突したら停止して報告する。
- 認証情報、パスワード、API キー、トークン、秘密鍵を保存しない。
- 作成・更新するファイルは UTF-8（BOM なし）/ LF とする。
- 不明点や承認が必要な操作は、勝手に補完せず停止する。

## 正本

- 共通入口: `AGENTS.md`
- プロジェクト状態: `PROJECT.md`
- 初期設定の手順: `SETUP.md`（設定完了後に削除される）
- 共通の安全規約: `references/safety-baseline.md`
- agent 定義の構造: `references/agent-anatomy.md`
- ツール別の配置先・キー・権限: `references/agents/`（`kiro.md`、`claude-code.md`、`gemini-cli.md`、`codex-cli.md`）
- skill の扱いと配置先: `references/skills.md`
- 雛形: `templates/`
- Claude Code 入口: `CLAUDE.md`（`AGENTS.md` への薄い参照）
- Gemini CLI 入口: `GEMINI.md`（`AGENTS.md` への薄い参照）
- Kiro と Codex は `AGENTS.md` を直接読むため、専用の入口を持たない。
