import ipaddress
import datetime
import multiprocessing
import os
import socket

# going to take 2 hours per /16 subnet

os.chdir('D:\\Python363\\projects\\STC_chassis_finder_2020\\working files\\20221011')
SUBNET = "10.108.8.0/25"


class STC_Finder():
    def portNumber(self, IP, num):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        #print("BEFORE sock.connect_ex: {}, {}".format(IP, num))
        portRes = sock.connect_ex((IP, num))
        sock.close()
        return portRes

    def portScanner(self, IP):
        # reference "startTime1" and "full path" returned from createFileName()
        stc_open_port_count = 0
        stc_open_ports = [22, 80, 111, 514, 2222]
        #print("type {}".format(type(self.portNumber(IP, 22))))
        for open_port in stc_open_ports:
            if self.portNumber(IP, open_port) == 0:
                print(f"{IP} : {open_port} is open")
                stc_open_port_count += 1
            else:
                break
        # write IP to file when all ports open
        if stc_open_port_count == len(stc_open_ports):
            print("All ports opened")
            with open(self.fullPathToResFile, 'a+') as results:
                results.write(IP + "\n")

    def write_to_txt(self, to_write):
        with open(self.fullPathToResFile, 'a+') as opened_file:
            opened_file.write(to_write)

    def createFileName(self):
        # filename to write to
        # return startTime1, fullPathToResFile # to calculate total time taken
        self.startTime1 = datetime.datetime.now()
        startTime2 = self.startTime1.strftime("%Y%m%d%H%M%S")
        resFile = "{}.txt".format(startTime2)
        # return startTime1, fullPathToResFile # to calculate total time taken
        self.fullPathToResFile = "results\\{}".format(resFile)
        # return startTime1, fullPathToResFile # to calculate total time taken
        # with open(self.fullPathToResFile, 'a+') as printStartTime:
        #     printStartTime.write("Start time: {}\n".format(startTime2))
        to_write = f"Start time: {startTime2}"
        self.write_to_txt(to_write)

    def endTimeStamp(self):
        # document end timings
        # startTime1, fullPathToResFile = createFileName() # reference "startTime1" and "full path" returned from createFileName()
        endTime1 = datetime.datetime.now()
        endTime2 = endTime1.strftime("%Y%m%d%H%M%S")
        printEndTime = "Time ended: {}".format(endTime2)
        printTimeTaken = "Total Time Taken: {}".format(
            endTime1 - self.startTime1)
        print(printEndTime)
        print(printTimeTaken)
        # write end times to file
        with open(self.fullPathToResFile, 'a+') as printStopTime:
            printStopTime.write(printEndTime + "\n")
            printStopTime.write(printTimeTaken + "\n")

    def __init__(self, IPLIST):
        # input IP to scan
        self.IPLIST = IPLIST
        self.main2()

    def main2(self):
        self.createFileName()   # create results output file
        for ip in self.IPLIST:
            self.portScanner(ip)    # scan ip and write to file if STC chassis
        self.endTimeStamp()         # document end time


class Hosts:
    def __init__(self, subnetList):
        self.subnetList = subnetList
        self.hosts2 = []  # file to store all hosts in subnetList
        self.ipList0 = []   # ipListx for mProcx
        self.ipList1 = []
        self.ipList2 = []
        self.ipList3 = []
        self.main2()

    def subnet_calc(self, subnet):
        hosts0 = ipaddress.ip_network(subnet).hosts()
        # creates a generator file, now lets put these in a list
        hosts1 = list(hosts0)
        # creates a list of class variables, now we need to change each class variable to string
        # now we create a new list host2 and convert host1 variables to string
        for i in range(0, len(hosts1)):
            self.hosts2.append(str(hosts1[i]))
        # print("self.host2 file has: {} items".format(len(self.hosts2)))
        # print(self.hosts2[-1])
    # print("hosts2 list has " + len(subnet_calc) + " items")

    def division(self):
        totalNum = len(self.hosts2)
        quarter = int(totalNum / 4)
        start = ["0", quarter, quarter * 2, quarter * 3]
        end = [quarter, quarter * 2, quarter * 3, totalNum]
        '''Make 4 ipLists for 4 processors'''
        ipList0 = []
        ipList1 = []
        ipList2 = []
        ipList3 = []
        for i in range(int(start[0]), int(end[0])):
            ipList0.append(self.hosts2[i])
        for i in range(int(start[1]), int(end[1])):
            ipList1.append(self.hosts2[i])
        for i in range(int(start[2]), int(end[2])):
            ipList2.append(self.hosts2[i])
        for i in range(int(start[3]), int(end[3])):
            ipList3.append(self.hosts2[i])
        # print(ipList2[-1])
        self.ipList0 = ipList0
        self.ipList1 = ipList1
        self.ipList2 = ipList2
        self.ipList3 = ipList3

    def main2(self):
        # print("Hosts Class.main subnetList: {}".format(self.subnetList))
        for subnet in self.subnetList:
            self.subnet_calc(subnet)
        self.division()


def mProc0():
    # STC_Finder(Hosts(["10.108.0.0/16", "10.109.0.0/16", "10.6.0.0/16"]).ipList0)
    STC_Finder(Hosts(["10.108.8.0/25", "10.109.51.128/25"]).ipList0)
    # STC_Finder(Hosts(["10.64.101.0/28"]).ipList0)


def mProc1():
    # STC_Finder(Hosts(["10.108.0.0/16", "10.109.0.0/16", "10.6.0.0/16"]).ipList1)
    STC_Finder(Hosts(["10.108.8.0/25", "10.109.51.128/25"]).ipList1)
    # STC_Finder(Hosts(["10.64.101.0/28"]).ipList1)


def mProc2():
    # STC_Finder(Hosts(["10.108.0.0/16", "10.109.0.0/16", "10.6.0.0/16"]).ipList1)
    STC_Finder(Hosts(["10.108.8.0/25", "10.109.51.128/25"]).ipList2)
    # STC_Finder(Hosts(["10.64.101.0/28"]).ipList2)


def mProc3():
    # STC_Finder(Hosts(["10.108.0.0/16", "10.109.0.0/16", "10.6.0.0/16"]).ipList1)
    STC_Finder(Hosts(["10.108.8.0/25", "10.109.51.128/25"]).ipList3)
    # STC_Finder(Hosts(["10.64.101.0/28"]).ipList3)


if __name__ == '__main__':
    # SUBNETS = ["10.108.0.0/16", "10.109.0.0/16", "10.6.0.0/16"]
    SUBNETS = ["10.108.8.0/25", "10.109.51.128/25"]
    h1 = Hosts(SUBNETS)

    """Create global IP lists"""
    # ipList0 = Hosts(SUBNETS).ipList0
    # ipList1 = Hosts(SUBNETS).ipList1
    # ipList2 = Hosts(SUBNETS).ipList2
    # ipList3 = Hosts(SUBNETS).ipList3

    ipList0 = h1.ipList0
    ipList1 = h1.ipList1
    ipList2 = h1.ipList2
    ipList3 = h1.ipList3

    # ipListMain = [ipList0, ipList1, ipList2, ipList3]

    #mProcMain = [mProc0(), mProc1(), mProc2(), mProc3()]

    print("global ipList0 length: {}".format(len(ipList0)))
    print("global ipList1 length: {}".format(len(ipList1)))
    print("global ipList2 length: {}".format(len(ipList2)))
    print("global ipList3 length: {}".format(len(ipList3)))

    # """mProc loop start 1"""
    # jobs = []
    # for z in (mProc0, mProc1, mProc2, mProc3):
    #     j = multiprocessing.Process(target=z)
    #     jobs.append(j)
    #     j.start()
    #     print("started job: {}".format(j.name))
    # print(jobs)
    #
    # for j in jobs:
    #     j.join()

    """mProc start using args"""
    jobs = []
    for z in (mProc0, mProc1, mProc2, mProc3):
        j = multiprocessing.Process(target=z)
        jobs.append(j)
        j.start()
        print("job started: {}".format(j.name))

    for j in jobs:
        j.join()
