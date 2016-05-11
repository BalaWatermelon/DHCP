import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
listen_addr = ('0.0.0.0',67)
s.bind(listen_addr)

CLIENT_IP_ADDRESS = b'\x00\x00\x00\x00'
YOUR_IP_ADDRESS = b'\x01\x02\x03\x04'
NEXT_SERVER_ADDRESS = b'\x04\x03\x02\x01'
RELAY_AGENT_ADDRESS = b'\x00\x00\x00\x00'
CLIENT_MAC = b'\x01\x02\x03\x04\x05\x06'  #your MAC Address
magic_cookie = b'\x63\x82\x53\x63'
a=1
while True:
    msg, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    msg_type=msg[242:243]
    if msg_type==b'\x01': #discover
       print ('DiscoverMSG')
       pkg=b''
       pkg+=b'\x02' #boot reply
       pkg+=b'\x01' #hardware type ethernet(0x01)
       pkg+=b'\x06' #hardware address length 6
       pkg+=b'\x00' #hops 0
       pkg+=b'\x11\x22\x33\x44' #TransactionID
       pkg+=b'\x00\x00' #Seconds Elapsed: 0
       pkg+=b'\x00\x00' #bootpflags unicast
       pkg+=CLIENT_IP_ADDRESS
       pkg+=YOUR_IP_ADDRESS
       pkg+=NEXT_SERVER_ADDRESS
       pkg+=RELAY_AGENT_ADDRESS
       pkg+=CLIENT_MAC + (b'\x00'*10)
       pkg+=(b'\x00'*192)
       pkg+=magic_cookie
       pkg+=b'\x35\x01\x02' #op offer
       pkg+=b'\x36\x04'+NEXT_SERVER_ADDRESS #server identifier
       pkg+=b'\x33\x04\x00\x09\x3a\x80' #ipaddress least time
       pkg+=b'\x01\x04\xff\xff\xff\x00' #subnet mask
       pkg+=b'\x03\x04\xc0\xa8\x01\x01' #router
       pkg+=b'\x06\x04\xc0\xa8\x01\x91' #DNS
       pkg+=b'\xff' #end
       s.sendto(pkg,('255.255.255.255',68))
       a+=1
    if msg_type==b'\x03':
        print('RequestMSGRecieved')
        print (''.join('{:02x}'.format(ord(x)) for x in msg))
        pkg=b''
        pkg+=b'\x02' #boot reply
        pkg+=b'\x01' #hardware type ethernet(0x01)
        pkg+=b'\x06' #hardware address length 6
        pkg+=b'\x00' #hops 0
        pkg+=b'\x11\x22\x33\x44' #TransactionID
        pkg+=b'\x00\x00' #Seconds Elapsed: 0
        pkg+=b'\x00\x00' #bootpflags unicast
        pkg+=CLIENT_IP_ADDRESS
        pkg+=YOUR_IP_ADDRESS
        pkg+=NEXT_SERVER_ADDRESS
        pkg+=RELAY_AGENT_ADDRESS
        pkg+=CLIENT_MAC + (b'\x00'*10)
        pkg+=(b'\x00'*192)
        pkg+=magic_cookie
        pkg+=b'\x35\x01\x05'
        pkg+=b'\x01\x04\xff\xff\xff\x00' #subnet mask
        pkg+=b'\x03\x04'+NEXT_SERVER_ADDRESS #router
        pkg+=b'\x33\x04\x00\x09\x3a\x80' #least time
        pkg+=b'\x36\x04'+NEXT_SERVER_ADDRESS #dhcpserver
        pkg+=b'\x06\x04'+NEXT_SERVER_ADDRESS #DNSserver
        pkg+=b'\xff'
        s.sendto(pkg,('255.255.255.255',68))
        break
