# DPCチェッカー ver 0.12

Dファイル・EFファイルをロードし、SQLiteデータベースに登録して
クエリを発行するアプリケーションです。
現在はデータ識別番号／入院年月日別の出来高対比、退院処方の入力ミスチェックなどの
機能を実装しています。

全くの未完成なので、バージョンは0.12としてあります。

## vwe 0.12での新機能　ダッシュボード機能の書き直し／DPC入院料のグラフを追加
予告通りダッシュボード機能を書き換えました。ついでにDPC入院料のグラフを追加しています。  
今まではajaxも使わず、HTMLにJavaSciptが混在しており、HTMLの教科書の始めに書いてある「やってはいけないこと」を全部やったような代物でしたが、大分マシになった･･･筈･･･です。
コードの見通しがよくなって、拡張しやすくなったので、思いつくままグラフを追加するかも知れません。科名の日本語化は早いうちにやってしまおうと思います。


## ver 0.11での新機能　認知症ケア加算の算定チェック機能
SQLの追加をアップデートを呼ぶな！と言われたらそれまでですが、認知症ケア加算の算定チェックを行うクエリが追加されています。  
また、ダッシュボード機能の実装が**とてつもなく**酷いことは分かっていますので、近く書き換える予定です。


## ver 0.10での新機能　ダッシュボード機能

ver 0.10よりダッシュボード機能を追加しました。  
ひとまず、科別・病棟別の出来高対比グラフ・収益分布チャートが描画されます。  
現在は診療科区分がデータ名のままですが、いずれ日本語科名に対応する予定です。
なお、グラフ描画はC3.jsで行いました。


## ver 0.08 デザイン修正／挙動修正
GoogleのMaterial Design LiteのTemplateを流用して、ほんの少しだけデザインがマシになりました。まだ色々工事中です。    
それとは別に、登録・削除を行う度、別ページに遷移する変な挙動が修正されました。


## ver 0.07の新機能 外部クエリ読み込み

ver 0.07より外部クエリの読み込みに対応しました。
`query`フォルダ直下にテキストファイルでSQLクエリを保存してください（エンコーディングはUTF-8にする必要があります）。
DPCチェッカー起動時に自動的に読み込まれ、`クエリ発行ページ`のクエリリストに追加されます。


## 既知の問題点/未実装機能

<del>- 抽出データのcsvエクスポート機能　未実装（予定あり）</del> 0.06で実装済み
</br>
<del>- 外部クエリの読み込み機能　未実装（予定あり）　</del> 0.07で実装済み
</br>
<del>- グラフによるデータの可視化　未実装 </del> 0.10で実装開始
- 特定の病棟を除外する機能　未実装（予定あり）
- 複数月にまたがるデータの登録　未実装（方針未決定）
- 見た目をマトモにする。Material Design Liteに乗っかる。

## 使用ライブラリ

- Pandas
- Flask
- DataTables
- jquery
- Material Design Lite
- D3.js
- C3.js

## 動作条件

Python 3.x系統　Flask,Pandas必須
Anaconda推奨






















































