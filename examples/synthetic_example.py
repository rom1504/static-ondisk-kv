from static_ondisk_kv import sort_parquet, parquet_to_file, OnDiskKV
from tqdm import tqdm
import random
import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "hash": np.random.randint(0, 10**8, size=(10000)),
        "pwatermark": np.random.rand(10000),
        "punsafe": np.random.rand(10000),
    }
)
df = df.drop_duplicates("hash")
df.to_parquet("/tmp/my_file.parquet")

sort_parquet(
    input_collection="/tmp/my_file.parquet",
    key_column="hash",
    value_columns=["pwatermark", "punsafe"],
    output_folder="/tmp/unsafe_collection",
)

parquet_to_file(
    input_collection="/tmp/unsafe_collection",
    key_column="hash",
    value_columns=["pwatermark", "punsafe"],
    output_file="/tmp/ordered_file",
    key_format="q",
    value_format="ee",
)
kv = OnDiskKV(file="/tmp/ordered_file", key_format="q", value_format="ee")
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
