import socket
import struct

class Client:
    def __init__:
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007

        # socket.AF_INET: Internet Protocol v4 addresses
        # socket.SOCK_DGRAM: UDP datagrams
        # socket.IPPROTO_UDP: set UDP protocol
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET,socket.IP_RECVDSTADDR,1)

        sock.bind(('',MCAST_PORT))
        sock.sendto(str.encode("Hello this is user 1"),(MCAST_GRP,MCAST_PORT))

        # Tell the operating system to add the socket to the multicast group on all interfaces.
        mreq = struct.pack("4sl",socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Setting TTL
        ttl = struct.pack('b',1)
        sock.setsocketopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

