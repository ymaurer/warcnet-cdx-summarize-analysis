#!/usr/bin/python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
import csv
from pathlib import Path
import json
import re

min_year = 1993
max_year = 2021
allfields = ["audio","css","font","html","image","js","json","pdf","video"]
reArchive = re.compile(r'(?P<archive>...[^\-]*)\-.*')

def read_averages(file, field, delim=',', minimum=1):
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=delim)
        output = {}
        for row in reader:
            if len(row) >= 5 and row[1] == field and row[0] != 'Total':
                year = int(row[0])
                if year >= min_year and year <= max_year and int(row[3]) >= minimum and int(row[4]) > 0:
                    output[int(row[0])] = int(row[3])
    return output

def all_averages(dir, field, delim=',', minimum=1):
    retval = {}
    p = Path(dir[0])
    for f in p.iterdir():
        o = read_averages(f, field, delim, minimum)
        m = reArchive.match(f.name)
        if m:
            retval[m.groupdict()['archive']] = o
    return retval

def line_plot(series, field):
    fig, ax = plt.subplots()
    x = np.arange(min_year, max_year + 1)
    for archive in series:
        yvalues = []
        for year in x:
            if year in series[archive]:
                yvalues.append(series[archive][year])
            else:
                yvalues.append(0)
        ax.plot(x, yvalues, label=archive)
    ax.set_title(f'Average size of {field}')
    ax.legend(title='Archive')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average size in bytes')
    fig.savefig(f'linechart-{field}.png', dpi=300)

def scatter_plot(series, field):
    fig, ax = plt.subplots()
    for archive in series:
        xvalues = []
        yvalues = []
        for year in series[archive]:
            xvalues.append(year)
            yvalues.append(series[archive][year])
        ax.scatter(xvalues, yvalues, label=archive)
    ax.legend(title='Archive')
    ax.set_title(f'Average size of {field}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average size in bytes')
    print(f'saved scatter-{field}.png')
    fig.savefig(f'scatter-{field}.png', dpi=300)

if __name__ == '__main__':
    parser = ArgumentParser(description='Plot the averages')
    parser.add_argument('--field', action='store', help='which field to plot (e.g. html)')
    parser.add_argument('dir', nargs=1, help='directory with csv files')
    args = parser.parse_args()
    for field in allfields:
        scatter_plot(all_averages(args.dir, field, ',', 1000), field)