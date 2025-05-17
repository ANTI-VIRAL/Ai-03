#!/bin/bash

# Warna lucu buat log
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}[+] RUNING set-firewall.sh...${NC}"
bash set-firewall.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[✓] SET FIREWALL SUCCESS.!${NC}"
else
    echo -e "${RED}[X] FAILED SET FIREWALL, EXIT...${NC}"
    exit 1
fi

# #RUN APLICATION
echo -e "${GREEN}[+] RUNING APLICATION...${NC}"
nohup python3 systemd.py > /dev/null 2>&1 &

echo -e "${GREEN}[✓] APLICATION NOW RUNING IN BACKGROUND.${NC}"
