-- 建設業の許可は必ず 1 つ以上の業種に出る。業種の無い許可が 1% を超えれば業種の検索を取り損ねている。
SELECT count(*) AS without_trade
FROM {{ ref('contractor') }}
ANTI JOIN {{ ref('contractor_trade') }} USING (license_code)
HAVING count(*) > (SELECT count(*) FROM {{ ref('contractor') }}) / 100
