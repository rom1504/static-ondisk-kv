from static_ondisk_kv import OnDiskKV
from tqdm import tqdm
import random
import pickle

# wget https://huggingface.co/datasets/laion/laion5B-watermark-safety-ordered/resolve/main/laion5B-watermark-safety-ordered -O /media/nvme/mybigfile

kv = OnDiskKV(file="/media/nvme/mybigfile", key_format="q", value_format="ee")

kv2 = pickle.loads(pickle.dumps(kv))

k = kv.get_key(100)
print(k)
k = kv2.get_key(100)
print(k)
