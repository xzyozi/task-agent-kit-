#!/usr/bin/env python3
"""テンプレートリポジトリの試用コピーを、一時ディレクトリに作成・削除する。

標準ライブラリと git コマンドだけを使う。外部ネットワークには接続しない
（ローカルのリポジトリから clone する）。

使い方:
    python setup_trial.py                      # 現在のリポジトリを %TEMP%/tak-trial へ clone
    python setup_trial.py --force              # 既存の試用コピーを削除して作り直す
    python setup_trial.py --remove             # 試用コピーを削除する
    python setup_trial.py --source <path> --dest <path> --ref <commit-ish>

安全上の制約:
    - 作成・削除する場所は、一時ディレクトリ配下で、名前が `tak-trial` で始まるものに限る。
    - 元のリポジトリは変更しない（読み取りのみ）。
"""
from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import NoReturn

NAME_PREFIX = "tak-trial"


def run_git(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """git を実行し、(終了コード, 標準出力, 標準エラー) を返す。シェルは使わない。"""
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def fail(message: str) -> NoReturn:
    print(f"エラー: {message}", file=sys.stderr)
    sys.exit(1)


def resolve_source(arg: str | None) -> Path:
    """元のリポジトリのルートを返す。git リポジトリでなければ停止する。"""
    start = Path(arg) if arg else Path.cwd()
    if not start.exists():
        fail(f"元のパスが存在しません: {start}")
    code, out, err = run_git(["rev-parse", "--show-toplevel"], cwd=start)
    if code != 0:
        fail(f"git リポジトリではありません: {start}\n{err}")
    return Path(out).resolve()


def resolve_dest(arg: str | None) -> Path:
    """作成先を返す。一時ディレクトリ配下で、名前が tak-trial で始まるものに限る。"""
    temp_root = Path(tempfile.gettempdir()).resolve()
    dest = Path(arg).resolve() if arg else temp_root / NAME_PREFIX
    try:
        dest.relative_to(temp_root)
    except ValueError:
        fail(f"作成先は一時ディレクトリ配下に限ります: {dest}（一時ディレクトリ: {temp_root}）")
    if dest == temp_root or not dest.name.startswith(NAME_PREFIX):
        fail(f"作成先の名前は '{NAME_PREFIX}' で始めてください: {dest.name}")
    return dest


def _on_remove_error(func, path, _exc) -> None:
    """読み取り専用ファイル（git のオブジェクトなど）を削除できるようにする。"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _rmtree_once(dest: Path) -> None:
    # Python 3.12 以降は onexc、それ以前は onerror を使う。
    if sys.version_info >= (3, 12):
        shutil.rmtree(dest, onexc=_on_remove_error)
    else:
        shutil.rmtree(dest, onerror=_on_remove_error)


def remove_dest(dest: Path, attempts: int = 6, wait_seconds: float = 0.5) -> None:
    """削除する。Windows では、他のプロセスが一時的にフォルダを掴むことがあるため、再試行する。"""
    for attempt in range(1, attempts + 1):
        try:
            _rmtree_once(dest)
            return
        except FileNotFoundError:
            return
        except PermissionError as exc:
            if attempt == attempts:
                fail(
                    f"削除できませんでした（他のプロセスが使用中の可能性があります）: {dest}\n"
                    f"そのフォルダを開いているツールを閉じて、もう一度実行してください。\n{exc}"
                )
            time.sleep(wait_seconds * attempt)


def warn_uncommitted(source: Path) -> None:
    """clone はコミット済みの内容だけを複製する。未コミットの変更があれば警告する。"""
    code, out, _ = run_git(["status", "--porcelain"], cwd=source)
    if code == 0 and out:
        lines = out.splitlines()
        print(
            f"警告: 元のリポジトリに未コミットの変更が {len(lines)} 件あります。"
            "試用コピーには含まれません。",
            file=sys.stderr,
        )


def create(source: Path, dest: Path, ref: str | None, force: bool) -> None:
    if dest.exists():
        if not force:
            fail(f"作成先が既に存在します: {dest}\n作り直す場合は --force を付けてください。")
        remove_dest(dest)

    warn_uncommitted(source)

    if ref is None:
        code, ref, err = run_git(["rev-parse", "HEAD"], cwd=source)
        if code != 0:
            fail(f"元のリポジトリの HEAD を取得できません。\n{err}")

    code, _, err = run_git(["clone", "--quiet", "--no-hardlinks", str(source), str(dest)])
    if code != 0:
        fail(f"clone に失敗しました。\n{err}")

    code, _, err = run_git(["checkout", "--quiet", "--detach", ref], cwd=dest)
    if code != 0:
        remove_dest(dest)
        fail(f"コミットを取り出せませんでした: {ref}\n{err}")

    _, short, _ = run_git(["log", "-1", "--format=%h %s"], cwd=dest)
    _, status, _ = run_git(["status", "--porcelain"], cwd=dest)
    print(f"作成先: {dest}")
    print(f"元: {source}")
    print(f"コミット: {short}")
    print(f"作業ツリー: {'クリーン' if not status else '変更あり（想定外）'}")


def remove(dest: Path) -> None:
    if not dest.exists():
        print(f"削除対象がありません: {dest}")
        return
    is_repo = (dest / ".git").exists()
    is_empty = dest.is_dir() and not any(dest.iterdir())
    if not (is_repo or is_empty):
        fail(f"git リポジトリでも空のフォルダでもないため削除しません: {dest}")
    remove_dest(dest)
    print(f"削除しました: {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="テンプレートの試用コピーを作成・削除する")
    parser.add_argument("--source", help="元のリポジトリ（既定: 現在のディレクトリが属するリポジトリ）")
    parser.add_argument("--dest", help=f"作成先（既定: 一時ディレクトリ/{NAME_PREFIX}）")
    parser.add_argument("--ref", help="取り出すコミット（既定: 元のリポジトリの HEAD）")
    parser.add_argument("--force", action="store_true", help="既存の作成先を削除して作り直す")
    parser.add_argument("--remove", action="store_true", help="作成先を削除する（作成はしない）")
    args = parser.parse_args()

    dest = resolve_dest(args.dest)
    if args.remove:
        remove(dest)
        return
    source = resolve_source(args.source)
    create(source, dest, args.ref, args.force)


if __name__ == "__main__":
    main()
