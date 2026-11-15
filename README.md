# CSSで絵を描く ― 座標から始める実践レシピ

画像もSVGも使わず、CSSだけで絵を描くための本の原稿です。1章1ファイルのMarkdownで、図は `images/` にあります。

## 目次

| ファイル | 章 | 型 |
|---|---|---|
| `00-preface.md` | はじめに | 案内 |
| `01-first-drawing.md` | 1章 まず1枚描く | チュートリアル |
| `02-design.md` | 2章 描く前に設計する | 手順 |
| `03-toolbox-box-gradient.md` | 3章 道具箱1: 箱・角丸・グラデーション・影 | 解説＋手順 |
| `04-toolbox-clip-mask.md` | 4章 道具箱2: 切り抜きとマスク | 解説＋手順 |
| `05-recipes.md` | 5章 レシピ集 | レシピ |
| `06-quality.md` | 6章 仕上げの質を上げる | レシピ |
| `07-project-emblem.md` | 7章 総合演習: 紋章を作り切る | チュートリアル |
| `08-animation.md` | 8章 動かす | レシピ |
| `09-production.md` | 9章 実務で使う | 判断基準＋レシピ |
| `10-troubleshooting.md` | 10章 困ったとき | リファレンス |
| `11-history.md` | 11章 先人たち | 読み物 |
| `appendix-a-checklist.md` | 付録A チェックリスト | リファレンス |
| `appendix-b-browser-support.md` | 付録B ブラウザ対応表 | リファレンス |
| `appendix-c-references.md` | 付録C 参考文献 | リファレンス |

## 図について

`images/` の図は、すべて本文に掲載したCSSをChrome 153で描画したスクリーンショットです。`jaggies.png` と `hairline.png` は、画面密度1倍で撮ったものを8倍に拡大しています。

## 製本する

Vivliostyle CLI を使う場合の設定例を `vivliostyle.config.js` に置いています。

```sh
npm install -D @vivliostyle/cli
npx vivliostyle build
```

## 検証の範囲

- コード例は Chrome 153 で描画して確認済み。Safari と Firefox では未確認
- ブラウザ対応の数字は、2026年11月時点の公開資料による

## ライセンス

- 文章と図: [CC BY 4.0](LICENSE)。出典を示せば、転載・改変・商用利用ができます
- 本文中のコード例と `vivliostyle.config.js`: [MIT License](LICENSE-CODE)

© 2026 nero15
