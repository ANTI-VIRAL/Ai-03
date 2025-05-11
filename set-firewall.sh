#!/bin/bash

# PORT VPS RELAY kamu
RELAY_PORT="11090"

# FLUSH tapi jaga koneksi SSH biar gak lost
sudo iptables -F
sudo iptables -X

# Default policy
sudo iptables -P OUTPUT DROP
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD DROP

# Allow koneksi SSH (jaga jangan keputus ya sayang)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Allow koneksi keluar ke port relay (destination ALL)
sudo iptables -A OUTPUT -p tcp --dport $RELAY_PORT -j ACCEPT

# Allow DNS (kalau pakai domain)
sudo iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

# Allow localhost
sudo iptables -A OUTPUT -o lo -j ACCEPT

# (Optional) Simpan rules
sudo apt-get install iptables-persistent -y
sudo netfilter-persistent save
