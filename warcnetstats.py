#!/usr/bin/python3
from argparse import ArgumentParser
import re
import json

EXPLICITIPV4 = 'explitipv4'
reSummaryLine = re.compile(r'((?P<host>.*)\.)?(?P<lvl2>[^\.]*)\.(?P<tld>[^\ ]*) (?P<data>.*)')

stata_domains = set()
stata_domains_py = {}
statb_tlds = set()
statb_tld_py = {}
statc_domains = {}
statc_domains_py = {}

def calc_stata(lvl2, tld, years):
    stata_domains.add(lvl2 + '.' + tld)
    for y in years:
        if not y in stata_domains_py:
            stata_domains_py[y] = set()
        stata_domains_py[y].add(lvl2 + '.' + tld)

def output_stata(args):
    fname = args.prefix
    with open(fname + "-stata-distinct-domains-overall.csv", 'w') as fil:
        fil.write(f'{len(stata_domains)}')
    with open(fname + "-stata-distinct-domains-per-year.csv", 'w') as fil:
        for y in sorted(stata_domains_py):
            fil.write(f'{y}{args.delimiter}{len(stata_domains_py[y])}\n')

def calc_statb(lvl2, tld, years):
    statb_tlds.add(tld)
    for y in years:
        if not y in statb_tld_py:
            statb_tld_py[y] = set()
        statb_tld_py[y].add(tld)

def output_statb(args):
    fname = args.prefix
    with open(fname + "-statb-distinct-tld-overall.csv", 'w') as fil:
        fil.write(f'{len(stata_domains)}')
    with open(fname + "-statb-distinct-tld-per-year.csv", 'w') as fil:
        for y in sorted(statb_tld_py):
            fil.write(f'{y}{args.delimiter}{len(statb_tld_py[y])}\n')

def calc_statc(lvl2, tld, years):
    if not tld in statc_domains:
        statc_domains[tld] = 0
        statc_domains_py[tld] = {}
    statc_domains[tld] = statc_domains[tld] + 1
    for y in years:
        inty = int(y)
        if not inty in statc_domains_py[tld]:
            statc_domains_py[tld][inty] = 0
        statc_domains_py[tld][inty] = statc_domains_py[tld][inty] + 1

def output_statc(args):
    fname = args.prefix
    sorted_statc_domains = dict(sorted(statc_domains.items(), key=lambda x: x[1], reverse=True))
    with open(fname + "-statc-distinct-lvl2-per-tld-overall.csv", 'w') as fil:
        for tld in sorted_statc_domains:
            fil.write(f'{tld}{args.delimiter}{sorted_statc_domains[tld]}\n')
    sorted_statc_domains_py = dict(sorted(statc_domains_py.items(), key=lambda x: sum(x[1].values()), reverse=True))
    with open(fname + "-statc-distinct-lvl2-per-tld-per-year.csv", 'w') as fil:
        fil.write(f'tld')
        for y in range(int(args.minyear), int(args.maxyear) + 1):
            fil.write(f'{args.delimiter}{y}')
        fil.write('\n')
        for tld in sorted_statc_domains_py:
            fil.write(f'{tld}')
            for y in range(int(args.minyear), int(args.maxyear) + 1):
                if y in statc_domains_py[tld]:
                    fil.write(f'{args.delimiter}{statc_domains_py[tld][y]}')
                else:
                    fil.write(f'{args.delimiter}0')
            fil.write('\n')

def dowork(args):
    with open(args.file[0]) as fil:
        for line in fil:
            m = reSummaryLine.match(line)
            if m:
                tld = m.groupdict()['tld']
                lvl2 = m.groupdict()['lvl2']
                years = json.loads(m.groupdict()['data'])
                if lvl2.isdigit() and tld.isdigit():
                    tld = EXPLICITIPV4
                    lvl2 = '0'
                calc_stata(lvl2, tld, years)
                calc_statb(lvl2, tld, years)
                calc_statc(lvl2, tld, years)
    output_stata(args)
    output_statb(args)
    output_statc(args)


if __name__ == '__main__':
    parser = ArgumentParser(description='Calculate Warcnet chapter statistics from summary file')
    parser.add_argument('--prefix', action="store", help='prefix of the output file')
    parser.add_argument('--minyear', action="store", default=1993, help='Minimum Year for statc: Number of distinct domains on TLDs per year report')
    parser.add_argument('--maxyear', action="store", default=2023, help='Maximum Year for statc: Number of distinct domains on TLDs per year report')
    parser.add_argument('--delimiter', action="store", default=',', help='Output file delimiter for csv files')
    parser.add_argument('file', nargs=1, help='summary file')
    args = parser.parse_args()
    dowork(args)