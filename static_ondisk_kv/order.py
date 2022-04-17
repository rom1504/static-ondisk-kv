"""order parquet collection"""


import fire


def sort_parquet(input_collection, key_column, value_columns, output_folder):
    """order parquet collection"""
    from pyspark.sql import SparkSession  # pylint: disable=import-outside-toplevel

    spark = SparkSession.getActiveSession()
    if spark is None:
        spark = (
            SparkSession.builder.config("spark.sql.autoBroadcastJoinThreshold", -1)
            .config("spark.sql.shuffle.partitions", 1000)
            .config("spark.driver.memory", "16G")
            .master("local[16]")
            .appName("spark-stats")
            .getOrCreate()
        )
    df = spark.read.parquet(input_collection)
    df = df.select(key_column, *value_columns)
    df = df.filter(df[key_column].isNotNull())
    for v in value_columns:
        df = df.filter(df[v].isNotNull())
    df = df.sort(key_column)
    df.coalesce(512).write.mode("overwrite").parquet(output_folder)


if __name__ == "__main__":
    fire.Fire(sort_parquet)
