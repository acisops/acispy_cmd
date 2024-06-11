#!/usr/bin/env python

import matplotlib
import matplotlib.pyplot as plt
import argparse
import acispy
from acispy.utils import state_labels, mylog
matplotlib.use("Qt5Agg")

def main():
    
    parser = argparse.ArgumentParser(description='Plot a single MSID with another MSID or state')
    parser.add_argument("tstart", type=str, help='The start time in YYYY:DOY:HH:MM:SS format')
    parser.add_argument("tstop", type=str, help='The stop time in YYYY:DOY:HH:MM:SS format')
    parser.add_argument("y_axis", type=str, help='The MSID to be plotted on the left y-axis')
    parser.add_argument("--y2_axis", type=str, help='The MSID or state to be plotted on the right y-axis (default: none)')
    parser.add_argument("--maude", action="store_true", help="Use MAUDE to get telemetry data.")
    args = parser.parse_args()
    
    msids = []
    states = []
    
    if args.y_axis in state_labels:
        y_axis = ("states", args.y_axis)
    else:
        msids.append(args.y_axis)
        y_axis = ("msids", args.y_axis)
    
    if args.y2_axis is not None:
        if args.y2_axis in state_labels:
            y2_axis = ("states", args.y2_axis)
        else:
            msids.append(args.y2_axis)
            y2_axis = ("msids", args.y2_axis)
    else:
        y2_axis = None
    
    if args.maude:
        mylog.info("Using MAUDE to retrieve MSID data.")
        ds = acispy.MaudeData(args.tstart, args.tstop, msids)
    else:
        ds = acispy.EngArchiveData(args.tstart, args.tstop, msids,
                                   filter_bad=True)
    
    cp = acispy.DatePlot(ds, y_axis, field2=y2_axis)
    plt.show()

if __name__ == "__main__":
    main()
