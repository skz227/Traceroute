from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii
import math


ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    myChecksum = 0
    myID= os.getpid() & 0xFFFF  # Return the current process i
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff		
    else:
	    myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    

    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.

    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end

    # So the function ending should look like this

    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = [] #This is your list to use when iterating through each trace 
    tracelist2 = [] #This is your list to contain all traces

    for ttl in range(1,MAX_HOPS):
        tracelist1.clear()
        tracelist1.append(str(ttl))
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname) # return ip address
            #print(hostname + "Tracing")
            #Fill in start
            #current_protocol="icmp"
            proto_constant=getprotobyname("icmp")
            mySocket = socket.socket(AF_INET, SOCK_RAW, proto_constant)
            # Make a raw socket named mySocket
            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    tracelist1.append("*")
                    tracelist1.append("Request timed out")
                    [' {} '.format(x) for x in tracelist1]
                    #print(tracelist1)
                    #Fill in start
                    #pckt_vars=[ttl, (timeReceived-t)*1000, destAddr, hostname]
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #tracelist2.append(tracelist1)
                    #You should add the list above to your all traces list
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist1.append("*")
                    tracelist1.append("Request timed out")
                    [' {} '.format(x) for x in tracelist1]
                    #print(tracelist1)
                    #Fill in start
                    #pckt_vars=[ttl, (timeReceived-t)*1000, destAddr, hostname]
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #tracelist2.append(tracelist1)
                    #You should add the list above to your all traces list
                    #Fill in end
            except timeout:
                continue

            else:
                #Fill in start
                types = recvPacket[20]
                #Fetch the icmp type from the IP packet
                #Fill in end
                try: #try to fetch the hostname
                    ip_add = addr[0]
                    host_name = gethostbyaddr(ip_add)[0]
                    tracelist1.append(host_name)
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #tracelist2.append(tracelist1)
                    #Fill in start
                    #Fill in end
                except herror:   #if the host does not provide a hostname
                    #Fill in start
                    host_name="hostname not returnable"
                    tracelist1.append(host_name)
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #tracelist2.append(tracelist2)
                    #Fill in end

                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 +bytes])[0]
                    #Fill in start
                    #hop_no=format(ttl, '%d')
                    #= str((timeReceived-timeSent*1000)+ "ms")
                    Round_trip_time=str(math.ceil((timeReceived-t)*1000)) + "ms"
                    #Rount_trip_time= Rount_trip_time + "ms"
                    #tracelist1.append(hop_no)
                    tracelist1.append(Round_trip_time)
                    tracelist1.append(ip_add)
                    tracelist1.append(host_name)
                    [' {} '.format(x) for x in tracelist1]
                    #print(tracelist1)
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #Vars=[("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived -timeSent)*1000, addr[0]))]

                    #You should add your responses to your lists here
                    #Fill in end
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #hop_no=format(ttl, '%d')
                    Round_trip_time=str(math.ceil((timeReceived-t)*1000)) + "ms"
                    #Round_trip_time=(" %.0fms" %((timeReceived-timeSent)*1000))
                    #tracelist1.append(hop_no)
                    tracelist1.append(Round_trip_time)
                    tracelist1.append(ip_add)
                    tracelist1.append(host_name)
                    [' {} '.format(x) for x in tracelist1]
                    #print(tracelist1)
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #You should add your responses to your lists here 
                    #Fill in end
                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #hop_no=format(ttl, '%d')
                    Round_trip_time=str(math.ceil((timeReceived-timeSent)*1000)) + "ms"
                    #Round_trip_time=(" %.0fms" %((timeReceived-timeSent)*1000))
                    #Rount_trip_time= Rount_trip_time + "ms"
                    #tracelist1.append(hop_no)
                    tracelist1.append(Round_trip_time)
                    tracelist1.append(ip_add)
                    tracelist1.append(host_name)
                    [' {} '.format(x) for x in tracelist1]
                    #print(tracelist1)
                    Nest_list=tracelist1[:]
                    tracelist2.append(Nest_list)
                    #if host_name==hostname:

                    #return host_name
                    #You should add your responses to your lists here and return your list if your destination IP is met
                    
                    #Fill in end
                else:
                    #Fill in start
                    tracelist1.append("Error in the if statement")
                    #If there is an exception/error to your if statements, you should append that to your list here
                    #Fill in end
                break
            finally:
                mySocket.close()
    #print(tracelist2)
    [' {} '.format(x) for x in tracelist2]
    #print(tracelist2)
    return tracelist2

get_route("bing.com")