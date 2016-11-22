# DPCチェッカー ver 0.06

Dファイル・EFファイルをロードし、SQLiteデータベースに登録して
クエリを発行するアプリケーションです。
現在はデータ識別番号／入院年月日別の出来高対比、退院処方の入力ミスチェック
機能を実装しています。

全くの未完成なので、バージョンは0.06としてあります。


## 既知の問題点/未実装機能

<del>- 抽出データのcsvエクスポート機能　未実装（予定あり）</del> 0.06で実装済み
- 特定の病棟を除外する機能　未実装（予定あり）
- 外部クエリの読み込み機能　未実装（予定あり）　テキストファイルを読み込む方式になりそう
- グラフによるデータの可視化　未実装（Bokehを使用する予定）
- 複数月にまたがるデータの登録　未実装（方針未決定）

## 使用ライブラリ

- Pandas
- Flask
- DataTables
- jquery

## 動作条件

Python 3.x系統　Flask,Pandas必須
Anaconda推奨






















































