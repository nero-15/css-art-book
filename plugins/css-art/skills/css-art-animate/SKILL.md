---
name: css-art-animate
description: CSSで描いた絵を動かす。何を動かすかの決め方、回転、グラデーションの値のアニメーション、形の変化、コマ送り、動きを減らす設定への対応、重くなったときの対処を扱う。絵の一部を回す・点滅させる・形を変える・扇形を広げるといった動きを付けるときに使う。Keywords: css art, animation, rotate, @property, conic-gradient sweep, clip-path morph, steps(), prefers-reduced-motion, will-change, performance
---

# CSSで描いた絵を動かす

CSSで描いた絵の強みは、部品がそのままアニメーションの対象になることです。画像と違い、あとから一部だけ動かせます。絵そのものの描き方は `css-art-draw` を使ってください。

用語:

- **箱**: 1つの要素、または疑似要素が占める長方形
- **部品**: 絵を構成する1つの形

コード例の色は、次の変数を前提にしています。

```css
:root { --green: #0f3d2e; --cream: #f4ecd8; --red: #e4572e; }
```

## 進め方

1. 何を動かすかを決める（次の節の表で、負担を確かめる）
2. 動かす部品を、別の箱に分ける
3. 動きの種類に合う節の書き方を使う（回す / グラデーションを動かす / 形を変える / コマ送り）
4. `prefers-reduced-motion` の対応を入れる
5. カクつくなら「重くなったときの対処」を当たる

## 最初に決めること: 何を動かすか

動かすプロパティによって、ブラウザの負担が大きく変わります。次の表の上にあるものほど軽く、下にあるものほど重くなります。

| 動かすもの | 負担 | 理由 |
|---|---|---|
| `transform`、`rotate`、`scale`、`translate`、`opacity` | 軽い | 描き直さず、出来上がった絵を動かすだけで済む |
| `clip-path`、グラデーションの値、`background-position` | 中 | 毎フレーム描き直す |
| `box-shadow`（特に大量の影やぼかし）、`filter` | 重い | 描き直しの量が多い |
| `width`、`top` などレイアウトに関わるもの | 重い | 配置の計算からやり直す |

**まず `transform` と `opacity` だけで実現できないか考えてください。** 回す、動かす、拡縮する、消す、の4つはこれで足ります。

## 1. 回す

例: 破線リングをゆっくり回す。

```css
.spin {
  width: 100px; aspect-ratio: 1; border-radius: 50%;
  background: repeating-conic-gradient(var(--green) 0 20deg, #0000 20deg 30deg);
  animation: spin 8s linear infinite;
}
@keyframes spin { to { rotate: 1turn; } }
```

- `rotate` は `transform: rotate()` を単独のプロパティにしたものです。他の変形と別々に指定でき、アニメーションで上書きし合いません
- 絵の中のリングだけを回したいときは、リングを親の背景ではなく、別の箱（疑似要素か子要素）に分けます。背景の一部だけを `rotate` で回すことはできません

**原則: 動かす部品は箱を分ける。**

## 2. グラデーションを動かす

例: 円グラフのように、扇形がだんだん広がる。

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

- 普通のCSS変数は、ブラウザから見るとただの文字列です。`0deg` と `360deg` の「間」が分からないので、なめらかに変化させられません。`@property` で「これは角度だ」と型を教えると、途中の値を計算できるようになります
- `syntax` を指定したら `initial-value` も必須です
- 型には `<angle>` のほか、`<percentage>`、`<length>`、`<color>`、`<number>` などが使えます
- グラデーションそのもの（`background`）は、なめらかに変化させられません。中で使う値を変数にして、変数のほうを動かします
- `mask` に使うグラデーションも同じ方法で動かせます
- `@property` は全主要ブラウザで使えます（2024年7月〜。2026年11月時点）

## 3. 形を変える

例: ひし形が正方形に変わる。

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

- 条件は、**頂点の数が同じ**であることです。数が違うと、途中経過なしでぱっと切り替わります
- 三角形から四角形へ変えたいときは、三角形のほうに頂点を1つ足して（同じ位置に2点置いて）数をそろえます
- 対応する頂点同士が、書いた順に結ばれます。順番がずれていると、形がねじれながら変化します。意図しないねじれが出たら、開始点と回る向きをそろえてください
- `shape()` 同士も、命令の種類と数が同じなら変化します

## 4. コマ送りにする

例: なめらかにではなく、カチカチと段階的に動かす。ドット絵の点滅や、秒針の動きに使う。

```css
.blink {
  animation: blink 1s steps(2, jump-none) infinite;
}
@keyframes blink { to { opacity: .2; } }
```

`steps(n)` は、変化をn段階に分けます。`steps(60)` を60秒の回転に付ければ、1秒ごとに6度ずつ進む秒針になります。

2つ目の値は、段の取り方です。

| 値 | 動き |
|---|---|
| `jump-end`（既定） | 開始時は元の値のまま。最後の値には到達しない |
| `jump-start` | 開始と同時に1段目へ進む |
| `jump-none` | 最初の値と最後の値の両方を含む |
| `jump-both` | 最初と最後の両方で1段ずつ進む |

点滅のように「元の値」と「最後の値」を行き来させたいときは、`jump-none` を使います。

## 5. 動きを減らす設定に対応する

動きで気分が悪くなる人がいます。OSで「視差効果を減らす」を設定している人には、動きを控えます。動きを付けたら、必ずこの対応を入れてください。

```css
@media (prefers-reduced-motion: reduce) {
  .spin, .sweep, .morph { animation: none; }
}
```

- すべての動きを消す必要はありません。問題になりやすいのは、大きく動くもの、回り続けるもの、点滅するものです
- 色がゆっくり変わる程度なら残して構いません
- 大きな動きを、フェードなど穏やかなものに差し替える方法もあります
- 絵が「動いて初めて意味が分かる」作りになっている場合は、止まった状態でも意味が通じるように、最終形を初期状態にしておきます

## 重くなったときの対処

| 症状 | 対処 |
|---|---|
| 動きがカクつく | 動かしているプロパティを確かめる。`transform` と `opacity` に置き換える |
| 大量の影を動かしている | 影そのものを動かさず、影を持つ箱ごと `transform` で動かす |
| ぼかした影の濃さを変えたい | 影を疑似要素に分け、`opacity` を動かす |
| 画面外の絵まで動いている | `content-visibility: auto` で、見えていない絵の描画を省く |

`will-change` は、問題が実際に起きてから、最後の手段として使います。予防のつもりで多くの要素に付けると、メモリを消費して逆に重くなります。

どの部分が描き直されているかは、Chromeの開発者ツールで確かめられます。Rendering タブの Paint flashing を有効にすると、描き直された領域が緑色に光ります。

## 動きがおかしいときの早見表

| 症状 | 原因 | 直し方 |
|---|---|---|
| グラデーションがぱっと切り替わる | 背景は途中の値を計算できない | 値を `@property` で登録した変数にする |
| 形がぱっと切り替わる | 頂点の数が違う | 頂点の数をそろえる |
| 形がねじれながら変わる | 頂点の対応がずれている | 開始点と回る向きをそろえる |
| カクつく | 重いプロパティを動かしている | `transform` と `opacity` に置き換える |
| 背景の一部だけ回せない | 背景は箱と一体 | 動かす部品を別の箱に分ける |

## 応用の例

- 太陽を左から右へ動かす: `radial-gradient` の中心位置を変数にし、`@property` で登録して動かす
- 秒針つきの時計: 針は中心に置いた細い箱を `rotate` で回す。`steps(60)` を60秒の回転に付ける

## このスキルの前提

コード例はChrome 153で描画して確かめたものです。SafariとFirefoxでは確認していません。

## 関連スキル

- `css-art-draw`: 絵そのものの描き方
- `css-art-troubleshoot`: 動き以外の不具合を症状から引く
- `css-art-production`: 公開前のチェック（`prefers-reduced-motion` の対応を含む）

出典: 『CSSで絵を描く』8章、10章
