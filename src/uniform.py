from subprocess import call
from qf        import qf_exec

def uniform(fmt, freq_spec, cmd, fuzzer, verbose):
    qf_cmd = qf_exec([], [], fmt, cmd, 0xffffffff, 50,1000, "outdir", fuzzer, verbose=verbose)
    return call(qf_cmd)


