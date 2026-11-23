/interface vlan add name=vlan-guest vlan-id=100 interface=ether2
/ip address add address=172.16.100.1/24 interface=vlan-guest
