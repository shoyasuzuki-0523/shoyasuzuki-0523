# 職務経歴書

# 目次

- [基本情報](#基本情報)
- [職務要約](#職務要約)
- [技術スタック](#技術スタック)
- [職務経歴](#職務経歴)

# 基本情報

|項目|詳細|
|---|---|
|氏名|鈴木翔也|
|生年月日|1998/05/23|
|居住地|東京都|
|GitHub|https://github.com/shoyasuzuki-0523|
|X|https://x.com/WisheeBell|
|Qiita|https://qiita.com/WisheeBell|
|Zenn|https://zenn.dev/show_yeah|

# 職務要約

2021年4月から既存の在庫管理システムの開発に携わり、2024年1月からはグループ企業全体で利用できる汎用的な在庫管理システムの新規開発に携わる。

主に担当するのは、在庫管理システムのインフラ構築とバックエンド開発であり、稀にフロントエンジニアとしてスポットで参加することもある。GCPやAWS、Terraform, といったインフラ構築技術に加え、Go、Ruby、Pythonといったバックエンド開発言語も活用する。またGithub Actions, Circle CIといったCI/CDの構築の経験もある。

開発業務においては単に実装するだけでなく機能の要件定義や画面イメージの作成も担当してきた。ユーザーにとって使いやすいシステムとなるよう上流工程から積極的に関わる。

開発業務と並行して新卒採用活動にも積極的に参加しており、面接やカジュアル面談を担当し開発組織の拡大にも貢献している。またチームメンバーのメンターも担当しており、育成にも力を入れている。

これらの経験を通じて、技術力はもちろんのこと、コミュニケーション能力や育成能力も身につけた。
# 技術スタック

|項目|詳細|
|---|---|
|インフラ|Google Cloud、AWS、Terraform|
|データベース|PostgreSQL|
|バックエンド|Go, Ruby on Rails, Python|
|フロントエンド|React.js, Vue.js|
|CI・CD|GitHub Actions、CircleCI|
|ツール|Jira、Confluence、Slack、Sentry, NewRelic, Mackerel|

# 職務経歴

## 2021/04 ~ 現在 株式会社 BuySell Technologies

### 2024/01 ~ グループ企業で使用する汎用的な在庫＆販売実績管理システムの開発

M&Aによるグループ企業拡大に伴い企業間での在庫のやり取りや在庫情報の一元管理を行う必要があった。
そこでグループ企業間で汎用的に使用できる在庫管理システムの開発がスタートしその開発に携わった。

#### 概要

|項目|詳細|
|---|---|
|期間|2024/01~|
|チーム構成|EM 1名、PdM 1名、バックエンド 2名、フロントエンド 2名|
|役割|バックエンドエンジニア|
|使用技術|Go, Gin, Gorm, React.js, GCP, Terraform, NewRelic|

#### 担当業務

- インフラ構築
  - 開発環境, 本番環境の構築
  - 自動デプロイの整備
  - DB閲覧やインフラの閲覧&更新の権限に関する整備
- バックエンド開発
  - 技術選定
  - DB設計
  - 自動テスト環境の整備
  - 機能実装
- その他
  - 要件定義
  - 画面イメージの作成

#### 主要実績

##### ユーザーを意識したプロダクト開発

ユーザー視点に立ち、要件定義段階からプロジェクトに参画した。ユーザーにとって本当に価値のある機能とは何かをチームと議論し、バックエンドの技術的な制約も考慮しながら、具体的な要件に落とし込んだ。また、使いやすいUIの実現に向けて、バックエンドのデータ構造やAPI設計を踏まえた提案を行い、スムーズな開発を支援した。

##### チームの足りない部分を補う立ち回り

開発初期、チームにインフラ構築経験者がいなかったので、私が率先して担当した。これは、チームに不足するスキルを補い、プロジェクトを円滑に進めるために貢献することができた。自身の経験と知識を活かし、インフラ構築に必要な作業を一手に引き受け、チームは外部の助けを借りずに開発を進めることができた。

##### DBやインフラのリソースに関する権限の整備
DBのデータやインフラのリソースに関して適切な適切な人員が適切なリソースにアクセスできるよう権限を整備した。具体的にはGCPのIAMとDBのユーザーを紐付け個々のユーザーごとに閲覧&更新できるデータを制限できるよう整備した。インフラのリソースに関してもPAMを用いて必要なユーザーに必要なタイミングだけ権限を付与するシステムを構築した。

### 2021/04 ~ 社内の在庫＆販売実績管理システムの開発

すでに運用されていた在庫管理システムの保守運用を行なった。
参加した時点で1000ユーザーほど（倉庫の従業員に加えて各地の営業所の方が使用）おり在庫のデータも100万件以上存在している規模だった。

主に社内での問い合わせ対応や要望のヒアリングに加えて実際に開発する内容の要件定義や機能の開発を行なった。

#### 概要

|項目|詳細|
|---|---|
|期間|2021/04~|
|チーム構成|EM 1名、PdM 1名、エンジニア 3名|
|役割|フルスタックエンジニア|
|使用技術|Ruby on Rails, Vue.js(v2), AWS, Terraform, NewRelic, mackerel, Circle CI|

#### 担当業務

- バックエンド開発
- フロントエンド開発
- その他
  - 要件定義
  - 画面イメージ作成
  - 問い合わせ対応

#### 主要実績

##### ユーザーと直接対話する開発

社内で不具合や追加機能の要望があった際にエンジニアが直接対応していた。
そのためユーザーがどのような業務フローで何を課題に感じているのか身近にヒアリングすることができた。
またそれによってユーザーから直接感謝される機会もあり仕事のやりがいを感じることにもつながった。

##### AWS Lambda や FTP サーバーを用いた外部サービスとの連携

外部の別サービスへ在庫の情報を連携するためLambdaによる定期実行される処理やCSVファイルをFTPサーバーでやりとりするような連携処理を実装した。
すでに定期実行されるバッチ処理が複数存在していたためその辺りの現状を整理し細かく文章化しながら進めていくことで既存の処理に影響を与えないよう実装した。

### その他

#### 採用活動

エンジニアの新卒採用活動を担当した。
実際に面接官やカジュアル面談にも参加しメンバーのリクルートに貢献した。

- サマーインターンシップの運営
- 逆求人イベントへの参加
- 面接
- アトラクト面談
- 内定者インターンのメンター
