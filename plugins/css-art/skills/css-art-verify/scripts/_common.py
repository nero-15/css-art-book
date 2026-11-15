"""measure.py と diff.py が共有する、画像の読み込みと色分けの処理。"""
import sys
from collections import Counter

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow が必要です。`python3 -m pip install Pillow` で入れてから、もう一度実行してください。")

MIN_SHARE = 0.01      # これより面積の小さい色は、縁のにじみとして色の一覧に入れない
MERGE_DISTANCE = 48   # これより近い色は同じ色として扱う
BUCKET_BITS = 4       # 色を数えるときに、RGB各8ビットのうち何ビットを見るか


def parse_box(text, size):
    """'x0,y0,x1,y1' を4つの整数にする。None なら画像全体。"""
    if text is None:
        return (0, 0, size[0], size[1])
    try:
        x0, y0, x1, y1 = (int(v) for v in text.split(","))
    except ValueError:
        sys.exit(f"--box は x0,y0,x1,y1 の形で指定してください（受け取った値: {text}）")
    if not (0 <= x0 < x1 <= size[0] and 0 <= y0 < y1 <= size[1]):
        sys.exit(f"--box が画像の範囲（{size[0]}×{size[1]}）に収まっていません: {text}")
    return (x0, y0, x1, y1)


def load(path, box=None):
    """画像をRGBで読み、box があればその範囲に切り出す。"""
    try:
        image = Image.open(path).convert("RGB")
    except OSError as error:
        sys.exit(f"画像を読めません: {path}（{error}）")
    return image.crop(parse_box(box, image.size))


def _distance(a, b):
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5


def find_palette(image):
    """面積の大きい色を、多い順に [(rgb, 面積の割合)] で返す。"""
    shift = 8 - BUCKET_BITS
    pixels = list(image.getdata())
    buckets = Counter((r >> shift, g >> shift, b >> shift) for r, g, b in pixels)
    exact = Counter(pixels)
    total = len(pixels)
    palette = []
    for bucket, count in buckets.most_common():
        if count / total < MIN_SHARE:
            break
        members = [c for c in exact if (c[0] >> shift, c[1] >> shift, c[2] >> shift) == bucket]
        color = max(members, key=exact.__getitem__)
        near = next((i for i, (c, _) in enumerate(palette) if _distance(c, color) < MERGE_DISTANCE), None)
        if near is None:
            palette.append((color, count / total))
        else:
            palette[near] = (palette[near][0], palette[near][1] + count / total)
    return palette


def classify(image, colors):
    """各画素を、colors の中で最も近い色の番号にする。bytes（1画素1バイト）を返す。"""
    swatch = Image.new("P", (1, 1))
    flat = [v for color in colors for v in color]
    swatch.putpalette(flat + flat[:3] * (256 - len(colors)))
    return image.quantize(palette=swatch, dither=Image.Dither.NONE).tobytes()


def hex_color(color):
    return "#%02x%02x%02x" % color
