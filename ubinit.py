import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script is going to create an employee profile. 
    """)
    parser.add_argument("ip", help="ip address of the server")
    

    args = parser.parse_args()

    def getGateway(ip):
        ip = ip.split(".")
        ip[3] = "1"
        ip = ".".join(ip)
        return ip
        

    interfaceName = os.popen("ip route | grep default | awk '{print $5}'").read().strip()

    config = f"""
network:
    version: 2
    renderer: networkd
    ethernets:
        {interfaceName}:
            dhcp4: no
            addresses:
                - {args.ip}/24
            gateway4: {getGateway(args.ip)}
            nameservers:
                addresses: [8.8.8.8, 1.1.1.1]"""
            
    with open("/etc/netplan/00-installer-config.yaml", "w") as f:
        f.write(config)
        f.close()
        
    #growpart /dev/sda 3;
    #pvresize /dev/sda3;
    #lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
    #resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
    os.system("growpart /dev/sda 3; pvresize /dev/sda3; lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv; resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv")

    os.system("netplan apply")
    os.system("reboot")
