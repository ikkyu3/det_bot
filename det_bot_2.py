import pprint
import json
import sys
import argparse
import os
import numpy as np
import time
import datetime

args = argparse.ArgumentParser()
args.add_argument("target")
args = args.parse_args()


row_list = []
t_list = {}
res_list = {}
for root, dirs, files in os.walk(args.target):
    for file_name in files:
            file_name = os.path.join(root, file_name)
            with open(file_name, encoding="utf8", errors='ignore') as f:
                try:
                    for row in f:
                        row_list.append(json.loads(row))
                except Exception:
                    pass
                for data in row_list:
                    comm = data["timestamp"]
                    comm = comm + "Z"
                    datetime.datetime.strptime(comm, '%Y-%m-%dT%H:%M:%S.%fZ')
                    s_ip = data["src_ip"]
                    if s_ip not in t_list:
                        t_list[s_ip] = []
                    t_list[s_ip].append(comm)

                    print("getting the log data from ip:"+s_ip)


tmp_list = []
t_delta = []
human_list = {}
##############
print(t_list)
for ttime in t_list:
    try:
        tmp_list = t_list[ttime]
        tmp_list = sorted(tmp_list)
        print("ip毎のアクセス時間")
        print("-----------------------------")
        print(tmp_list)
        print(" ")
        print("時差のリスト")
        print("------------------------------")
        for i in range(len(tmp_list)-1):
            tmp_delta = datetime.datetime.strptime(tmp_list[i+1], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime.strptime(tmp_list[i], '%Y-%m-%dT%H:%M:%S.%fZ')
            t_delta.append(tmp_delta.microseconds)
        print(t_delta)
        print(" ")
        Min_t = min(t_delta)
        print("ip毎の最小時間")
        print("-------------------------")
        print(Min_t)
        ###############
        if Min_t > 0:
            human_list[ttime] = Min_t
        print(" ")
        res_list[ttime] = Min_t 
                           
        t_delta = []
    except Exception:
        pass


print("ip:最小時間")
print("-------------------------")
print(res_list)
print(" ")
print("botではない可能性あり")
pprint.pprint(human_list)
