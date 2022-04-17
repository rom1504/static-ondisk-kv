# static_ondisk_kv
[![pypi](https://img.shields.io/pypi/v/static_ondisk_kv.svg)](https://pypi.python.org/pypi/static_ondisk_kv)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rom1504/static_ondisk_kv/blob/master/notebook/static_ondisk_kv_getting_started.ipynb)
[![Try it on gitpod](https://img.shields.io/badge/try-on%20gitpod-brightgreen.svg)](https://gitpod.io/#https://github.com/rom1504/static_ondisk_kv)

Simple and fast implementation of a static on disk kv, in python


## Why this lib?

leveldb, rocksdb and lmdb all have issues for a static collections of key and values:
* slow to build (many hours) : 3h for rocksdb compared to 1h for this lib (for a 5B collections for 1 long and 2 float16)
* uses more space than necessary (100GB for rocksdb unlike 60GB)
* as fast as this much simpler lib: about 5k sample/s on nvme drive

What this lib does not support:
* non static collection
* variable length values and keys

## Install

pip install static_ondisk_kv

## Python examples

Checkout these examples:
* [synthetic_example.py](examples/synthetic_example.py)
* [end_to_end_example.py](examples/end_to_end_example.py)
* [prebuilt_example.py](examples/prebuilt_example.py)

```py
from static_ondisk_kv import OnDiskKV
from tqdm import tqdm
import random

kv = OnDiskKV(file='/media/nvme/mybigfile', key_format="q", value_format="ee")
print("length", kv.length)
k = kv.get_key(100)
v = kv.get_value(100)
print(k)
print(v)
print(kv[k])
```

## API

### OnDiskKV(file, key_format="q", value_format="ee")

Creates an ondisk kv from `file` using `key_format` and `value_format` for decoding.

#### get_key(i)

Returns the key at position i.

#### get_value(i)

Returns the value at position i.

#### __getitem__(k)

Returns the value for the key `k`


### sort_parquet(input_collection, key_column, value_columns, output_folder)

sort parquet files of collection `input_collection` by `key_column` and writes to `output_folder`


### parquet_to_file(input_collection, key_column, value_columns, output_file, key_format, value_format)

read parquet of sorted `input_collection` and writes to `output_file` the key and values using format `key_format` and `value_format`


## For development

Either locally, or in [gitpod](https://gitpod.io/#https://github.com/rom1504/static_ondisk_kv) (do `export PIP_USER=false` there)

Setup a virtualenv:

```
python3 -m venv .env
source .env/bin/activate
pip install -e .
```

to run tests:
```
pip install -r requirements-test.txt
```
then 
```
make lint
make test
```

You can use `make black` to reformat the code

`python -m pytest -x -s -v tests -k "dummy"` to run a specific test
