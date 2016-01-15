#! /usr/bin/python3

# Libraries imported
# Files needed in logs folder: leases,IP_neigh_show,uptime,version,DFS,wl0_status,wl1_status,dhcp.conf,wl0_assoclist,wl1_assoclist,con_status


import itertools as it # for groupby related code
from lib2to3.pgen2.token import LESS
import string # for string operations
import re # for regular expression operations
import os
import sys
from tkinter.filedialog import *
from prettytable import PrettyTable
import csv


# Function to retrieve a list of indeces which has the search term. IF not found, the list will be return [] 
def substring(mystr, mylist): return [i for i, val in enumerate(mylist) if mystr in val]


def DHCP_leases(Logs_folder): 
    #Declaration of variables
    # 
    Lease_file = os.path.join(Logs_folder,'config','dhcpd','leases')
    address_IP = []
    Lease_chunks = []
    DHCP_Lease = []
    IP_list = []
    Mac_list = []
    Vendor_string = []
    Hostname = []
    DeviceProductClass = []
    DeviceSerialNumber = []
    DeviceManufacturerOUI = []

    
#Copy leases file into a list
    try:
        inputtext = open(Lease_file,'r')
        data_list = inputtext.readlines()
        inputtext.close() 
    
        #Remove header/emptyspaces and then add } at start of file for chunck seperation
    
        del data_list[0:3]
        data_list.insert(0,"}\n")
    
        for i, c in enumerate(data_list): 
            if c.startswith('server-duid',0,15):
                 del data_list[i]
            if c == '\n':
                 del data_list[i]
        
        outfilename = os.path.join(Logs_folder,'outleases')
        outputtext = open(outfilename,'w')    
        outputtext.writelines(data_list)
        outputtext.close()
    
        with open(outfilename,'r') as f:
            for key,group in it.groupby(f,lambda line: line.startswith('}',0, 2)):         
                if not key:
                    group = list(group)
                    Lease_chunks.append(group)
    
    
        #
        for i in range(len(Lease_chunks)):
            for j in range(len(Lease_chunks[i])):
            
                Lease_chunks[i][j] = Lease_chunks[i][j].replace(';', '')
                Lease_chunks[i][j] = Lease_chunks[i][j].replace('{','')
                Lease_chunks[i][j] = Lease_chunks[i][j].replace('}','')
                Lease_chunks[i][j] = Lease_chunks[i][j].replace('\n','')
       
        # Format the output table for information on output clients
        for i in range(len(Lease_chunks)): 
        
            Ips = substring("lease",Lease_chunks[i])
            Mac_add = substring("hardware",Lease_chunks[i])
            venstring = substring("vendor-string",Lease_chunks[i])
            hostnam = substring("hostname",Lease_chunks[i])
            DevProClass = substring("DeviceProductClass",Lease_chunks[i])
            DevSerNum = substring("DeviceSerialNumber",Lease_chunks[i])
            DevManOUI = substring("DeviceManufacturerOUI",Lease_chunks[i])
          
            if len(Ips) != 0:   
             IP_list.append((Lease_chunks[i][Ips[0]]).split()[1])       
            else:     
             IP_list.append('')      
         
            if len(Mac_add) != 0:
             Mac_list.append((Lease_chunks[i][Mac_add[0]]).split()[2])
            else:
             Mac_list.append('')
         
            if len(venstring) != 0:     
             Vendor_string.append((re.findall('"([^"]*)"',Lease_chunks[i][venstring[0]])[0]))     
            else:
             Vendor_string.append('')
          
            if len(hostnam) != 0:    
             Hostname.append((re.findall('"([^"]*)"',Lease_chunks[i][hostnam[0]])[0]))
            else:
             Hostname.append('')
    
            if len(DevProClass) != 0:    
             DeviceProductClass.append((re.findall('"([^"]*)"',Lease_chunks[i][DevProClass[0]])[0]))
            else:
             DeviceProductClass.append('')
         
            if len(DevSerNum) != 0:    
             DeviceSerialNumber.append((re.findall('"([^"]*)"',Lease_chunks[i][DevSerNum[0]])[0]))
            else:
             DeviceSerialNumber.append('') 
    
            if len(DevManOUI) != 0:    
             DeviceManufacturerOUI.append((re.findall('"([^"]*)"',Lease_chunks[i][DevManOUI[0]])[0]))
            else:
             DeviceManufacturerOUI.append('')

        List_2G,List_5G = Assoc_list(Logs_folder)
        List_wireless = ['']*len(Mac_list)
        
        for i, c in enumerate(Mac_list):     
            for j in List_2G:
                if j.lower() == c.lower():
                    List_wireless[i] = '2.4G'
        
        for i, c in enumerate(Mac_list):     
            for j in List_5G:
                if j.lower() == c.lower():
                    List_wireless[i] = '5G'
        
#                                
        DHCP_profile = [list(a) for a in zip(IP_list, Mac_list,List_wireless, Vendor_string, Hostname, DeviceProductClass, DeviceSerialNumber, DeviceManufacturerOUI)]
        return(DHCP_profile)
    except:
        print("lease file not found")
        return([])
     
def print_table(table, header, type, write_summary):
    
#Prints a 2D list as a formatted table 
    if table == []:
        write_summary.write(str("No devices listed"))
        write_summary.write(str('\n'))
    else:
        if type == 'Wireless':
            prettys = PrettyTable(header)

            
            for i,c in enumerate(table):               
                if i == 0:
                    c.insert(0,'5 GHz')
                    prettys.add_row(c)
                if i == 1:
                    c.insert(0,'2.4GHz')
                    prettys.add_row(c)
        else:    
            prettys = PrettyTable(header)
            for i,c in enumerate(table):
                prettys.add_row(c)
                    
        prettys.padding_width = 1        
        # write the output to a file. A common output that needs to be changed.
        
    try:
        write_summary.write(str(prettys))
        
    except:
        print("nothing")

def neighbours(Logs_folder):

    neigh = os.path.join(Logs_folder,'IP_neigh_show')
    IP_list = []
    Device_status = []
    inputtext = open(neigh,'r')
    data_list = inputtext.readlines()
    inputtext.close()


    for i, c in enumerate(data_list):
         IP_list.append(c.split()[0])
         Device_status.append(c.split()[-1])
#
    IP_neig = [list(a) for a in zip(IP_list,Device_status)]
    return(IP_neig)


def devices_status(Wireless_profile,IP_neig):
    
    Nonactive_list = []
    Stale_list = []
    Active_list = []
    Delay_list = []

    Active_devices = []
    Stale_devices = []
    Nonactive_devices = []
    Delay_devices = []
    Unlisted = []
    foundit = []
    
    for i,c in enumerate(IP_neig):
        if c[1] == 'FAILED':
            Nonactive_list.append(c[0])
        if c[1] == 'STALE':
            Stale_list.append(c[0])
        if c[1] == 'REACHABLE':
            Active_list.append(c[0])
        if c[1] == 'DELAY':
            Delay_list.append(c[0])    

#
 
    found_list = Active_list+Stale_list+Nonactive_list+Delay_list

             
    for i,c in enumerate(Active_list):
        for j in Wireless_profile:
            if c == j[0]:
              Active_devices.append(j)
    for i,c in enumerate(Stale_list):
        for j in Wireless_profile:
            if c == j[0]:
                Stale_devices.append(j)
    for i,c in enumerate(Nonactive_list):
        for j in Wireless_profile:
            if c == j[0]:
                Nonactive_devices.append(j)
    for i,c in enumerate(Delay_list):
        for j in Wireless_profile:
            if c == j[0]:
                Delay_devices.append(j)
    for i,c in enumerate(Wireless_profile):
        del foundit[:]
        for j in found_list:
            if c[0] == j:
                foundit.append('found')
            else:
                foundit.append('not')
        
        if 'found' not in foundit:
            Unlisted.append(c)
#
    return(Active_devices,Stale_devices,Nonactive_devices,Delay_devices,Unlisted) 


def header_add(device_list, header_type):
 
    if device_list != []:
        if header_type == 'DHCP_leases':
            header = ['IP addr', 'Mac addr', 'Network','Vendor', 'Host Name', 'DeviceProductClass', 'DeviceSerialNumber', 'DeviceManufacturerOUI']
            return(header)
        if header_type == 'Wireless':
            header = ['Network','SSID','Noise','Current Channel','Mode','Int. Mac ID','Channel selection']
            return(header)
        if header_type == 'static_ips':
            header = ['Hostname','Mac add','Static IP']
            return(header)
        if header_type == 'conn_type':
            header = ['Interface name','Mac add','IP add','Broadcast add','Subnet mask','IPv6 add']
            return(header)
    else:
        return([])


def wirelessstatus(status_input, ACS,frequency):
    
    status_info = []
    for i, c in enumerate(status_input): 

        if 'SSID' in c:
            if re.findall('\\bSSID\\b', c) != []:               
                status_info.append(re.findall('"([^"]*)"', c)[0]) 
 
        if 'BSSID' in c:
            status_info.append(c.split()[1])
        if 'Channel' in c:
            if c.split()[1] == 'Managed':
                status_info.append(c.split()[9])
                status_info.append(c.split()[12])
                status_info.append('Managed')
            else:    
                status_info.append(c.split()[10])
                status_info.append(c.split()[13])
                status_info.append('Ad hoc')
    for i, c in enumerate(ACS):
        DFS = frequency
        if DFS in c:
            if c[13] == '0':              
                status_info.append('Auto')
            else:
                status_info.append('Manual')
    
    return(status_info)        

def Static_ips(Logs_folder):
     
 
    DHCP_conf = os.path.join(Logs_folder,'dhcpd','dhcpd.conf')
 
    host_list = []
    static_IPs = []
    try:
        inputtext = open(DHCP_conf,'r')
        data_list = inputtext.readlines()
        inputtext.close()
         
        for i,c in enumerate(data_list):
            if 'host' in c:                 
                host_list.append(i)
 
    except:
        print('Static IPs file not found')
     
 
    for i,c in enumerate(host_list):
        static_IPs.append([data_list[c].split()[1],data_list[c+1].split()[2],data_list[c+2].split()[1]])      
    return(static_IPs)


def Assoc_list(Logs_folder):
    
    List_5G = []
    List_2G = []
    try:
        Assoc5G_input = open(os.path.join(Logs_folder,'wl0_assoclist'),'r')
        Assoc5G = Assoc5G_input.readlines()
        Assoc5G_input.close()
        if Assoc5G != []:
            for i,c in enumerate(Assoc5G):
                List_5G.append(c.split()[1])       
    
        Assoc2G_input = open(os.path.join(Logs_folder,'wl1_assoclist'),'r')
        Assoc2G = Assoc2G_input.readlines()
        Assoc2G_input.close()
        if Assoc2G != []:
            for i,c in enumerate(Assoc2G):
                List_2G.append(c.split()[1])         
    except:
        print('5Gz assoclist file not found')    
  
    return(List_2G,List_5G)


def Connection_status(Logs_folder):
    
   
    constatus_input = os.path.join(Logs_folder,'con_status')
    host_list = []
    Lease_chunks = []
    Inter_name = []
    Hardware_macadd = []
    leng = 0
    try:
        inputtext = open(constatus_input,'r')
        con_status = inputtext.readlines()
        inputtext.close()
        interfaces = ['br-guest','br-lan','eth0','eth1','eth2','eth2.1','eth2.2','lo','wl0','wl0.1','wl1','wl1.1']
            
        for i, c in enumerate(con_status):
            if c == '\n':
                con_status[i] = '}' + c
            elif c.split()[0] in interfaces:
                con_status[i] = '{' + c
                
        outputtext = open(constatus_input,'w')
        outputtext.writelines(con_status)
        outputtext.close()    
        
        with open(constatus_input,'r') as f:
     
            for key,group in it.groupby(f,lambda line: line.startswith('}',0, 2)):         
                if not key:
                    group = list(group)
                    Lease_chunks.append(group)
         
        for i,c in enumerate(interfaces):
            for j,k in enumerate(Lease_chunks):
                elem = c + ' '
                if re.search(elem ,Lease_chunks[j][0]):
                    leng = leng+1 
         
        IP_add = [''] * leng
        Broadcast_add = [''] * leng
        Subnet_mask = [''] * leng
        IPv6_add = [''] * leng
        
        for i,c in enumerate(interfaces):
            for j,k in enumerate(Lease_chunks):
                elem = c + ' '
                if elem in Lease_chunks[j][0]:
                    if 'HWaddr' in Lease_chunks[j][0]:
                        Inter_name.append(c)
                        Hardware_macadd.append(Lease_chunks[j][0].split()[-1])
                        
                        for w, z in enumerate(Lease_chunks[j]):
    
                            if 'inet ' in Lease_chunks[j][w]:
                                IP_add.insert(j,Lease_chunks[j][w].split()[1][5:])
                                Broadcast_add.insert(j,Lease_chunks[j][w].split()[2][6:])
                                Subnet_mask.insert(j, Lease_chunks[j][w].split()[3][5:])
    
                            if 'inet6 ' in Lease_chunks[j][w]:
                                IPv6_add.insert(j,Lease_chunks[j][w].split()[2])

    
        conn_type = [list(a) for a in zip(Inter_name,Hardware_macadd,IP_add,Broadcast_add,Subnet_mask,IPv6_add)]
        return(conn_type)
    
    except:
        print('Interfaces file not found')
        return([])


def Meminfo(Logs_folder):
    Mem_array = []
    Meminfo_input = os.path.join(Logs_folder,'meminfo')
    
    Meminfo = open(Meminfo_input,'r').readlines()
    for i, c in enumerate(Meminfo):
    #Add in the number of lines from the meminfo file that needs to be displayed
        if i in [0,1,2,3,13,14,30,31,32]:
            Mem_array.append(c)
            
    return(Mem_array)

# Main call function 
def Main():

    Logs_folder = askdirectory()
    Wireless_profile = []
    
    try:
        
        write_summary = open(os.path.join(Logs_folder,'Router_summary'),'a')
        
        try: 
            uptime_input = open(os.path.join(Logs_folder,'uptime'),'r')
            uptime = uptime_input.readlines()
            uptime_input.close()
            write_summary.write(str('Router uptime is: ')) 
            write_summary.write(uptime[0])
            write_summary.write(str('\n'))
            write_summary.write(str('\n'))
        
        except:
            write_summary.write(str('Uptime file was not found'))  
            write_summary.write(str('\n'))
            write_summary.write(str('\n'))      
    
        try: 
            version_input = open(os.path.join(Logs_folder,'version'),'r')
            version = version_input.readlines()
            version_input.close()
            print(version[0])
            write_summary.write(str('FW version: '))
            write_summary.write(version[0])
            write_summary.write(str('\n'))
        except:
            write_summary.write(str('Version file was not found'))  
            write_summary.write(str('\n'))

        write_summary.write('MEMORY STATUS\n')
        Mems = Meminfo(Logs_folder)
        for item in Meminfo(Logs_folder):
            write_summary.write(str(item))
            
        write_summary.write(str('\n'))
        write_summary.write(str('\n'))
        write_summary.write(str('INTERFACES SUMMARY'))
        write_summary.write(str('\n'))
             
        try:
            conn_type = Connection_status(Logs_folder)       
              
            print_table(conn_type, header_add(conn_type,'conn_type'), 'conn_type',write_summary)
            write_summary.write(str('\n'))
            write_summary.write(str('\n'))
        except:
            write_summary.write(str("DHCP.conf file not found"))
            write_summary.write(str('\n'))
            write_summary.write(str('\n')) 
            
           
            
        write_summary.write(str("Wireless profile: "))
        write_summary.write(str('\n'))

        try:
            ACS_input = open(os.path.join(Logs_folder,'DFS'),'r')
            ACS = ACS_input.readlines()       
        
            try:
                fiveghz_input = open(os.path.join(Logs_folder,'wl0_status'),'r')
                fiveghz = fiveghz_input.readlines()
                fiveghz_status = wirelessstatus(fiveghz, ACS,'wl0')          
    #            str = 'The SSID for the 5GHz network is {0}, current channel is {2}. Channel selection is {4}. Mac Id is {3}. Noise floor is at {1}'
            except:
                write_summary.write(str("5Ghz status not found"))
                write_summary.write(str('\n'))
                write_summary.write(str('\n'))
            
            try:
                twoghz_input= open(os.path.join(Logs_folder,'wl1_status'),'r')
                twoghz = twoghz_input.readlines()
                twoghz_status = wirelessstatus(twoghz, ACS,'wl1')
     #           str = 'The SSID for the 2.4GHz network is {0}, current channel is {2}. Channel selection is {4}. Mac Id is {3}. Noise floor is at {1}'
     #           print(str.format(*twoghz_status))
            except: 
                write_summary.write(str("2Ghz status not found"))
                write_summary.write(str('\n'))
                write_summary.write(str('\n'))
                
                
            Wireless_profile.append(fiveghz_status)
            Wireless_profile.append(twoghz_status)
            print_table(Wireless_profile, header_add(Wireless_profile,'Wireless'),'Wireless', write_summary)
            write_summary.write(str('\n'))
            write_summary.write(str('\n'))
            ACS_input.close()
        except: 
            write_summary.write(str("The DFS file is missing from logs"))
            write_summary.write(str('\n'))
            write_summary.write(str('\n'))
    
    #
        print('')
        DHCP_profile = DHCP_leases(Logs_folder)
    
        IP_neig = neighbours(Logs_folder)
    
     
        DeviceStatus = devices_status(DHCP_profile,IP_neig); 
        
        write_summary.write(str('Active Devices'))
        write_summary.write(str('\n'))   
        print_table(DeviceStatus[0], header_add(DeviceStatus[0],'DHCP_leases'),'DHCP_leases', write_summary)
        write_summary.write(str('\n'))
        
        write_summary.write(str('Stale Devices'))
        write_summary.write(str('\n'))
        print_table(DeviceStatus[1], header_add(DeviceStatus[1],'DHCP_leases'),'DHCP_leases', write_summary)
        write_summary.write(str('\n'))
      
        write_summary.write(str('Non Active devices'))
        write_summary.write(str('\n'))
        print_table(DeviceStatus[2], header_add(DeviceStatus[2],'DHCP_leases'),'DHCP_leases', write_summary)
        write_summary.write(str('\n'))
        
        write_summary.write(str('Delay devices'))
        write_summary.write(str('\n'))
        print_table(DeviceStatus[3], header_add(DeviceStatus[3],'DHCP_leases'),'DHCP_leases', write_summary)
        write_summary.write(str('\n'))
        
        write_summary.write(str('Unlisted devices'))
        write_summary.write(str('\n'))
        print_table(DeviceStatus[4], header_add(DeviceStatus[4], 'DHCP_leases'), 'DHCP_leases', write_summary)
        write_summary.write(str('\n'))
    

        write_summary.write(str('Static IPs assignment'))
        write_summary.write(str('\n'))
    
        try:
            static_ips = Static_ips(Logs_folder)       
               
            print_table(static_ips, header_add(static_ips,'static_ips'), 'static_ips', write_summary)
        except:
            write_summary.write(str("DHCP.conf file not found"))
            write_summary.write(str('\n'))
            
         
        write_summary.close()
            
    except:
        
        print("Cannot open summary file")

if __name__ == "__main__": 
    Main() 