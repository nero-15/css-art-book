# CSSで絵を描く ― 座標から始める実践レシピ

画像もSVGも使わず、CSSだけで絵を描くための本の原稿です。1章1ファイルのMarkdownで、図は `images/` にあります。

本の内容を Claude Code から使えるようにしたプラグイン（skill とサブエージェント）も、同じリポジトリに置いています。

## Claude Code で使う

本の手順とレシピを、Claude Code の skill（作業の手引き）とサブエージェント（役割を持った作業担当）にまとめています。入れておくと、「CSSで〇〇を描いて」と頼んだときに、本の進め方（下絵、分解、座標、実装、検証）で作業します。

### 含まれるもの

skill は6つです。

| 名前 | 内容 | もとの章 |
|---|---|---|
| `css-art-draw` | 5つの工程、道具の選び方、レシピ、計算式 | 1〜5章、7章、付録A |
| `css-art-quality` | 拡縮、縁のギザギザ、継ぎ目、新しい機能の安全な使い方、複数ブラウザでの確認、ブラウザ対応表 | 6章、付録A、付録B |
| `css-art-troubleshoot` | 症状から原因と直し方を引く | 10章 |
| `css-art-animate` | 動かす | 8章、10章 |
| `css-art-production` | CSSで描くべきかの判断、読み上げ対応、ハイコントラスト表示、画像への書き出し、canvas | 9章、付録A |
| `css-art-verify` | 下絵の画像を測る、描画する、画素単位で突き合わせる、の3つのスクリプトと、合格するまで直し続ける手順 | 本には無い。プラグイン独自 |

`css-art-verify` のスクリプトは、Python 3 と Pillow、それに Chrome（Chromium、Edge でも可）を使います。無くても、ほかの5つは使えます。

サブエージェントは3つです。

| 名前 | やること | もとの章 |
|---|---|---|
| `css-art-designer` | 描く前の設計だけを行う。100×100の方眼に載せた下絵、部品表、座標表、箱の割り当てを作る。コードは書かない | 2章、7.1節 |
| `css-artist` | 設計をもとにCSSで描き、実際に描画して確かめる。設計が無ければ先に作る | 1〜5章、7章 |
| `css-art-reviewer` | すでにあるCSSの絵をチェックリストに照らして点検し、問題を重さの順に、直し方つきで報告する。ファイルは書き換えない | 付録A、6章、9章 |

### プラグインとして入れる

Claude Code で次の2つを実行します。

```
/plugin marketplace add nero-15/css-art-book
/plugin install css-art@css-art-book
```

### プラグインの仕組みを使わずに入れる

リポジトリを取得し、ファイルを写します。

```sh
git clone https://github.com/nero-15/css-art-book.git
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R css-art-book/plugins/css-art/skills/* ~/.claude/skills/
cp css-art-book/plugins/css-art/agents/* ~/.claude/agents/
```

特定のプロジェクトだけで使う場合は、`~/.claude/` の代わりに、そのプロジェクトの `.claude/skills/` と `.claude/agents/` に写します。

### 頼み方の例

```
自分のイニシャル「K」と数字の「7」で、丸い紋章をCSSだけで描いて。色は紺と白。
```

```
css-art-designer で、このスケッチ（sketch.png）の部品表と座標表を作って。まだコードは書かないで。
```

```
css-art-reviewer で、src/emblem.css を公開前に点検して。
```

```
三角形を2枚並べたら、境目に細い線が出る。原因と直し方を教えて。
```

```
この下絵（logo-draft.png）をCSSだけで描いて。css-art-verify で、下絵と合うまで直して。
```

### 注意

- `css-art-verify` 以外の skill は、原稿を要約したものです。内容が食い違う場合は、原稿が正です
- コード例は Chrome 153 で描画して確かめたものです。Safari と Firefox では確認していません（本と同じ条件です）
- 権利のない既存のロゴやキャラクターを題材にしたものは、公開できません。自分のサイトや架空のブランドを題材にしてください（「はじめに」を参照）

## リポジトリの構成

| 場所 | 中身 |
|---|---|
| `00-preface.md` 〜 `appendix-c-references.md` | 本の原稿。1章1ファイル |
| `images/` | 本の図 |
| `vivliostyle.config.js` | 製本の設定例 |
| `plugins/css-art/` | Claude Code 用のプラグイン本体。`skills/` に skill、`agents/` にサブエージェント、`.claude-plugin/plugin.json` にプラグインの定義 |
| `.claude-plugin/marketplace.json` | このリポジトリをプラグインの配布元（マーケットプレイス）として登録するための定義 |
| `LICENSE`、`LICENSE-CODE` | ライセンス |

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
- `plugins/css-art/` の skill とサブエージェント: 本と同じ分け方です。文章は CC BY 4.0、中のコード例と `scripts/` のスクリプトは MIT License

© 2026 nero15
