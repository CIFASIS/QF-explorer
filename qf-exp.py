#!/usr/bin/env python2.7

import argparse

from src.specs import read_spec_file
from src.freqs import write_freq_file

from src.uniform import uniform
from src.sparse import sparse

"""
import subprocess

from subprocess import Popen, PIPE, check_output, call

import cma

from src.specs import read_specs_file
from src.freqs import write_freq_file
from src.objective import outcount, outlsh, outfile, qf_outcount
from src.qf import qf
"""


def radamsa(args, seeds, n, outdir):
    args = map(int,args)
    radamsa_mutators = ["ab=","bd=","bf=","bi=","br=","bp=","bei=","bed=","ber=","sr=","sd=","ld=","lds=","lr2=","li=","lr=","ls=","lp=","lis=","lrs=","td=","tr2=","ts1=","ts2=","tr=","uw=","ui=","num=","ft=","fn=","fo="]
    cmd = "radamsa -m "
    for (mut,val) in zip(radamsa_mutators, args):
      cmd = cmd + mut + str(val) + ","
    return cmd[:-1] + " -r" + " -n "+ str(n) + " " + seeds + " -o "+outdir+"/fuzz.%n"



def f(ps):

    global cmd_to_exec, freq_spec, fmt
    r = qf_outcount(ps, freq_spec, fmt, cmd_to_exec, 100, 300, 1000, "outdir")

    #cmd = qf(ps, freq_spec, fmt, 100, 30, "outdir")
    #rc = call(cmd.split(" "))
    #r = outcount(cmd_to_exec,"outdir")

    return -r

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("fmt", type = str)
    parser.add_argument("spec", type = str)
    parser.add_argument("cmd", type = str)
    parser.add_argument("--mode", type = str, default = "uniform")
    parser.add_argument("--fuzzer", type = str, default = None)
    parser.add_argument("--verbose", action='store_true')

    args = parser.parse_args()

    mode = args.mode
    verbose = args.verbose 
    fuzzer = args.fuzzer 
    
    cmd = args.cmd
    freq_spec = read_spec_file(args.spec)
    fmt = args.fmt

    if mode == "uniform":

        uniform(fmt, freq_spec, cmd, fuzzer, verbose)

    elif mode == "sparse":
        
        sparse(fmt, freq_spec, cmd, fuzzer, verbose) 

    elif mode == "optimize":

        optimize(fmt, freq_spec, cmd, fuzzer, verbose) 


    #print fmt
    #print freq_spec
    #print cmd_to_exec

    #freq_input_space = sum(map(lambda x: x[1], freq_spec))

    #es = cma.CMAEvolutionStrategy((freq_input_space) * [1], 1, {'verb_disp': 1, 'bounds': [-0.99,10]})
    #es.optimize(f, iterations=3000)
    #print map(int,es.result()[0])
