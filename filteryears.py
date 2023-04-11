#!/usr/bin/python3
from argparse import ArgumentParser
import re
import json

EXPLICITIPV4 = '0.explitipv4'
reSummaryLine = re.compile(r'(?P<hostname>[^\ ]*) (?P<data>.*)')
reWrongHostname = re.compile(r'.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\/.*)?')

def dowork(args):
    with open(args.file[0]) as fil:
        for line in fil:
            m = reSummaryLine.match(line)
            if m:
                years = json.loads(m.groupdict()['data'])
                newyears = {}
                for y in years:
                    if int(y) >= int(args.minyear) and int(y) <= int(args.maxyear):
                        newyears[y] = years[y]
                if len(newyears) > 0:
                    hostname = m.groupdict()['hostname']
                    m1 = reWrongHostname.match(hostname)
                    if m1:
                        print(EXPLICITIPV4 + ' ' + json.dumps(newyears))
                    else:
                        print(hostname + ' ' + json.dumps(newyears))

if __name__ == '__main__':
    parser = ArgumentParser(description='Filter years from summary file')
    parser.add_argument('--minyear', action="store", default=1993, help='Minimum Year to include')
    parser.add_argument('--maxyear', action="store", default=2023, help='Maximum Year to include')
    parser.add_argument('file', nargs=1, help='summary file')
    args = parser.parse_args()
    dowork(args)