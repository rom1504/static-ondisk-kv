"""transform a parquet collection into an ordered file"""

from tqdm import tqdm
from struct import pack
import pyarrow as pa
import pyarrow.dataset as ds
import pandas as pd
import fire


def parquet_to_file(
    input_collection,
    output_file,
    key_column="hash",
    value_columns=None,
    key_format="q",
    value_format="ee",
):
    """transform a parquet collection into an ordered file"""
    if value_columns is None:
        value_columns = ["pwatermark", "punsafe"]

    dataset = ds.dataset(input_collection, format="parquet")

    def encodeb(k, values):
        k, v = pack(key_format, k), pack(value_format, *values)
        return k + v

    with open(output_file, "wb") as f:
        for batch in tqdm(dataset.to_batches()):
            d = batch.to_pandas(types_mapper={pa.int64(): pd.Int64Dtype()}.get)
            for t in zip(d[key_column], *[d[value_column] for value_column in value_columns]):
                k = t[0]
                vs = t[1:]
                l = encodeb(k, vs)
                f.write(l)


if __name__ == "__main__":
    fire.Fire(parquet_to_file)
