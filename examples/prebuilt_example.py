from static_ondisk_kv import OnDiskKV
from tqdm import tqdm
import random

kv = OnDiskKV(file="/media/nvme/mybigfile", key_format="q", value_format="ee")
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
