#!/bin/sh

#CONFIG
conf="config/nmap.conf"
hosts="output/live-hosts.txt"
xml="output/nmap-output.xml"
nmapvulnxml="output/nmapvuln.xml"
xml2json="plugins/xml2json/xml2json.py"
json="output/nmap-output.json"
red="\e[31m"
reset="\e[0m"
bold="\e[1m"
flicker="\e[5m"
lgreen="\e[92m"

#SCRIPT
clear
## SETUP
echo $red$bold"Starting Tool\n"$reset
echo $bold$lgreen"Starting up nessus"$reset
sh fixnessus.sh
/etc/init.d/nessusd start
## nmap pingsweep
echo $bold$lgreen"Nmap scans"$reset
nmap -n -sS -iL $conf -oG - | awk '/Up$/{print $2}' > $hosts
echo $bold$lgreen"Pingsweep done"$reset
## nmap service detection
nmap -sV -O -iL $hosts -oX $xml
echo $bold$lgreen"Service detection done"$reset
python $xml2json -t xml2json -o $json $xml
echo $bold$lgreen"Starting nessus scan"$reset
#sh nessus.sh
echo $lgreen$bold$flicker"Nessus scan in progress"$reset
# check periodically to see if scan is done
echo $bold$lgreen"Starting nmap vulnerability scan"$reset
nmap -Pn --script vuln -iL $hosts -oX $nmapvulnxml