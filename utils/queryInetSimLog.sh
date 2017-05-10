echo $1
sudo grep -iE "info" /var/log/inetsim/service.log  | grep "$1" | grep -E "info.*Request" 
sudo grep -iE "info" /var/log/inetsim/service.log  | grep "$1" | grep -E "info.*Request" | grep -vEf ~/cuckoo-modified/utils/networkWhiteList.txt
sudo grep -iE "info" /var/log/inetsim/service.log  | grep "$1" | grep -E "info.*Request" | grep -vEf ~/cuckoo-modified/utils/networkWhiteList.txt | cut -f 6-12 -d : |  sed -e "s/\./\.\./"
sudo grep -iE "dns_.*recv" /var/log/inetsim/service.log  | grep "$1" | grep -vEf ~/cuckoo-modified/utils/networkWhiteList.txt | cut -f 4-12 -d : | sed -e "s/\./\.\./"
sudo grep -iE "dns_.*recv" /var/log/inetsim/service.log  | grep "$1" | grep -vEf ~/cuckoo-modified/utils/networkWhiteList.txt | cut -f 4-12 -d : | sed -e "s/\./\.\./"

