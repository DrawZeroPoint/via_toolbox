import os
import sys

lines = os.listdir('/home/gy/Database/Done/grape/voc/JPEGImages')
lines = [os.path.splitext(line)[0] + '\n' for line in lines]
outfile = '/home/gy/Database/Done/grape/voc/out.txt'

with open(outfile, "a") as f:
    for line in lines:
        print(line)
        f.write(line)