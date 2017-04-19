#!/usr/bin/evn python
# _*_ coding:utf-8 _*_


__author__ = 'tangcw'

import os
import random
import re
import sys
import shutil
import getopt



kvm_conf_old_file = ''
kvm_start_number = ''
kvm_start_name = ''
kvm_cp_number = ''

kvm_start_ip = ''
kvm_start_hostname = ''
kvm_gateway = ''


def Usage():
    print 'usage: scprit -n start_number -f kvm_old_file -s kvm_cp_number -h hostname -i ip -g gateway --name kvm_start_name'

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:f:n:s:i:g:",['help','name='])

    if len(sys.argv) <= 1:
        Usage()

    for op, value in opts:
        if op == '--help' or re.search(r'=.*',value):
            Usage()
        elif op == "-f":
            kvm_conf_old_file = value
        elif op == "-n":
            kvm_start_number = int(value)
        elif op == "-s":
            kvm_cp_number = int(value)
        elif op == '-i':
            kvm_start_ip = value
        elif op == '-h':
            kvm_start_hostname = value
        elif op == '-g':
            kvm_gateway = value
        elif op == '--name':
            kvm_start_name = value
       
except getopt.GetoptError:
    Usage()
    sys.exit()



def genmac(n):
    macstring = ''
    string_own = 'a9b1c2d3e4f5e6f7d8c9b0a8b7c6d5e4f3e2d1c4b6a7b8e21c0d'
    for i in range(n):
        macstring = macstring + string_own[random.randint(0,(len(string_own)-1))]
    return macstring


def getconf(file1,n):
    file_info = []
    img_info = []
    obj1 = re.search(r"(/.*/)(.*).xml",file1)
    old_file_name = obj1.group(2) + '.xml'
    new_file_name = kvm_start_name + str(n + kvm_start_number - 1) + '.xml'
    old_file_path = obj1.group(1)
    file_info = [ old_file_name,old_file_path,new_file_name ]
    with open(file1,'r') as f:
        for line in f.readlines():
	    m = re.search(r"<source file='(/.*/)(.*).qcow2'/>",line)
            if m:
                old_img_name = m.group(2) + '.qcow2'
                old_img_path = m.group(1)
                new_img_name = kvm_start_name + str(n + kvm_start_number - 1) + '.qcow2'
        img_info = [ old_img_name,old_img_path,new_img_name ]
    return file_info,img_info    
 
def cpfile(old_file,new_file):
    shutil.copyfile(old_file,new_file)

def genconf(name,n):
    filelist = []
    f = open(name,'r')
    for line in f.readlines():
        m1 = re.search(r'(<name>)(.*)(</name>)',line)
        m2 = re.search(r'(<uuid>)(.{8})-(.*)</uuid>',line)
        m3 = re.search(r"<source file='(/.*/)(.*).qcow2'/>",line)
        m4 = re.search(r"(<mac address='.*:)(.*)('/>)",line)
        m5 = re.search(r"(<graphics type='vnc' port=')(.*)(' autoport='no' listen='.*'>)",line)
        if m1:
            name_old = m1.group(2)
            name_new = kvm_start_name + str(n + kvm_start_number - 1)
            filelist.append(line.replace(name_old,name_new))
        elif m2:
            name_old = m2.group(2)
            macstr = genmac(8)
            filelist.append(line.replace(name_old,macstr))
        elif m3:
            name_old = m3.group(2)
            name_new = kvm_start_name + str(n + kvm_start_number - 1)
            filelist.append(line.replace(name_old,name_new))
        elif m4:
            if (int(m4.group(2)) + n + kvm_start_number - 1) < 10:
                name_old = m4.group(1) + m4.group(2)
                name_new = m4.group(1) + '0' + str(int(m4.group(2)) + n + kvm_start_number - 1)
                filelist.append(line.replace(name_old,name_new))
            else:
                name_old = m4.group(1) + m4.group(2)
                name_new = m4.group(1) + str(int(m4.group(2)) + n + kvm_start_number - 1)
                filelist.append(line.replace(name_old, name_new))
        elif m5:
            name_old = m5.group(2)
            name_new = str(int(m5.group(2)) + n + kvm_start_number - 1)
            filelist.append(line.replace(name_old,name_new))
        else:
            filelist.append(line)
    f.close()
    return filelist

conf = ['70-persistent-net.rules','hosts','ifcfg-eth0','network']
abs_conf = ['/etc/udev/rules.d/','/etc/','/etc/sysconfig/network-scripts/','/etc/sysconfig/']

def copyout(domain):
    print 'copy-out the files of config...'
    for item in range(len(abs_conf)):
        os.system('virt-copy-out -d %s %s ./' % (domain,(abs_conf[item])+conf[item]))

def copyin(domain):
    print 'copy-in the files of config...'
    for item in range(len(abs_conf)):
        os.system('virt-copy-in -d %s %s %s' % (domain,conf[item],abs_conf[item]))
        os.system('rm -rf %s' % conf[item])

def changeosfile(ip,number,gateway,hostname):
    #change mac
    #os.system('echo `cat 70-persistent-net.rules | grep ^[^#] | tail -1` > 70-persistent-net.rules')
    os.system('> 70-persistent-net.rules')

    #change hosts
    real_ip = re.search(r'(([0-9]{1,3}.){3})(.*)',ip).group(1) + str(int(re.search(r'(([0-9]{1,3}.){3})(.*)',ip).group(3)) + number)
    os.system("sed -i s'@IPADDR=.*@IPADDR=%s@g' ifcfg-eth0" % real_ip)

    #change gateway
    os.system("sed -i s'@GATEWAY=.*@GATEWAY=%s@g' ifcfg-eth0" % gateway)

    #change hostname
    real_hostname = hostname + real_ip.replace('.','-')
    os.system("sed -i s'@HOSTNAME=.*@HOSTNAME=%s@g' network" % real_hostname)

    #print hosts 
    hosts = real_ip + ' ' + real_hostname
    os.system("echo %s >> hosts" % hosts)




if __name__ == '__main__':

    #print kvm_start_ip
    #print kvm_start_hostname
    #print kvm_gateway
    if len(kvm_conf_old_file) != 0 and len(str(kvm_start_number)) != 0 and len(str(kvm_cp_number)) != 0 and len(kvm_start_name) != 0 and len(kvm_start_ip) != 0 and len(kvm_start_hostname) != 0 and len(kvm_gateway) != 0:

        for item in range(1,kvm_cp_number+1):
            file_info,img_info = getconf(kvm_conf_old_file,item)
            file_list = genconf(kvm_conf_old_file,item)
            new_conf_file = file_info[1] + file_info[2]
            with open(new_conf_file,'w+') as f:
                for i in file_list:
                    f.write(i)

            print 'cp:',img_info[1]+img_info[0],'to',img_info[1]+img_info[2]
            shutil.copyfile(img_info[1]+img_info[0],img_info[1]+img_info[2])
            #add kvm_instance to area
            os.system("virsh define %s" % new_conf_file)
            domain = re.search(r'/.*/(.*).xml',new_conf_file).group(1)
            copyout(domain) 
            changeosfile(kvm_start_ip,item-1,kvm_gateway,kvm_start_hostname)
            copyin(domain)
            os.system("virsh start %s" % domain)

    else:
        print 'invalid option or option more|less!'
        Usage()
