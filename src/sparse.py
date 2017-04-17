from subprocess   import call
from numpy.random import choice # FIXME: remove numpy dependency?
from specs        import get_spec_size
from qf           import qf_exec


def sparse(fmt, freq_spec, cmd, fuzzer, verbose):

    spec_size = get_spec_size(freq_spec) 

    while True:
        freqs = list(choice([0,1,2], spec_size, True))
        print freqs
        qf_cmd = qf_exec(freqs, freq_spec, fmt, cmd, 10000, 50, 10000, "outdir", fuzzer, verbose = verbose)
        call(qf_cmd)

