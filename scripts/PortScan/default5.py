# Scapy module not loading

import scapy.all as sc
import scapy.layers.inet as scli
import socket
import random

class PortScanner():
    def __init__(self, targIP):
        self.targIp = targIP
        self.ports = list(range(1, 65535))

    def checkIfTargetOnline(self):
        arpRequest = sc.ARP(pdst=self.targIp)
        broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
        arpRequestBroadcast = broadcast / arpRequest

        # Actually Broadcasting packet to targ IP, returns two lists of answered and unanswered responses
        answeredList = sc.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]
        if len(answeredList) == 0:
            print(self.targIp)
            exit()

    def printResultsTable(self):
        osDetectPack = sc.IP(dst = self.targIp)/scli.ICMP()
        osResponse = sc.sr1(osDetectPack, timeout = 2, verbose=False)
        targetOS = ""
        if osResponse == None:
            targetOS = "Could not identify OS!"
        elif osResponse.haslayer(scli.IP):
            if osResponse[scli.IP].ttl == 64:
                targetOS = "Unix, Linux, or FreeBSD"
            elif osResponse[scli.IP].ttl == 128:
                targetOS = "Windows"
        print("Target: ", self.targIp)
        print("Detected target Operating System: {targetOS}\n")

    def dynamicPrint(self, port, portStatus):
        if portStatus == "Open":
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Could not be determined for this port"
            print(f"\r{str(port)}\t\t\t{'Open'}\t\t\t{service}", end="\n")
        elif portStatus == "Filtered":
            print(f"\r{str(port)}\t\t\t{'Filtered'}", end="\n")
        elif portStatus == "Open/Filtered":
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Could not be determined for this port"
            print(f"\r{str(port)}\t\t\t{'Open/Filtered'}\t\t\t{service}", end="\n")

    def tcpConnectScan(self):
        for port in self.ports:
            self.checkIfTargetOnline()
            localSourcePort = random.randint(1, 10000)
            tcpConnectScanResponse = sc.sr1(sc.IP(dst=self.targIp) / sc.TCP(sport=localSourcePort, dport=port, flags="S"), timeout=1,
                                           verbose=False)
            if tcpConnectScanResponse.haslayer(sc.TCP):
                flagIndicator = tcpConnectScanResponse[sc.TCP].flags
                if flagIndicator == "SA":
                    sendReset = sc.sr(sc.IP(dst=self.targIp)/sc.TCP(sport=80,dport=port,flags="AR"), timeout=1, verbose = False)
                    self.dynamicPrint(port, "Open")
                elif flagIndicator == "RA":
                    continue

    def tcpStealthScan(self):
        for port in self.ports:
            self.checkIfTargetOnline()
            localSourcePort = random.randint(1,10000)
            tcpStealthScanResponse = sc.sr1(sc.IP(dst=self.targIp) / sc.TCP(sport=localSourcePort, dport=port, flags="S"), timeout=1,
                                           verbose=False)
            if tcpStealthScanResponse.haslayer(sc.TCP):
                flagIndicator = tcpStealthScanResponse[sc.TCP].flags
                if flagIndicator == "SA":
                    sendReset = sc.sr(sc.IP(dst=self.targIp) / sc.TCP(sport=80, dport=port, flags="AR"), timeout=1,
                                      verbose=False)
                    self.dynamicPrint(port, "Open")
                elif flagIndicator == "RA":
                    continue
            elif tcpStealthScanResponse.haslayer(scli.ICMP):
                filterList = [1, 2, 3, 9,10, 13]
                if tcpStealthScanResponse[sc.ICMP].type == 3 and tcpStealthScanResponse[sc.ICMP].code in filterList:
                    self.dynamicPrint(port, "Filtered")
                    continue

    def xmasScan(self):
        for port in self.ports:
            self.checkIfTargetOnline()
            localSourcePort = random.randint(1,10000)
            xmasScanPKT = sc.sr1(sc.IP(dst=self.targIp) / sc.TCP(sport = localSourcePort, dport=port, flags="FPU"), verbose = False ,timeout=1)
            if not xmasScanPKT:
                self.dynamicPrint(port, "Open/Filtered")
            elif xmasScanPKT.haslayer(sc.TCP):
                if xmasScanPKT[sc.TCP].flags == 0x14:
                    continue
                elif xmasScanPKT.haslayer(sc.ICMP):            
                    if xmasScanPKT[sc.ICMP].type == 3 and xmasScanPKT[sc.ICMP].code in [1, 2, 3, 9, 10, 13]:
                        self.dynamicPrint(port, "Filtered")

    def finScan(self):
        for port in self.ports:
            self.checkIfTargetOnline()
            localSourcePort = random.randint(1,10000)
            finScanPKT = sc.sr1(sc.IP(dst=self.targIp) / sc.TCP(sport = localSourcePort, dport=port, flags="F"), verbose = False ,timeout=1)
            if not finScanPKT:
                self.dynamicPrint(port, "Open/Filtered")
            elif finScanPKT.haslayer(sc.TCP):
                if finScanPKT[sc.TCP].flags == 0x14:
                    continue
                elif finScanPKT.haslayer(sc.ICMP):
                    if finScanPKT[sc.ICMP].type == 3 and finScanPKT[sc.ICMP].code in [1, 2, 3, 9, 10, 13]:
                        self.dynamicPrint(port, "Filtered")

    def nullScan(self):
        for port in self.ports:
            self.checkIfTargetOnline()
            localSourcePort = random.randint(1,10000)
            finScanPKT = sc.sr1(sc.IP(dst=self.targIp) / sc.TCP(sport = localSourcePort, dport=port, flags=""), verbose = False ,timeout=1)
            if not finScanPKT:
                self.dynamicPrint(port, "Open/Filtered")
            elif finScanPKT.haslayer(sc.TCP):
                if finScanPKT[sc.TCP].flags == 0x14:
                    continue
                elif finScanPKT.haslayer(sc.ICMP):
                    if finScanPKT[sc.ICMP].type == 3 and finScanPKT[sc.ICMP].code in [1, 2, 3, 9, 10, 13]:
                        self.dynamicPrint(port, "Filtered")


    def tcpACKScan(self):
        for port in self.ports:
            self.checkIfTargetOnline()
            localSourcePort = random.randint(1,10000)
            ackFlagPKT = sc.sr1(sc.IP(dst=self.targIp) / sc.TCP(dport=port,sport = localSourcePort ,flags="A"),verbose = False , timeout=1)
            if not ackFlagPKT:
                self.dynamicPrint(port, "Filtered")
            elif ackFlagPKT.haslayer(sc.TCP):
                if ackFlagPKT[sc.TCP].flags == 0x4:
                    continue
            elif ackFlagPKT.haslayer(sc.ICMP):
                if ackFlagPKT[sc.ICMP].type == 3 and  ackFlagPKT[sc.ICMP].code == 3 in [1, 2, 3, 9, 10, 13]:
                    self.dynamicPrint(port, "Filtered")


specifiedTargetIP = socket.gethostbyname('markgacoka.com')
scanner = PortScanner(targIP=specifiedTargetIP)
scanner.checkIfTargetOnline()

scanChoice = 1
if scanChoice == "0":
    print("Exiting Program....Have a nice day!")
    exit()
else:
    print("PLEASE DO NOT EXIT THE SCAN EARLY, WAIT UNTIL THE SCAN COMPLETION MESSAGE HAS APPEARED")
    if scanChoice == "1": # TCP Connect scan
        print(f"\n[{'+'}] Initiating TCP Connect Scan on {scanner.targIp}...\n")
        scanner.printResultsTable()
        scanner.tcpConnectScan()
    elif scanChoice == "2": # stealth TCP scan
        print(f"\n[{'+'}] Initiating TCP Stealth Scan on {scanner.targIp}...\n")
        scanner.printResultsTable()
        scanner.tcpStealthScan()
    elif scanChoice == "3": # XMAS scan
        print(f"\n[{'+'}] Initiating Xmas Scan on {scanner.targIp}...\n")
        scanner.printResultsTable()
        scanner.xmasScan()
    elif scanChoice == "4": # Begin FIN Scan
        print(f"\n[{'+'}] Initiating FIN Scan on {scanner.targIp}...\n")
        scanner.printResultsTable()
        scanner.finScan()
    elif scanChoice == "5": # Null Scan
        print(f"\n[{'+'}] Initiating NULL Scan on {scanner.targIp}...\n")
        scanner.printResultsTable()
        scanner.nullScan()
    elif scanChoice == "6": # TCP ACK Scan
        print(f"\n[{'+',}] Initiating TCP ACK Scan on {scanner.targIp}...\n")
        scanner.printResultsTable()
        scanner.tcpACKScan()

    print(f"[{'+'}] Scan Complete!")