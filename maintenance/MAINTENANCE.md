# テンプレート自体の保守

このリポジトリの原本を保守する場合は、`SETUP.md` を実行しない。変更前に次を確認する。

- `AGENTS.md`、`SETUP.md`、`references/`、`templates/`、`maintenance/` の参照パスが実在する。
- 中身を持つプレースホルダ（二重波括弧で囲んだ、空でない文字列）が、`PROJECT.md` と `templates/` 以外に残っていない。他の文書で言及する場合は、中身のない二重波括弧だけで書く。
- 特定ドメインのサーバ、パス、コマンドを雛形や参照文書に持ち込んでいない。
- `SETUP.md` への言及は、`SETUP.md` 自身、`AGENTS.md`、`README.md`、`references/skills.md` の同梱表、`maintenance/` に限る。それ以外の参照文書に書くと、`SETUP.md` の削除後に参照先が失われる。

## ブランチと PR

- 統合先は `develop` とする。作業ブランチは `develop` から作成し、PR の base も `develop` にする。
- `main` への反映は、`develop` から `main` への PR で行う。作業ブランチから `main` へ直接 PR を出さない。

## 変更後の動作確認

初期設定の流れを実際に試すときは、元のリポジトリを汚さないよう、使い捨ての試用コピーで行う。
試用コピーの作成・作り直し・削除は、`maintenance/skills/template-trial-clone/SKILL.md` に従う。

試用コピーには、コミット済みの内容だけが入る。試したい変更は、先にコミットしておく。
