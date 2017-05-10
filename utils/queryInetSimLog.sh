sudo grep -iE "info" /var/log/inetsim/service.log  | grep "$1" | grep -E "info.*Request" | grep -vf utils/networkWhiteList.txt | cut -f 6-12 -d : |  sed -e "s/\./\.\./"
sudo grep -iE "dns_.*recv" /var/log/inetsim/service.log  | grep "$1" | grep -vf utils/networkWhiteList.txt | cut -f 4-12 -d : | sed -e "s/\./\.\./"
sudo grep -iE "dns_.*recv" /var/log/inetsim/service.log  | grep "$1" | grep -vf utils/networkWhiteList.txt | cut -f 4-12 -d : | sed -e "s/\./\.\./"

