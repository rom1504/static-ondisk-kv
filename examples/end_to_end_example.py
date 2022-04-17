from static_ondisk_kv import sort_parquet, parquet_to_file, OnDiskKV
from tqdm import tqdm
import random

# cd /tmp && wget https://huggingface.co/datasets/laion/laion2B-en-safety/resolve/main/part-00000-04f28fe3-36a0-4ea1-bae0-734c27804ea6-c000.snappy.parquet


step = 2

if step == 0:
    sort_parquet(
        input_collection="/tmp/part-00000-04f28fe3-36a0-4ea1-bae0-734c27804ea6-c000.snappy.parquet",
        key_column="hash",
        value_columns=["prediction"],
        output_folder="/tmp/unsafe_collection",
    )

elif step == 1:
    parquet_to_file(
        input_collection="/tmp/unsafe_collection",
        key_column="hash",
        value_columns=["prediction"],
        output_file="/tmp/ordered_file",
        key_format="q",
        value_format="e",
    )
elif step == 2:
    kv = OnDiskKV(file="/tmp/ordered_file", key_format="q", value_format="e")
    print("length", kv.length)
    k = kv.get_key(100)
    v = kv.get_value(100)
    print(k)
    print(v)
    print(kv[k])
    r = [random.randint(0, kv.length) for _ in range(10**7)]
    for i in tqdm(r):
        k = kv.get_key(i)
        kv[k]
