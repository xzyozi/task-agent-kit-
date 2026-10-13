# task-agent-kit

特定タスクを消化する agent 構成（入口・安全規約・agent 定義）を、新しいプロジェクトで
素早く立ち上げるためのテンプレートリポジトリ。

このリポジトリ自体がテンプレートである。clone（または GitHub の「Use this template」）した
プロジェクトのルートで、agent が `SETUP.md` に従って対話しながら穴埋めする。

## 使い方

1. このリポジトリを clone する（または「Use this template」で新規リポジトリを作る）。
2. clone したプロジェクトのルートを agent で開く。`AGENTS.md` が `SETUP.md` の実行を指示する。
3. `SETUP.md` の質問に答える。agent が `PROJECT.md` と agent 定義を生成する。
4. 承認すると `SETUP.md` が削除され、`PROJECT.md` の状態が `configured` になる。

## 構成

| パス                      | 役割                                                         |
| ------------------------- | ------------------------------------------------------------ |
| `SETUP.md`                | 最初に実行する手順。agent への指示そのもの                   |
| `AGENTS.md`               | AI ツール共通の入口                                          |
| `PROJECT.md`              | プロジェクトの状態と範囲（穴埋め対象）                       |
| `CLAUDE.md` / `GEMINI.md` | Claude Code / Gemini CLI 用の薄い入口                        |
| `references/`             | agent が参照する正本（agent 定義の構造、共通の安全規約など） |
| `templates/`              | 穴埋めして使う agent 定義・skill の雛形                      |

Kiro と Codex は `AGENTS.md` を直接読む。

## 設計方針

- 文書はそのまま agent への指示になる形で書く。人間向けの説明と agent 向けの指示を別々に持たない。
- 同じ内容を複数の場所に書かない。この README は案内にとどめ、詳細は各正本を指す。
- 配布先で動くよう、必須の手順はリポジトリ内に持つ。グローバルの skill は任意の補助とする。
- コードのライブラリやプラグイン機構、入口の自動生成スクリプトは作らない。
- 作成するファイルは UTF-8（BOM なし）/ LF とする。

## テンプレート自体の保守

このリポジトリの原本を保守する場合は、`SETUP.md` を実行しない。変更前に次を確認する。

- `AGENTS.md`、`SETUP.md`、`references/`、`templates/` の参照パスが実在する。
- 穴埋め用の `{{ }}` が、`PROJECT.md`、`templates/`、`references/`、`SETUP.md`、`README.md` 以外に残っていない。
- 特定ドメインのサーバ、パス、コマンドを雛形や参照文書に持ち込んでいない。
