#!/usr/bin/env python3
"""下絵の画像を測り、100×100の方眼の単位で「どの色がどこからどこまでか」を出す。

使い方:
  python3 measure.py 下絵.png                     # 色の一覧と、絵の範囲の候補を出す
  python3 measure.py 下絵.png --box 2,6,502,506   # 絵の範囲を決めて、行ごとに測る
  python3 measure.py 下絵.png --box ... --columns # 列ごと（縦方向）に測る
"""
import argparse

from _common import classify, find_palette, hex_color, load

MIN_RUN = 0.6  # 方眼の単位。これより短い区間は縁のにじみとして出さない


def runs(row):
    """同じ色が続く区間を (色番号, 開始, 終了) の並びにする。"""
    out, start = [], 0
    for i in range(1, len(row) + 1):
        if i == len(row) or row[i] != row[start]:
            out.append((row[start], start, i))
            start = i
    return out


def content_box(indexes, width, height, background):
    """背景色ではない画素を囲む範囲。絵の範囲の候補として出す。"""
    xs = [i % width for i, v in enumerate(indexes) if v != background]
    ys = [i // width for i, v in enumerate(indexes) if v != background]
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1) if xs else (0, 0, width, height)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("image")
    parser.add_argument("--box", help="絵の範囲 x0,y0,x1,y1（画素）。方眼の (0,0)〜(100,100) に当たる")
    parser.add_argument("--step", type=float, default=2, help="何単位おきに測るか（既定: 2）")
    parser.add_argument("--columns", action="store_true", help="行ではなく列を測る")
    args = parser.parse_args()

    image = load(args.image, args.box)
    width, height = image.size
    palette = find_palette(image)
    colors = [color for color, _ in palette]
    indexes = classify(image, colors)

    print(f"大きさ: {width}×{height}")
    print("色（面積の多い順）:")
    for letter, (color, share) in zip("ABCDEFGHIJ", palette):
        print(f"  {letter} {hex_color(color)} {share * 100:.1f}%")
    if args.box is None:
        corner = indexes[0]
        box = content_box(indexes, width, height, corner)
        print(f"絵の範囲の候補（左上の角の色を背景と見た場合）: --box {','.join(map(str, box))}")
        print("範囲が正方形でない、または絵が画像の端で切れている場合は、手で直してから --box を付けて実行してください。")
        return

    across, along = (height, width) if args.columns else (width, height)
    axis, other = ("x", "y") if args.columns else ("y", "x")
    print(f"\n{axis} ごとの区間（{other} の値。単位は方眼）:")
    position = 0.0
    while position <= 100:
        line = min(int(position / 100 * along), along - 1)
        row = indexes[line::width][:height] if args.columns else indexes[line * width:(line + 1) * width]
        parts = [
            f"{'ABCDEFGHIJ'[c]} {a / across * 100:.1f}-{b / across * 100:.1f}"
            for c, a, b in runs(row)
            if (b - a) / across * 100 >= MIN_RUN
        ]
        print(f"  {axis}={position:g}: " + "  ".join(parts))
        position += args.step


if __name__ == "__main__":
    main()
