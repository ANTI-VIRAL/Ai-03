#!/bin/bash

RELAY_PORT="11002"

# Bersihkan rules sebelumnya
iptables -F
iptables -X

# Set default policy
iptables -P OUTPUT DROP
iptables -P INPUT ACCEPT
iptables -P FORWARD DROP

# Jaga koneksi SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Izinkan koneksi ke port relay
iptables -A OUTPUT -p tcp --dport $RELAY_PORT -j ACCEPT

# Izinkan DNS (domain)
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

# Izinkan localhost
iptables -A OUTPUT -o lo -j ACCEPT

# Cek apakah apt-get tersedia (berarti kemungkinan Ubuntu/Debian)
if command -v apt-get >/dev/null 2>&1; then
    echo "[*] Debian/Ubuntu terdeteksi, tapi skip install iptables-persistent"
else
    echo "[*] Bukan Debian/Ubuntu, skip bagian iptables-persistent"
fi

echo "[✓] Firewall rules telah diterapkan (tanpa simpan permanen)"
exit 0
