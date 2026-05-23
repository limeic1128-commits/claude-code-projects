"""
デスクトップフォルダー自動整理スクリプト (Windows用)
使い方: python organize_desktop.py
オプション: python organize_desktop.py --dry-run  # 実際には移動せず確認のみ
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# ===== 整理ルール設定 =====
# 拡張子 → 移動先フォルダー名
RULES = {
    # 画像
    "画像": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".heic", ".raw"],
    # 動画
    "動画": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    # 音楽
    "音楽": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    # ドキュメント
    "ドキュメント": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv"],
    # 圧縮ファイル
    "圧縮ファイル": [".zip", ".rar", ".7z", ".tar", ".gz", ".lzh"],
    # プログラム・インストーラー
    "インストーラー": [".exe", ".msi", ".bat", ".ps1", ".cmd"],
    # コード
    "コード": [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".sh", ".java", ".cpp", ".c"],
    # フォント
    "フォント": [".ttf", ".otf", ".woff", ".woff2"],
}

# 整理しないもの（スキップ）
SKIP_NAMES = {
    "desktop.ini",
    "thumbs.db",
    ".ds_store",
}


def get_desktop_path() -> Path:
    """Windowsのデスクトップパスを取得"""
    return Path.home() / "Desktop"


def get_target_folder(file: Path) -> str | None:
    """ファイルの拡張子から移動先フォルダー名を返す"""
    ext = file.suffix.lower()
    for folder_name, extensions in RULES.items():
        if ext in extensions:
            return folder_name
    return "その他"  # どのルールにも一致しない場合


def organize(desktop: Path, dry_run: bool = False) -> None:
    moved = 0
    skipped = 0
    errors = 0

    print(f"\n{'[DRY RUN] ' if dry_run else ''}デスクトップを整理中: {desktop}\n")
    print("-" * 60)

    for item in sorted(desktop.iterdir()):
        # フォルダーはスキップ
        if item.is_dir():
            continue

        # スキップ対象ファイル
        if item.name.lower() in SKIP_NAMES:
            continue

        target_folder_name = get_target_folder(item)
        target_dir = desktop / target_folder_name

        # 移動先が自分自身の場合はスキップ（すでに整理済みフォルダーにいる場合）
        if item.parent == target_dir:
            skipped += 1
            continue

        target_path = target_dir / item.name

        # 同名ファイルが存在する場合はタイムスタンプを付加
        if target_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = item.stem
            suffix = item.suffix
            target_path = target_dir / f"{stem}_{timestamp}{suffix}"

        action = f"  {item.name}"
        arrow  = f"  → {target_folder_name}/"
        print(f"{action:<45} {arrow}")

        if not dry_run:
            try:
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(target_path))
                moved += 1
            except Exception as e:
                print(f"    ⚠️  エラー: {e}")
                errors += 1
        else:
            moved += 1

    print("-" * 60)
    label = "移動予定" if dry_run else "移動完了"
    print(f"\n✅ {label}: {moved} ファイル  ⏭️ スキップ: {skipped}  ❌ エラー: {errors}\n")

    if dry_run:
        print("※ --dry-run モードのため実際には移動していません。")
        print("   実際に整理するには: python organize_desktop.py\n")


def main():
    parser = argparse.ArgumentParser(description="デスクトップを自動整理します")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際には移動せず、何が起きるかを確認するだけ",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="デスクトップ以外のフォルダーを整理する場合にパスを指定",
    )
    args = parser.parse_args()

    desktop = Path(args.path) if args.path else get_desktop_path()

    if not desktop.exists():
        print(f"❌ フォルダーが見つかりません: {desktop}")
        return

    organize(desktop, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
