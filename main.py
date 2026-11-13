"""建設業者・宅建業者等企業情報検索システムのデータパイプライン。

1. license: 建設業者・建設業者の業種・宅建業者の一覧を取得して Parquet にする
2. dbt: dbt ビルド
"""

import logging

from dbt.cli.main import dbtRunner

from pipelines.license import download_license

# dbt を読み込むとルートロガーが先に設定されるので、force で上書きする
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", force=True)
logger = logging.getLogger("pipelines")


def dbt_build():
    dbt = dbtRunner()
    for command in (["deps"], ["build"], ["docs", "generate"]):
        if not dbt.invoke(command).success:
            raise SystemExit(f"dbt {' '.join(command)} failed")


def main():
    logger.info("1/2: license (建設業者・宅建業者の一覧)")
    download_license()

    logger.info("2/2: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
