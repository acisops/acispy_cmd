#!/usr/bin/env python

import argparse
import acispy
from acispy.utils import mylog
import numpy as np
import sys

att_msg = \
"""The attitude information for the ECS run. One of
three possible formats:
pitch,off_nom_roll: 155.0,2 .0;
quaternion: 1.0,0.3,0.0,0.0;
a string named: vehicle
"""

def main():
    
    parser = argparse.ArgumentParser(description='Simulate an ECS run.')
    parser.add_argument("component", type=str, help='The component to model: dpa, dea, psmc, or acisfp')
    parser.add_argument("tstart", type=str, help='The start time of the ECS run in YYYY:DOY:HH:MM:SS format')
    parser.add_argument("hours", type=float, help='The length of the ECS run in hours.')
    parser.add_argument("T_init", type=float, help='The initial temperature of the component in degrees C.')
    parser.add_argument("attitude", help=att_msg)
    parser.add_argument("ccd_count", type=int, help="The number of CCDs to clock.")
    
    fix_minus_sign = False
    
    argv = sys.argv[1:]
    if len(argv) >= 5 and argv[4].startswith("-"):
        argv[4] = argv[4][1:]
        fix_minus_sign = True
    
    args = parser.parse_args(args=argv)
    
    if "," not in args.attitude:
        attitude = args.attitude
    else:
        attitude = [float(a) for a in args.attitude.split(",")]
        if fix_minus_sign:
            attitude[0] *= -1
    
    ecs_run = acispy.SimulateECSRun(args.component, args.tstart, args.hours, args.T_init,
                                    attitude, args.ccd_count)
    
    dp = ecs_run.plot_model()
    filename = f"ecs_run_{ecs_run.name}_{args.ccd_count}chip_{args.tstart}.png"
    dp.savefig(filename)
    mylog.info("Image of the model run has been written to %s." % filename)


if __name__ == '__main__':
    main()