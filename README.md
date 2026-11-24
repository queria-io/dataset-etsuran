# 建設業者・宅建業者等企業情報検索システム

国土交通省の[建設業者・宅建業者等企業情報検索システム](https://etsuran2.mlit.go.jp/TAKKEN/)に載っている事業者の一覧を、SQL で検索・集計できるテーブルにしたデータセットです。今は建設業の許可業者と宅地建物取引業者を収録しています。

## 出典と利用条件

| 原典 | テーブル |
| --- | --- |
| [建設業者・宅建業者等企業情報検索システム](https://etsuran2.mlit.go.jp/TAKKEN/)の建設業者の検索結果の一覧 | `construction.*` |
| 同じ検索システムの宅地建物取引業者の検索結果の一覧 | `real_estate.*` |

- 国土交通省ウェブサイトのコンテンツに準拠する[公共データ利用規約（第1.0版）（PDL1.0）](https://www.mlit.go.jp/link.html)に従います
- 使うときは、たとえば「「建設業者・宅建業者等企業情報検索システム」（国土交通省）を加工して作成」のように、出典と加工したことを書いてください
- 提供情報の最新性、正確性、完全性等が保証されたものではありません

加工の内容: 許可・免許を出した行政庁ごとの検索結果の一覧を 1 行にまとめ、許可番号を数字の列に分けています。業種は、業種と一般・特定で絞った検索結果から作っています。全角英数を半角に正規化しています。代表者名と、個人事業主の行は取り込んでいません。

## テーブル

| テーブル | 内容 |
| --- | --- |
| `construction.contractor` | 1 行が 1 件の建設業の許可。許可行政庁・許可番号・商号・所在地 |
| `construction.contractor_trade` | 1 行が 1 許可 × 1 業種。29 業種と一般・特定の区分 |
| `real_estate.broker` | 1 行が 1 件の宅地建物取引業の免許。免許行政庁・免許証番号・更新回数・商号・所在地 |

## 使い方

都道府県知事許可の建設業者を、土木工事業の特定建設業の許可を持つものに絞って都道府県別に数える:

```sql
SELECT c.authority, count(*) AS contractors
FROM etsuran.construction.contractor AS c
JOIN etsuran.construction.contractor_trade AS t USING (license_code)
WHERE c.license_kind = '知事' AND t.trade = '土木工事業' AND t.trade_type = '特定'
GROUP BY ALL
ORDER BY contractors DESC;
```

更新回数の多い（営業の長い）宅地建物取引業者:

```sql
SELECT name, authority, renewal_count, address
FROM etsuran.real_estate.broker
ORDER BY renewal_count DESC
LIMIT 20;
```

## 収録範囲の注意

- 検索システムは月 2 回更新されます
- 1 つの許可は、許可行政庁と許可番号の組で決まります。`license_code`（許可行政庁の 2 桁と番号の 6 桁）で引いてください。許可番号だけでは都道府県をまたいで重なります
- 業種と一般・特定の区分は `construction.contractor_trade` にあります
- 商号に法人の種類（株式会社・(株)・合同会社・医療法人・協同組合など）が無い行は、個人事業主として取り込んでいません。東京都の建設業許可業者名簿の法人・個人の区分と比べると、個人の行はすべて除かれ、法人のうち名前に種類の入らない外国法人（東京都で 10 行）が漏れます
- 法人番号は検索システムに無いため持っていません。必要なときは Queria の resolve_company で商号と所在地から照合してください
- 宅地建物取引業者は本店（本社・主たる事務所）の行だけです。支店の事務所は取り込んでいません。免許ではなく届出で営む信託会社等も取り込んでいません

## ビルド

```bash
git clone https://github.com/queria-io/dataset-shared.git shared  # 初回のみ。更新は git -C shared pull
uv sync
scripts/build.sh                # 取得・ビルドして Queria に公開する
```

`main.py` が行政庁ごとに一覧を 1 回で取得し（建設業者・宅建業者それぞれ 48 回）、建設業者の業種は 29 業種 × 一般・特定で検索します。全国で 50,000 件を超える組だけ行政庁ごとに分けます。1 秒に 1 回の頻度で、1 時間ほどかかります。

`.github/workflows/sync.yml` が毎月 11 日に作り直します。
