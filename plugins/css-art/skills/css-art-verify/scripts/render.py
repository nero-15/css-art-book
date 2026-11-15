#!/usr/bin/env python3
"""HTMLをヘッドレスのChromeで描画し、スクリーンショットを保存する。

使い方:
  python3 render.py art.html out.png --size 400
  python3 render.py art.html out.png --size 100 --density 2

絵を左上の角に置き、URLの ?size= を絵の大きさに反映するページを渡すこと
（SKILL.md の「検証用のページ」を参照）。左上から size×size を切り出して保存する。
Chrome の場所は自動で探す。見つからなければ環境変数 CHROME に実行ファイルのパスを入れる。
"""
import argparse
import os
import pathlib
import shutil
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow が必要です。`python3 -m pip install Pillow` で入れてから、もう一度実行してください。")

MAC_APPS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
COMMANDS = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]
TIMEOUT_SECONDS = 60
MIN_WINDOW = 600  # ヘッドレスのChromeは画面幅に下限があるので、広めに開いてから切り出す


def find_chrome():
    candidates = [os.environ.get("CHROME"), *MAC_APPS, *(shutil.which(name) for name in COMMANDS)]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    sys.exit(
        "Chrome が見つかりません。Chrome か Chromium を入れるか、"
        "環境変数 CHROME に実行ファイルのパスを入れてください。"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html")
    parser.add_argument("out")
    parser.add_argument("--size", type=int, default=400, help="絵の幅と高さ（CSSピクセル。既定: 400）")
    parser.add_argument("--density", type=float, default=1, help="画面密度（既定: 1）")
    args = parser.parse_args()

    page = pathlib.Path(args.html).resolve()
    if not page.is_file():
        sys.exit(f"HTMLが見つかりません: {page}")
    out = pathlib.Path(args.out).resolve()
    window = max(args.size, MIN_WINDOW)
    command = [
        find_chrome(), "--headless", "--disable-gpu", "--hide-scrollbars",
        f"--force-device-scale-factor={args.density}",
        f"--window-size={window},{window}",
        f"--screenshot={out}", f"{page.as_uri()}?size={args.size}",
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        sys.exit(f"描画が{TIMEOUT_SECONDS}秒で終わりませんでした: {page}")
    if result.returncode != 0 or not out.is_file():
        sys.exit(f"描画に失敗しました（終了コード {result.returncode}）:\n{result.stderr.strip()}")
    side = round(args.size * args.density)
    with Image.open(out) as shot:
        cropped = shot.crop((0, 0, side, side))
    cropped.save(out)
    print(f"描画しました: {out}（{args.size}×{args.size}、画面密度 {args.density:g}）")


if __name__ == "__main__":
    main()
