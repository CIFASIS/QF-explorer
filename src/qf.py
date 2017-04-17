from subprocess import Popen, PIPE, check_output, call
from freqs      import write_freq_file

def qf_gen(freqs, freq_spec, fmt, n, size, outdir):

    call(("rm -Rf "+outdir+"").split(" "))
    call(("mkdir "+outdir+"").split(" "))

    freqs = map(int,freqs)
    write_freq_file(freqs,freq_spec, "freqs.txt")

    cmd = "QuickFuzz gen"
    return cmd + " " + fmt + " -q "+ str(n) + " -l " + str(size) + " -u " + str(size) + " -o "+outdir

def qf_exec(freqs, freq_spec, fmt, cmd,  n, min_size, max_size, outdir, fuzzer, verbose = False, shrink=False):

    freqs = map(int,freqs)
    write_freq_file(freqs,freq_spec, "freqs.txt")

    cmd = ["/home/g/.local/bin/QuickFuzz", "test", fmt, cmd] 

    if fmt in ["xml", "pdf", "ps", "html", "zip"]:
        cmd.append("-a")
        min_size = min_size * 10
        max_size = max_size * 10

    if verbose:
        cmd.append("-v")

    if shrink:
        cmd.append("-r")

    if fuzzer:
        cmd.append("-f")
        cmd.append(fuzzer)

    return cmd + ["-q", str(n), "-l", str(min_size), "-u", str(max_size), "-o", outdir]
