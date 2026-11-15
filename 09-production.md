# 9章 実務で使う

## この章でできるようになること

- CSS、SVG、canvas、画像のどれで描くべきか判断する
- CSSで描いた絵を、読み上げソフトやハイコントラスト表示に対応させる
- 描いた絵を画像ファイルにして、ファビコンなどに使う

ここまでは「描けるか」の話でした。この章は「使っていいか」の話です。

## 9.1 CSSで描くべきか

### 結論

**ロゴ、アイコン、イラストを本番サイトに置くなら、まずSVGを検討してください。** CSSで描くのは、次のどれかに当てはまるときです。

- すでにある要素への装飾である（ボタンの切り欠き、区切りの模様、背景のパターン）
- 状態やテーマに合わせて、色・大きさ・動きを細かく変えたい
- 画像ファイルを増やしたくない、ごく単純な図形である
- 学習や作品づくりが目的である

これはCSSアートの作り手自身も認めていることです。CSS図形の解説で知られる Temani Afif は、自分の解説記事の中で「使えるならSVGを使え」と書いています。

### 4つの手段の比較

| 観点 | CSS | SVG | canvas | 画像（PNG等） |
|---|---|---|---|---|
| 拡縮 | 作り方次第 | 劣化しない | 画面密度への対応が要る | 拡大でぼやける |
| 複雑な曲線 | 苦手 | 得意 | 得意 | 何でも可 |
| 図形ソフトで編集 | できない | できる | できない | できる |
| 一部だけ動かす | 得意 | 得意 | 自分で実装 | できない |
| テーマで色を変える | 得意 | できる | 自分で実装 | 作り直し |
| 読み上げ対応 | 追加の記述が要る | 仕組みがある | 代替文のみ | `alt` |
| 大量の図形 | 重くなる | 重くなる | 得意 | 関係なし |

### 判断の手順

1. 写真や、色数の多い複雑な絵 → **画像**
2. 数千個の図形、ゲーム、毎フレーム描き直す表現 → **canvas**
3. ロゴ、アイコン、図形ソフトで作ったイラスト → **SVG**
4. 既存の要素の装飾、単純な図形、テーマ連動 → **CSS**

### CSSで描くことへの批判

CSSで絵を描くことには、昔から批判があります。主な論点は次の3つです。

| 批判 | 内容 |
|---|---|
| 役割が違う | CSSは文書やUIの見た目を整えるもので、絵を描く道具ではない |
| HTMLが汚れる | 絵のために、意味のない空の `div` が大量に増える |
| 手間がかかる | 同じ絵がSVGなら数分の1の時間で作れる |

どれも正当な指摘です。本書の立場は、**学習と装飾には価値があり、本番のイラストには向かない**、です。HTMLが汚れる問題は、single-div（7章）なら避けられます。

学習上の価値については、多くの作り手が同じことを言っています。CSSで絵を描くと、普段使わないプロパティの挙動が身につき、UIの実装が速くなる、というものです。

## 9.2 読み上げソフトに対応する

### 問題

CSSで描いた絵は、中身が空の `div` です。読み上げソフトには何も伝わりません。

### 解決

意味のある絵には、役割と名前を付けます。

```html
<div class="n15 single" role="img" aria-label="N15 の紋章"></div>
```

飾りでしかない絵は、読み上げから隠します。

```html
<div class="pattern" aria-hidden="true"></div>
```

### 解説

`role="img"` を付けると、読み上げソフトはその要素を1枚の画像として扱い、`aria-label` の文を読みます。中に子要素があっても、個別には読まれません。

どちらにするかは、「その絵が無くなったら、情報が欠けるか」で決めます。欠けるなら `role="img"`、欠けないなら隠します。

## 9.3 ハイコントラスト表示に対応する

### 問題

Windowsのハイコントラストモード（強制カラー）では、CSSで描いた絵がほぼ消える。

### 解決

強制カラーのときだけ、枠線で輪郭を出します。

```css
@media (forced-colors: active) {
  .n15 {
    border: 2px solid CanvasText;   /* システムの文字色 */
  }
}
```

絵そのものを残したい場合は、色の強制を解除します。

```css
.n15, .n15::before, .n15::after {
  forced-color-adjust: none;
}
```

### 解説

強制カラーでは、ブラウザが色を上書きします。絵に関わる部分では次のことが起きます。

| プロパティ | 強制カラーでの扱い |
|---|---|
| `background-color` | システムの色に置き換わる |
| グラデーションの背景 | 消える |
| `box-shadow` | 消える |
| `border-color` | システムの色に置き換わる（枠線自体は残る） |

グラデーションと影で描いた絵は、何も残りません。枠線だけは残るので、輪郭を枠線で示すのが基本の対策です。

`forced-color-adjust: none` は、ロゴのように色そのものに意味がある場合に限って使います。乱用すると、ハイコントラストを必要とする人の設定を無視することになります。

Chromeの開発者ツールでは、Rendering タブで forced-colors のエミュレーションを有効にすると確認できます。

## 9.4 描いた絵を画像にする

### 問題

CSSで描いた紋章を、ファビコンやSNSの共有画像に使いたい。これらは画像ファイルでないと指定できない。

### 解決

実際のブラウザで描画し、要素だけをスクリーンショットに撮ります。

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=2)
    page.goto("file:///path/to/emblem.html")
    page.locator(".n15").screenshot(path="emblem.png", omit_background=True)
    browser.close()
```

### 解説

`omit_background=True` で、ページの背景を透明にできます。ページ側で `body` に背景色を指定していると透明にならないので、撮影用のページでは背景を指定しないでください。

ブラウザ上でDOMを画像に変換するライブラリ（html-to-image など）もあります。ただし、内部でSVGに包み直して描画する仕組みのため、`mask` や新しい機能が再現されないことがあります。確実なのは、ブラウザそのものに撮らせる方法です。

ファビコンに必要な大きさの目安は次のとおりです。

| ファイル | 大きさ | 用途 |
|---|---|---|
| `favicon.ico` | 32×32 | 古いブラウザ、タブ |
| `apple-touch-icon.png` | 180×180 | iPhoneのホーム画面 |
| manifest用 PNG | 192×192、512×512 | Androidのホーム画面 |

小さいサイズでは、細い線や破線がつぶれます。32pxで撮ってみて読めなければ、ファビコン用に細部を省いた版を作ってください。7章の紋章なら、破線リングを省き、文字を太くします。

## 9.5 canvasで同じ絵を描く

### 問題

同じ絵をcanvasでも使いたい。ゲームや、画像として書き出す処理の中で必要になった。

### 解決

2章の座標表は、canvasでもそのまま使えます。

```js
const N = [[17,72],[17,28],[25,28],[38,56.6],[38,28],
           [45,28],[45,72],[37,72],[24,43.4],[24,72]];

function draw(canvas, size) {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = canvas.height = Math.round(size * dpr);   // 内部の解像度
  canvas.style.width = canvas.style.height = size + "px";  // 表示の大きさ
  const g = canvas.getContext("2d");
  g.setTransform(canvas.width / 100, 0, 0, canvas.width / 100, 0, 0);  // 100×100の座標系に

  g.fillStyle = "#0f3d2e";
  g.beginPath(); g.arc(50, 50, 50, 0, Math.PI * 2); g.fill();

  const path = new Path2D();
  N.forEach(([x, y], i) => i ? path.lineTo(x, y) : path.moveTo(x, y));
  path.closePath();
  g.fillStyle = "#f4ecd8";
  g.fill(path);
}
```

### 解説

要点は2つです。

**内部の解像度を画面密度倍にする。** canvasは、何もしないと高密度の画面でぼやけます。`width` と `height` の属性を画面密度倍にし、CSSで表示の大きさを戻します。

**座標系を100×100にそろえる。** `setTransform` で拡大率をかけておけば、CSSの `%` と同じ数字で描けます。CSS版とcanvas版で、座標表を共有できます。

角度の向きには注意が要ります。CSSの `conic-gradient` は真上が0度で時計回り、canvasの `arc` は右が0度で時計回りです。CSSの角度から90度引くと、canvasの角度になります。

## 本番投入前のチェックリスト

- [ ] この絵はSVGや画像にすべきではないか、9.1の手順で確かめた
- [ ] 意味のある絵に `role="img"` と `aria-label` を付けた
- [ ] 飾りの絵に `aria-hidden="true"` を付けた
- [ ] 強制カラーで、必要な輪郭が残る
- [ ] 動きに `prefers-reduced-motion` の対応を入れた（8章）
- [ ] 3つのブラウザエンジンで確かめた（6章）
- [ ] 絵のための空要素を、必要最小限にした

## 次にやること

1. 自分のサイトで、画像にしている単純な図形を1つ探し、9.1の手順でCSSに置き換える価値があるか判断する
2. 7章の紋章に `role="img"` を付け、開発者ツールのアクセシビリティ表示で名前が出るか確かめる
3. 紋章を32pxで撮影し、ファビコンとして読めるか見る

## 出典

- [When to Use SVG vs. When to Use Canvas（CSS-Tricks）](https://css-tricks.com/?p=297707)
- [The Modern Guide For Making CSS Shapes（Temani Afif, Smashing Magazine）](https://www.smashingmagazine.com/2024/05/modern-guide-making-css-shapes/)
- [Wow, Mona Lisa with pure CSS!（Lea Verou）](https://lea.verou.me/2010/05/wow-mona-lisa-with-pure-css/)
- [The CSS Art Paradox（Jens Oliver Meiert）](https://meiert.com/en/blog/the-css-art-paradox)
- [CSS art? Pfft! Try SVG art!（GrahamTheDev）](https://dev.to/grahamthedev/css-art-pfft-try-svg-art-2o0n)
- [Creating Accessible CSS Art（Alvaro Montoro）](https://alvaromontoro.com/blog/67979/creating-accessible-css-art)
- [ARIA: img role（MDN）](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/img_role)
- [forced-colors（MDN）](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors)
- [How to Favicon: Six files that fit most needs（Evil Martians）](https://evilmartians.com/chronicles/how-to-favicon-in-six-files-that-fit-most-needs)
- [Optimizing canvas（MDN）](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas)
