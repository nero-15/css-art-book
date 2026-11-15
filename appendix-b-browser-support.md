# 付録B ブラウザ対応表

2026年11月時点の情報です。数字は web-features-explorer（web-platform-dx）、web.dev、Chrome for Developers の記載によります。筆者が実機で動作を確かめたのはChrome 153のみです。使う前に、MDNの互換表で最新の状況を確かめてください。

「全主要ブラウザ」は、Chrome、Edge、Firefox、Safari の現行版すべてで使えることを指します。

## 本書で使った機能

| 機能 | 状況 | 初対応 | 本書の章 |
|---|---|---|---|
| `border-radius`、`box-shadow`、グラデーション | 全主要ブラウザ | — | 3章 |
| `clip-path` の `inset()` `circle()` `ellipse()` `polygon()` | 全主要ブラウザ | Chrome 37 / Edge 79 / Firefox 54 / Safari 10.1 | 4章 |
| `clip-path: shape()` | 全主要ブラウザ（2026年2月〜） | Chrome 135 / Edge 135 / Safari 18.4 / Firefox 148 | 4章、7章 |
| `mask-image`、`mask-composite`（接頭辞なし） | 全主要ブラウザ（2023年12月〜） | — | 4章 |
| `sin()` `cos()` `tan()` | 全主要ブラウザ | Safari 15.4 / Firefox 108 / Chrome 111 / Edge 111 | 5章 |
| `@property` | 全主要ブラウザ（2024年7月〜） | Chrome 85 / Edge 85 / Safari 16.4 / Firefox 128 | 8章 |
| コンテナクエリ（`container-type`） | 全主要ブラウザ | Chrome 105 / Edge 105 / Safari 16 / Firefox 110 | 6章 |

## 本書では使っていないが、絵に役立つ機能

| 機能 | 状況 | 初対応 | 使い道 |
|---|---|---|---|
| `clip-path` の `rect()` `xywh()` | 全主要ブラウザ | Chrome 119 / Edge 119 / Firefox 122 / Safari 17.2 | 長方形の切り抜き |
| `color-mix()` | 全主要ブラウザ | Safari 16.2 / Chrome 111 / Edge 111 / Firefox 113 | 基準の色から陰影の色を作る |
| `light-dark()` | 全主要ブラウザ（2024年5月〜） | Firefox 120 / Chrome 123 / Edge 123 / Safari 17.5 | 明暗のテーマで配色を切り替える |
| `sibling-index()` `sibling-count()` | 全主要ブラウザ（2026年8月〜） | Chrome 138 / Edge 138 / Safari 26.2 / Firefox 154 | 何番目の要素かを使って角度を自動計算する |
| `corner-shape` | Chrome / Edge のみ | Chrome 139 / Edge 139 | 角の形を、斜め切り・えぐり・スクワークルに変える |

## 補足

**`sibling-index()` を使うと、5章の円周配置（5.10）で `style="--i:0"` を手で書かずに済みます。** `--a: calc((sibling-index() - 1) * 30deg)` と書けます。新しい機能なので、本書では確実に動く書き方を採りました。

**`corner-shape` は `clip-path` と違い、影や枠線が形に沿います。** 対応ブラウザが限られるので、当面は「無くても困らない装飾」にとどめてください。

**コンテナ単位（`cqi` など）が単独でいつから使えるかは、確認できませんでした。** コンテナクエリと同時期と思われますが、裏は取れていません。

**anchor positioning は、資料によって対応状況の記載が食い違っており、確定できませんでした。** 絵を描く用途では必須ではないので、本書では扱っていません。

## 確かめ方

```css
@supports (clip-path: shape(from 0 0, line to 1px 1px, close)) {
  /* shape() が使えるときだけ適用される */
}
```

JavaScriptからは `CSS.supports("clip-path", "shape(from 0 0, line to 1px 1px, close)")` で確かめられます。
