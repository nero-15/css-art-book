# 付録C 参考文献

章ごとの出典は各章の末尾にあります。ここでは、本書全体の土台になった資料を、読む優先度の高い順に挙げます。

## まず読むもの

| 資料 | 著者 | 何が得られるか |
|---|---|---|
| [Single Div Drawings with CSS](https://hacks.mozilla.org/2014/09/single-div-drawings-with-css/) | Lynn Fisher | 背景の重ねと影だけで描く基本 |
| [Advice for Complex CSS Illustrations](https://dev.to/jh3y/advice-for-complex-css-illustrations-2di0) | Jhey Tompkins | 下絵から積み上げる進め方 |
| [The Modern Guide For Making CSS Shapes](https://www.smashingmagazine.com/2024/05/modern-guide-making-css-shapes/) | Temani Afif | `clip-path` と `mask` による図形の総覧 |

## 技法を深めるもの

| 資料 | 著者・発行元 | 関連する章 |
|---|---|---|
| [Using CSS gradients](https://developer.mozilla.org/docs/Web/CSS/CSS_Images/Using_CSS_gradients) | MDN | 3章 |
| [box-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow) | MDN | 3章 |
| [Diana Smith's Top 5 CSS Properties She Uses to Produce CSS Art](https://css-tricks.com/diana-smiths-top-5-css-properties-she-uses-to-produce-css-art/) | CSS-Tricks | 3章 |
| [Use shape() for responsive clipping](https://developer.chrome.com/blog/css-shape) | Chrome for Developers | 4章、7章 |
| [mask-composite](https://developer.mozilla.org/docs/Web/CSS/mask-composite) | MDN | 4章 |
| [Trigonometric functions in CSS](https://web.dev/articles/css-trig-functions) | web.dev | 5章 |
| [Obsessing Over Smooth radial-gradient Disc Edges](https://frontendmasters.com/blog/obsessing-over-smooth-radial-gradient-disc-edges/) | Ana Tudor | 6章 |
| [@property: giving superpowers to CSS variables](https://web.dev/articles/at-property) | web.dev | 8章 |
| [How to create high-performance CSS animations](https://web.dev/articles/animations-guide) | web.dev | 8章 |
| [Beyond border-radius: the corner-shape property](https://www.smashingmagazine.com/2026/03/beyond-border-radius-css-corner-shape-property-ui/) | Smashing Magazine | 付録B |

## 実務で使うときに読むもの

| 資料 | 著者・発行元 | 関連する章 |
|---|---|---|
| [Creating Accessible CSS Art](https://alvaromontoro.com/blog/67979/creating-accessible-css-art) | Alvaro Montoro | 9章 |
| [forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors) | MDN | 9章 |
| [Non-text Contrast（WCAG 2.2 解説）](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | W3C | 9章 |
| [Visual comparisons](https://playwright.dev/docs/test-snapshots) | Playwright | 6章 |
| [How to Favicon: Six files that fit most needs](https://evilmartians.com/chronicles/how-to-favicon-in-six-files-that-fit-most-needs) | Evil Martians | 9章 |

## 論争を知るもの

| 資料 | 著者 | 立場 |
|---|---|---|
| [Wow, Mona Lisa with pure CSS!](https://lea.verou.me/2010/05/wow-mona-lisa-with-pure-css/) | Lea Verou | 批判。CSSの役割ではない |
| [The CSS Art Paradox](https://meiert.com/en/blog/the-css-art-paradox) | Jens Oliver Meiert | 批判。HTMLの質が犠牲になる |
| [CSS art? Pfft! Try SVG art!](https://dev.to/grahamthedev/css-art-pfft-try-svg-art-2o0n) | GrahamTheDev | 批判。SVGのほうが速く作れる |
| [CSS Art](https://www.oddbird.net/2020/12/08/css-art/) | Miriam Suzanne | 擁護。常に実用的である必要はない |
| [How Creating CSS Images Made Me a Better Developer](https://medium.com/coding-artist/how-creating-css-images-made-me-a-better-developer-25b7a79f1af6) | Eva Lettner | 擁護。学習効果 |

## 日本語の資料

| 資料 | 内容 |
|---|---|
| [CSSでロゴを描く（coosy）](https://coosy.co.jp/blog/css-coosy-logo/) | 角丸、枠線、疑似要素でロゴを組み立てる作例 |
| [CSSでドット絵（ponhiro）](https://ponhiro.com/css-dot-illust/) | `box-shadow` でドット絵を描く作例と生成ツールの紹介 |
| Lea Verou『CSSシークレット ―47のテクニックでCSSを自在に操る』（オライリー・ジャパン） | 図形を含むCSSの技法集 |

## 作品を見る

| 場所 | 内容 |
|---|---|
| [A Single Div](https://a.singlediv.com/) | Lynn Fisher の single-div 作品集 |
| [purecss-francine](https://github.com/cyanharlow/purecss-francine) | Diana Smith の作品とソース |
| [css-doodle](https://css-doodle.com/) | Yuan Chuan の生成ツールと作例 |
| [CSSBattle](https://cssbattle.dev/) | 短いコードで再現を競う |
| [100 Days CSS Challenge](https://100dayscss.com/) | 毎日のお題 |

## 資料の扱いについて

- 英語の資料は、筆者が要約して紹介しています。正確な表現は原文に当たってください
- ブラウザの対応状況は変わります。付録Bの数字は2026年11月時点のものです
- 性能に関する公開の計測値は、古いもの（2013年）しか見つかりませんでした。8章の「軽い・重い」は傾向であり、数値の裏付けはありません
