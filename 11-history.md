# 11章 先人たち

## この章について

手を動かす話は10章までで終わりです。この章は読み物として、CSSで絵を描く文化がどう育ってきたか、誰がどんな流儀で描いているかを紹介します。次に何を見て学べばいいか、の案内にもなります。

## 年表

| 年 | 出来事 |
|---|---|
| 2003年 | Dave Shea が CSS Zen Garden を公開。同じHTMLに、CSSだけで違うデザインを与える場 |
| 2010年 | David DeSandro が、角丸・グラデーション・影でブラウザのロゴを再現する記事を公開 |
| 2010年 | Nicolas Gallagher が、疑似要素を使った84個のアイコンを公開 |
| 2010年 | Lea Verou が、CSSで絵を描く流行を批判する記事を公開 |
| 2014年 | Lynn Fisher が A Single Div を開始 |
| 2017年 | Yuan Chuan が css-doodle を公開 |
| 2018年 | Diana Smith の Pure CSS Francine が話題になり、一般のメディアでも報じられる |
| 2019年 | CSSBattle が公開される |
| 2020年ごろ | 10月に毎日1枚描く催し Divtober が行われるようになる |

2010年前後に、CSS3で角丸・グラデーション・影が使えるようになり、「画像なしでどこまで描けるか」の試みが一気に増えました。同じ年に批判も出ている点が興味深いところです。この論争は今も続いています（9章）。

Divtober がいつ始まったかは、確かな記録を見つけられませんでした。2020年10月に Lynn Fisher の投稿があること、2021年は Fisher の主催だと参加者が書いていることまでは確認できています。

## 作り手と流儀

### Lynn Fisher — 要素1つで描く

A Single Div の作者です。`div` 1つと、その `::before`、`::after` の3つの箱だけで絵を描きます。使うのは、背景のグラデーションの重ねと、影の複製です。

きっかけは、2013年のカンファレンスで聞いた講演だったと本人が書いています。動機として、美術学校の「三原色だけで色を作る」課題を挙げています。制約があると、手持ちの道具を見直すことになる、という考え方です。

本書の7章で扱った single-div は、この流儀です。

### Diana Smith — 手書きで絵画を描く

Pure CSS Francine は、18世紀の油彩画のような肖像を、HTMLとCSSだけで描いた作品です。自分に課したルールは、すべて手で入力すること、使う道具はテキストエディタとブラウザの開発者ツールだけ、の2つです。

よく使うプロパティとして、`border-radius`、`box-shadow`、`transform`、グラデーション、`overflow` の5つを挙げています。本書の3章で扱った道具です。8値の角丸を持つ箱を大量に重ね、ぼかした影で陰影を付けます。

作品はChrome向けに作られていて、他のブラウザや古いブラウザでは崩れます。古いブラウザで開くと抽象画のようになることが話題になりました。

### Temani Afif — 図形を体系化する

`clip-path`、`mask`、グラデーションを使って、要素1つで図形を作る方法を大量に公開しています。本書の4章と5章の内容は、この人の解説に多くを負っています。

実用寄りの立場で、図形の作り方を解説しつつ、SVGが使えるならSVGを使うよう勧めています。

### Ana Tudor — 数学で描く

三角関数や3次元の変形を使った、数学的な作品で知られます。6章で紹介した「円の縁のギザギザを消す」方法は、この人の検証記事によるものです。

### Jhey Tompkins — 手順を言葉にする

複雑なCSSイラストの進め方を記事にまとめています。下絵をなぞる、絶対配置を使う、大きな形から積む、変数で拡縮できるようにする、といった内容です。本書の2章の工程と重なります。

### Ben Evans — 3次元と空間

CSSだけで3次元の迷路や空間を作っています。CSSで描く理由について、紙や図形ソフトを用意するより、開いているエディタで描くほうが手軽だった、と語っています。重い影を避ける、見えない要素を省く、といった性能上の工夫も公開しています。

### Yuan Chuan — 生成する

css-doodle は、格子状に並べたセルに、乱数で変化を付けたCSSを当てる道具です。手で1つずつ描くのではなく、規則から模様を生成します。

### Alvaro Montoro — アクセシビリティを言う

Divtober の常連です。CSSで描いた絵は、そのままでは読み上げソフトに伝わらない、という問題を取り上げ、対応方法を記事にしています。本書の9章の内容です。

## 腕試しの場

| 場 | 内容 |
|---|---|
| CSSBattle | お題の画像を、できるだけ短いコードで再現する。一致度と文字数で採点 |
| Divtober | 10月の毎日、お題に沿って要素1つで描く |
| 100 Days CSS Challenge | 100日間、毎日1つ作る |
| CodePen | 作品を公開する場。上の催しの作品も、多くはここに置かれる |

CSSBattle は、文字数を削る競技です。採点はまず一致度が効き、100%一致してからは文字数が少ないほど点が伸びます。実務とは違う書き方になることを、作者自身が認めています。プロパティの省略記法や既定値に詳しくなる、という学習効果はあります。

始めるなら、Divtober のお題を1つ借りて、single-div で描いてみるのを勧めます。制約が強いので、かえって迷いません。

## 次に読むもの

| 資料 | 内容 | 本書との関係 |
|---|---|---|
| Lynn Fisher「Single Div Drawings with CSS」 | single-div の基本技法 | 3章、7章の原典 |
| Jhey Tompkins「Advice for Complex CSS Illustrations」 | 複雑な絵の進め方 | 2章と同じ主題 |
| Temani Afif「The Modern Guide For Making CSS Shapes」 | 図形の作り方の総覧 | 4章、5章の発展 |
| Ana Tudor「Obsessing Over Smooth radial-gradient Disc Edges」 | 縁の品質の徹底検証 | 6章の原典 |
| Alvaro Montoro「Creating Accessible CSS Art」 | アクセシビリティ対応 | 9章の原典 |
| Lea Verou『CSSシークレット』（オライリー・ジャパン） | 図形を含むCSSの技法集 | 3〜5章の背景知識 |

日本語で、CSSで絵を描くことを主題にした書籍や定番の記事は、筆者の調べた範囲では見つかりませんでした。個別の作例記事（参考にした2本を付録Cに挙げています）はありますが、体系的な資料は英語が中心です。

## 出典

- [CSS Zen Garden（Dave Shea）](https://daveshea.com/projects/zen)
- [Opera Logo with CSS（David DeSandro）](https://v2.desandro.com/articles/opera-logo-css)
- [Pure CSS GUI icons（Nicolas Gallagher）](https://nicolasgallagher.com/pure-css-gui-icons/)
- [Wow, Mona Lisa with pure CSS!（Lea Verou）](https://lea.verou.me/2010/05/wow-mona-lisa-with-pure-css/)
- [Single Div Drawings with CSS（Lynn Fisher, Mozilla Hacks）](https://hacks.mozilla.org/2014/09/single-div-drawings-with-css/)
- [Community highlight: Lynn Fisher（web.dev）](https://web.dev/community-highlight-lynn-fisher/)
- [purecss-francine（Diana Smith, GitHub）](https://github.com/cyanharlow/purecss-francine)
- [Diana Smith's Top 5 CSS Properties She Uses to Produce CSS Art（CSS-Tricks）](https://css-tricks.com/diana-smiths-top-5-css-properties-she-uses-to-produce-css-art/)
- [Diana Smith と Pure CSS Francine を紹介する記事（Vice, 2018年）](https://www.vice.com/en/article/painting-made-with-code-html-pure-css-browser-art-diana-smith)
- [Interview with Ben Evans（Alvaro Montoro, DEV）](https://dev.to/alvaromontoro/interview-with-ben-evans-3o3b)
- [Advice for Complex CSS Illustrations（Jhey Tompkins, DEV）](https://dev.to/jh3y/advice-for-complex-css-illustrations-2di0)
- [css-doodle](https://css-doodle.com/)
- [CSSBattle FAQs](https://cssbattle.dev/faqs)
- [Introducing CSSBattle（freeCodeCamp）](https://www.freecodecamp.org/news/introducing-cssbattle-the-first-css-code-golfing-game-88b7518df618/)
- [My Divtober 2021 drawings（Alvaro Montoro）](https://alvaromontoro.com/blog/67991/my-divtober-2021-drawings)
- [100 Days CSS Challenge](https://100dayscss.com/)
