# static_ondisk_kv
[![pypi](https://img.shields.io/pypi/v/static_ondisk_kv.svg)](https://pypi.python.org/pypi/static_ondisk_kv)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rom1504/static_ondisk_kv/blob/master/notebook/static_ondisk_kv_getting_started.ipynb)
[![Try it on gitpod](https://img.shields.io/badge/try-on%20gitpod-brightgreen.svg)](https://gitpod.io/#https://github.com/rom1504/static_ondisk_kv)

Simple and fast implementation of a static on disk kv, in python

## Install

pip install static_ondisk_kv

## Python examples

Checkout these examples to call this as a lib:
* [example.py](examples/example.py)

## API

This module exposes a single function `hello_world` which takes the same arguments as the command line tool:

* **message** the message to print. (*required*)

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
