#!/usr/bin/python

import subprocess
import os
import re
import ConfigParser
import logging
import struct

src_port = "" 
dst_host = ""
dst_port = "" 

# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.FileHandler("water.log")
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
logging.debug("ttttt")

def main():
    #0. init some value
    first = 1
    status = "info"
    data = ""

    #for re
    ip_line = r'.*IP (\d+\.\d+\.\d+\.\d+)\.(\d+)'
    data_line = r'.{10}(.{39})  (.{1,16})'
    line_num = 0

    #1. parser config
    config = ConfigParser.ConfigParser() 
    with open("./config", "rw") as cfg:
        config.readfp(cfg)
        src_host = config.get("config", "src_host")
        src_port = config.get("config", "src_port")
        dst_host = config.get("config", "dst_host")
        dst_port = config.get("config", "dst_port")
    logging.debug('src=%s:%s,dst=%s:%s',src_host, src_port, dst_host, dst_port)

    #2. start subprocess tcpdump
    cmd = "tcpdump -i any -nn -Xs0 tcp" 
    if src_host != "0":
        cmd = cmd + " and host " + src_host
    if src_port != "0":
        cmd = cmd + " and port " + src_port

    logging.debug('cmd = %s', cmd)
    #output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        fd = os.open("./test.udp", os.O_RDONLY)
        file = os.fdopen(fd)
    except KeyboardInterrupt:
        logging.error("file error")

    #3. process tcpdump data

    while True:
        #line = output.stdout.readline()
        line = file.readline()
        if not line:
            break

        #print line
        if status == "info" and first == 1:
            info_data = re.compile(ip_line).match(line)
            if info_data:
                from_ip = info_data.group(1)
                from_port = info_data.group(2)
                first = 0
                line_num = 0
                status = "head"
                #if from_port != src_port:
                #    first = 1
                #    status = "info"
                logging.debug("from_addr=%s:%s, status=%s, first = %d", from_ip, from_port, status, first)

        elif status == "head" and first == 0:
            head_data = re.compile(data_line).match(line)
            if head_data:
                print head_data.group(1)

        #elif status == "data":

    


if __name__ == "__main__":
    main()
