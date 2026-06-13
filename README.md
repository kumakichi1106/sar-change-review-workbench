# SAR Change Review Workbench

Sentinel-1 GRD画像を題材に、SAR画像の取得・可視化からWebアプリケーション上での比較・確認・判断までの流れを学ぶためのReact / TypeScript製Webアプリケーションです。

## 目的

本プロジェクトは、本番レベルのSAR解析やPythonスキルを示すことを目的としたものではありません。

衛星データやSARデータを扱う基本的な流れを学び、自分の強みであるWebアプリケーション開発と接続することを目的に作成しています。

## 参考にする学習内容

SAR画像の取得・可視化の学習には、宙畑の記事「SAR画像（Sentinel-1）の取得から可視化まで～GEE、STAC編～」を参考にしています。

今後、記事で紹介されているGoogle Earth Engine上のSentinel-1 GRD画像取得・可視化の流れを学習し、その結果をReactアプリケーションで扱う予定です。

## 方針

- 本アプリは本番レベルのSAR解析ツールではありません。
- 高精度な変化検知、干渉SAR、地表変位解析を目的としていません。
- Pythonは、取得済み画像の前処理、差分画像、変化マスク、簡易メトリクス生成に使う予定です。
- React / TypeScriptでは、処理結果を比較・確認・判断するためのUIを実装する予定です。

## 使用技術

- React
- TypeScript
- Vite
- CSS
- Python
- NumPy
- Pillow
- matplotlib

## フォルダ構成

実務での保守性や機能追加を意識し、以下のように責務を分けます。

- `components`: 表示コンポーネント
- `layout`: 画面全体のレイアウト
- `dataModel`: アプリで扱うデータ型
- `constants`: 初期表示用データや固定値
- `domain`: 今後追加するレビュー判定やメトリクス整形ロジック
- `infrastructure`: 今後追加するローカルJSON読み込みやAPI接続
- `hooks`: Reactとdomain / infrastructureを接続する処理

## 今後の実装予定

- GEEで取得したSentinel-1画像を実際に接続する
- Pythonで画像前処理、差分画像、変化マスク、簡易メトリクスを生成する
- ReactでBefore / After比較、差分表示、レビューUIを実装する

## セットアップ

```bash
yarn install
yarn dev
```

ビルド確認:

```bash
yarn build
```
