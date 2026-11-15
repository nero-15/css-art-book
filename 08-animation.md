# 8章 動かす

## この章でできるようになること

- 絵の一部を回す、点滅させる、形を変える
- グラデーションの角度や位置を、なめらかに動かす
- 動きが苦手な人に配慮する

CSSで描いた絵の強みは、部品がそのままアニメーションの対象になることです。画像と違い、あとから一部だけ動かせます。

## 最初に決めること: 何を動かすか

動かすプロパティによって、ブラウザの負担が大きく変わります。次の表の上にあるものほど軽く、下にあるものほど重くなります。

| 動かすもの | 負担 | 理由 |
|---|---|---|
| `transform`、`rotate`、`scale`、`translate`、`opacity` | 軽い | 描き直さず、出来上がった絵を動かすだけで済む |
| `clip-path`、グラデーションの値、`background-position` | 中 | 毎フレーム描き直す |
| `box-shadow`（特に大量の影やぼかし）、`filter` | 重い | 描き直しの量が多い |
| `width`、`top` などレイアウトに関わるもの | 重い | 配置の計算からやり直す |

**まず `transform` と `opacity` だけで実現できないか考えてください。** 回す、動かす、拡縮する、消す、の4つはこれで足ります。

## 8.1 回す

### 問題

破線リングをゆっくり回したい。

### 解決

```css
.spin {
  width: 100px; aspect-ratio: 1; border-radius: 50%;
  background: repeating-conic-gradient(var(--green) 0 20deg, #0000 20deg 30deg);
  animation: spin 8s linear infinite;
}
@keyframes spin { to { rotate: 1turn; } }
```

### 解説

`rotate` は `transform: rotate()` を単独のプロパティにしたものです。他の変形と別々に指定でき、アニメーションで上書きし合いません。

紋章の破線リングだけを回したいときは、リングを親の背景ではなく、別の箱（疑似要素か子要素）に分けます。背景の一部だけを `rotate` で回すことはできません。「動かす部品は箱を分ける」が原則です。

## 8.2 グラデーションを動かす

### 問題

円グラフのように、扇形がだんだん広がる動きを付けたい。

### 解決

動かしたい値を `@property` で登録し、その変数をアニメーションさせます。

```css
@property --sweep {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}
.sweep {
  width: 100px; aspect-ratio: 1; border-radius: 50%;
  background: conic-gradient(var(--red) var(--sweep), var(--cream) 0);
  animation: sweep 2s linear infinite;
}
@keyframes sweep { to { --sweep: 360deg; } }
```

### 解説

普通のCSS変数は、ブラウザから見るとただの文字列です。`0deg` と `360deg` の「間」が分からないので、なめらかに変化させられません。`@property` で「これは角度だ」と型を教えると、途中の値を計算できるようになります。

`syntax` を指定したら `initial-value` も必須です。型には `<angle>` のほか、`<percentage>`、`<length>`、`<color>`、`<number>` などが使えます。

グラデーションそのもの（`background`）は、なめらかに変化させられません。中で使う値を変数にして、変数のほうを動かします。`mask` に使うグラデーションも同じ方法で動かせます。

## 8.3 形を変える

### 問題

ひし形が正方形に変わる、といった形の変化を付けたい。

### 解決

頂点の数が同じ `polygon()` 同士なら、なめらかに変化します。

```css
.morph {
  width: 100px; aspect-ratio: 1; background: var(--green);
  clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%);
  animation: morph 1s ease-in-out infinite alternate;
}
@keyframes morph {
  to { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
}
```

### 解説

条件は、**頂点の数が同じ**であることです。数が違うと、途中経過なしでぱっと切り替わります。三角形から四角形へ変えたいときは、三角形のほうに頂点を1つ足して（同じ位置に2点置いて）数をそろえます。

対応する頂点同士が、書いた順に結ばれます。順番がずれていると、形がねじれながら変化します。意図しないねじれが出たら、開始点と回る向きをそろえてください。

`shape()` 同士も、命令の種類と数が同じなら変化します。

## 8.4 コマ送りにする

### 問題

なめらかにではなく、カチカチと段階的に動かしたい。ドット絵の点滅や、秒針の動きに使う。

### 解決

```css
.blink {
  animation: blink 1s steps(2, jump-none) infinite;
}
@keyframes blink { to { opacity: .2; } }
```

### 解説

`steps(n)` は、変化をn段階に分けます。`steps(60)` を60秒の回転に付ければ、1秒ごとに6度ずつ進む秒針になります。

2つ目の値は、段の取り方です。

| 値 | 動き |
|---|---|
| `jump-end`（既定） | 開始時は元の値のまま。最後の値には到達しない |
| `jump-start` | 開始と同時に1段目へ進む |
| `jump-none` | 最初の値と最後の値の両方を含む |
| `jump-both` | 最初と最後の両方で1段ずつ進む |

点滅のように「元の値」と「最後の値」を行き来させたいときは、`jump-none` を使います。

## 8.5 動きを減らす設定に対応する

### 問題

動きで気分が悪くなる人がいる。OSで「視差効果を減らす」を設定している人には、動きを控えたい。

### 解決

```css
@media (prefers-reduced-motion: reduce) {
  .spin, .sweep, .morph { animation: none; }
}
```

### 解説

すべての動きを消す必要はありません。問題になりやすいのは、大きく動くもの、回り続けるもの、点滅するものです。色がゆっくり変わる程度なら残して構いません。大きな動きを、フェードなど穏やかなものに差し替える方法もあります。

絵が「動いて初めて意味が分かる」作りになっている場合は、止まった状態でも意味が通じるように、最終形を初期状態にしておきます。

## 重くなったときの対処

| 症状 | 対処 |
|---|---|
| 動きがカクつく | 動かしているプロパティを確かめる。`transform` と `opacity` に置き換える |
| 大量の影を動かしている | 影そのものを動かさず、影を持つ箱ごと `transform` で動かす |
| ぼかした影の濃さを変えたい | 影を疑似要素に分け、`opacity` を動かす |
| 画面外の絵まで動いている | `content-visibility: auto` で、見えていない絵の描画を省く |

`will-change` は、問題が実際に起きてから、最後の手段として使います。予防のつもりで多くの要素に付けると、メモリを消費して逆に重くなります。

どの部分が描き直されているかは、Chromeの開発者ツールで確かめられます。Rendering タブの Paint flashing を有効にすると、描き直された領域が緑色に光ります。

## 次にやること

1. 1章のバッジの太陽を、`@property` で左から右へ動かす（`radial-gradient` の中心位置を変数にする）
2. 5章の円周配置（5.10）を、秒針つきの時計にする。針は中心に置いた細い箱を `rotate` で回す
3. 自分の絵に `prefers-reduced-motion` の対応を入れる

## 出典

- [How to create high-performance CSS animations（web.dev）](https://web.dev/articles/animations-guide)
- [@property: giving superpowers to CSS variables（web.dev）](https://web.dev/articles/at-property)
- [steps()（MDN）](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/steps)
- [prefers-reduced-motion（MDN）](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [will-change（MDN）](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change)
- [How to animate box-shadow（Tobias Ahlin）](https://tobiasahlin.com/blog/how-to-animate-box-shadow/)
