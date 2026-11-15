#!/usr/bin/env python3
"""下絵と描画結果を画素ごとに突き合わせ、食い違いの割合と場所を出す。

使い方:
  python3 diff.py 下絵.png 描画.png --box 2,6,502,506 --out diff.png

- 下絵の色の一覧（面積の大きい色）に両方の画像を寄せ、色が違う画素を数える
- 下絵の色の境目（縁のにじみ）は数えない（--edge で幅を変える）
- 10×10 のマスごとの食い違いを出す。数字が大きいマスの部品から直す
- 差分画像は、食い違った画素が赤。それ以外は下絵を薄くしたもの
- 合格なら終了コード 0、不合格なら 1
"""
import argparse
import sys

from _common import classify, find_palette, load

from PIL import Image

CELLS = 10        # マスの数（縦横）
SEARCH_STRIDE = 3  # 位置合わせのときは、この間隔で間引いて数える


def edge_mask(indexes, width, height, reach):
    """下絵の色の境目から reach 画素以内を True にする。"""
    edge = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            i = y * width + x
            if (x + 1 < width and indexes[i] != indexes[i + 1]) or (y + 1 < height and indexes[i] != indexes[i + width]):
                for yy in range(max(0, y - reach + 1), min(height, y + reach + 1)):
                    for xx in range(max(0, x - reach + 1), min(width, x + reach + 1)):
                        edge[yy * width + xx] = 1
    return edge


def mismatches(ref, out, edge, width, height, dx, dy, stride=1):
    """描画結果を (dx, dy) ずらしたときに食い違う画素の位置と、比べた画素の数。"""
    bad, compared = [], 0
    for y in range(max(0, dy), min(height, height + dy), stride):
        for x in range(max(0, dx), min(width, width + dx), stride):
            i = y * width + x
            if edge[i]:
                continue
            compared += 1
            if ref[i] != out[(y - dy) * width + (x - dx)]:
                bad.append(i)
    return bad, compared


def best_shift(ref, out, edge, width, height, reach):
    """±reach 画素の範囲で、食い違いが最も少ないずらし方を探す。"""
    shifts = [(dx, dy) for dy in range(-reach, reach + 1) for dx in range(-reach, reach + 1)]
    return min(shifts, key=lambda s: len(mismatches(ref, out, edge, width, height, *s, SEARCH_STRIDE)[0]))


def save_diff(reference, bad, path):
    faded = Image.eval(reference, lambda v: v // 2 + 110)
    pixels = faded.load()
    width = reference.size[0]
    for i in bad:
        pixels[i % width, i // width] = (255, 0, 0)
    faded.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference")
    parser.add_argument("render")
    parser.add_argument("--box", help="下絵の中の絵の範囲 x0,y0,x1,y1（measure.py と同じ値）")
    parser.add_argument("--out", default="diff.png", help="差分画像の保存先（既定: diff.png）")
    parser.add_argument("--edge", type=int, default=1, help="色の境目から何画素を数えないか（既定: 1）")
    parser.add_argument("--shift", type=int, default=2, help="位置合わせで試すずれの幅（画素。既定: 2）")
    parser.add_argument("--pass-total", type=float, default=0.5, help="全体の食い違いの上限（%%。既定: 0.5）")
    parser.add_argument("--pass-cell", type=float, default=3.0, help="1マスの食い違いの上限（%%。既定: 3）")
    args = parser.parse_args()

    reference = load(args.reference, args.box)
    width, height = reference.size
    render = load(args.render)
    if render.size[0] < width:
        print(f"注意: 描画（{render.size[0]}px）が下絵（{width}px）より小さいので、拡大のにじみが食い違いに入ります。"
              "判定には下絵以上の大きさで描画したものを使ってください。")
    render = render.resize((width, height), Image.Resampling.LANCZOS)
    colors = [color for color, _ in find_palette(reference)]
    ref, out = classify(reference, colors), classify(render, colors)
    edge = edge_mask(ref, width, height, args.edge)

    dx, dy = best_shift(ref, out, edge, width, height, args.shift)
    bad, compared = mismatches(ref, out, edge, width, height, dx, dy)
    total = len(bad) / compared * 100

    cell_bad = [[0] * CELLS for _ in range(CELLS)]
    for i in bad:
        cell_bad[min(i // width * CELLS // height, CELLS - 1)][min(i % width * CELLS // width, CELLS - 1)] += 1
    cell_area = (width / CELLS) * (height / CELLS)
    cells = sorted(
        ((count / cell_area * 100, col, row) for row, line in enumerate(cell_bad) for col, count in enumerate(line) if count),
        reverse=True,
    )
    worst = cells[0][0] if cells else 0.0

    save_diff(reference, bad, args.out)
    print(f"食い違い: {total:.2f}%（{len(bad)} / {compared} 画素。位置合わせ dx={dx}, dy={dy}）")
    if abs(dx) == args.shift or abs(dy) == args.shift:
        print("注意: 位置合わせが探す範囲の端です。--box が絵の範囲と合っているか確かめてください。")
    print("食い違いの多いマス（方眼の範囲、マスの面積に対する割合）:")
    for share, col, row in cells[:8]:
        print(f"  x {col * 10}-{col * 10 + 10}, y {row * 10}-{row * 10 + 10}: {share:.1f}%")
    print(f"差分画像: {args.out}")
    passed = total <= args.pass_total and worst <= args.pass_cell
    print("判定: 合格" if passed else f"判定: 不合格（上限は全体 {args.pass_total}%、1マス {args.pass_cell}%）")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
