import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.bind(('0.0.0.0',68))

CLIENT_IP_ADDRESS = '\x00\x00\x00\x00'
YOUR_IP_ADDRESS = '\x00\x00\x00\x00'
NEXT_SERVER_ADDRESS = '\x00\x00\x00\x00'
RELAY_AGENT_ADDRESS = '\x00\x00\x00\x00'
CLIENT_MAC='\x01\x02\x03\x04\x05\x06'  #your MAC Address
magic_cookie='\x63\x82\x53\x63'

pkg=b'\x01' #Boot request(1)
pkg+=b'\x01' #hardware type ethernet(0x01)
pkg+=b'\x06' #hardware address length 6
pkg+=b'\x00' #hops 0
pkg+=b'\x11\x22\x33\x44' #TransactionID
pkg+=b'\x00\x00' #Seconds Elapsed: 0
pkg+=b'\x00\x00' #bootpflags unicast
pkg+=CLIENT_IP_ADDRESS.encode()
pkg+=YOUR_IP_ADDRESS.encode()
pkg+=NEXT_SERVER_ADDRESS.encode()
pkg+=RELAY_AGENT_ADDRESS.encode()
pkg+=CLIENT_MAC.encode() + (b'\x00'*10) #padding
pkg+=(b'\x00'*192)
pkg+=b'\x63\x82\x53\x63'
pkg+=b'\x35\x01\x01'     #DHCP Discover
pkg+=b'\x37\x0a\x01\x79\x03\x06\x0f\x77\xfc\x5f\x2c\x2e' #parameter request list (1)(121)(3)(6)(15)(119)(252)(95)(44)(46)
pkg+=b'\x39\x02\x05\xdc' #option(57) maximum dhcp message size 1500
pkg+=b'\x3d\x07\x01'+CLIENT_MAC.encode()       #Client identifier 3d length 07 hardware type ethernet 01
pkg+=b'\x33\x04\x00\x76\xa7\x00' #IP address lease time 33 length 04 lease time 00 76 a7 00 (90 days)
pkg+=b'\x0c\x0f\x4c\x69\x6e\x4a\x61\x63\x6b\x73\x6f\x6e\x64\x65\x4d\x42\x50' #host name 0c length 0f name LinJacksondeMBP
pkg+=b'\xff\x00\x00\x00\x00\x00\x00\x00\x00'     #end

s.sendto(pkg,("255.255.255.255",67))
a=1
while True:
    msg, addr = s.recvfrom(1024)
    msg_type = msg[242:243]
    if msg_type==b'\x02': #offerMsg
        '''
        print('offerMSG')
        print('OP: ',msg[:1],' : OfferMSG')
        print('YIADDR: ',msg[16:20])
        print('SIADDRL ',msg[20:24])
        '''
        NEXT_SERVER_ADDRESS = msg[20:24]
        pkg=b'\x01' #Boot request(1)
        pkg+=b'\x01' #hardware type ethernet(0x01)
        pkg+=b'\x06' #hardware address length 6
        pkg+=b'\x00' #hops 0
        pkg+=b'\x11\x22\x33\x44' #TransactionID
        pkg+=b'\x00\x00' #Seconds Elapsed: 0
        pkg+=b'\x00\x00' #bootpflags unicast
        pkg+=CLIENT_IP_ADDRESS.encode()
        pkg+=YOUR_IP_ADDRESS.encode()
        pkg+=NEXT_SERVER_ADDRESS
        pkg+=RELAY_AGENT_ADDRESS.encode()
        pkg+=CLIENT_MAC.encode() + (b'\x00'*10) #padding
        pkg+=(b'\x00'*192)
        pkg+=b'\x63\x82\x53\x63'
        pkg+=b'\x35\x01\x03' #op53
        pkg+=b'\x32\x04\xc0\xa8\x01\x6c' #op50 Request IP 192.168.1.108
        pkg+=b'\x36\x04'+NEXT_SERVER_ADDRESS #op54 server ip
        pkg+=b'\xff'
        s.sendto(pkg,('255.255.255.255',67))
        break
