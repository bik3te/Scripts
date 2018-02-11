sudo systemctl stop NetworkManager
sudo systemctl stop org.cups.cupsd.service
sudo systemctl stop cups-browsed.service
sudo systemctl stop avahi-daemon.socket
sudo systemctl stop avahi-daemon.service
sudo systemctl stop rpcbind.socket
macchanger -r eno1
sudo dhcpcd eno1
echo "Check if double IP on eno1"
echo "sudo ip addr show"
echo "If yes:"
echo "sudo ip addr delete dev eno1 ip/mask"
