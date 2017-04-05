from os import walk
from subprocess import Popen, PIPE, check_output, call

from freqs      import write_freq_file


DEVNULL = open("/dev/null","w")
maxout = ""
minout = ""

def outfile(cmd, seeds):
    global maxout

    r = 0
    all_files = []

    for x, y, files in walk(seeds):
        for f in files:
            all_files.append(x + "/" + f)

    for filename in all_files:
        prepared_cmd = cmd.replace("@@",filename).split(" ")
        process = Popen(prepared_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        rc = process.returncode
        if rc <> 0:
            print err
            print out
            print prepared_cmd
            assert(0)
        try:
            out = open(filename+".0.png","r+").read()
        except:
            out = ""

        size = len(out)
        r = r + size

        if size >= len(maxout):
            maxout = out
            f = open("sample.out", "w+")
            f.write(maxout)
            f.close()


    return -r / float(len(all_files))


def execute(cmd, seeds):

    r = 0
    all_files = []

    for x, y, files in walk(seeds):
        for f in files:
            all_files.append(x + "/" + f)

    for filename in all_files:
        prepared_cmd = cmd.replace("@@",filename).split(" ")
        process = Popen(prepared_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        rc = process.returncode
        if rc <> 0:
            print err
            print out
            print prepared_cmd
            assert(0)

    return 0



def outcount(cmd, seeds):
    global maxout

    r = 0
    all_files = []

    for x, y, files in walk(seeds):
        for f in files:
            all_files.append(x + "/" + f)

    for filename in all_files:
        prepared_cmd = cmd.replace("@@",filename).split(" ")
        process = Popen(prepared_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        rc = process.returncode
        if rc <> 0:
            print err
            print out
            print prepared_cmd
            #assert(0)
        size = len(out)
        r = r + size

        if size >= len(maxout):
            maxout = out
            f = open("sample.out", "w+")
            f.write(maxout)
            f.close()


    return -r / float(len(all_files))


def qf_outcount(freqs, freq_spec, fmt, cmd,  n, minsize, maxsize, outdir):

    freqs = map(int,freqs)
    write_freq_file(freqs,freq_spec, "freqs.txt")
   
    cmd = "QuickFuzz test " + fmt + " \"" + cmd + "\" -q " + str(n) + " -l " + str(minsize) + " -u " + str(maxsize) + " -o " + outdir + " -v -a | wc -c"
    print cmd
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, shell=1)
    out, _ = process.communicate()
    r = int(out) / float(n)

    return r

from lsh import LSHCache
cache = LSHCache()
last = 0
uniques = 0

def outlsh(cmd, seeds):

    global uniques, last, cache

    r = 0
    all_files = []
    last_uniques = uniques

    for x, y, files in walk(seeds):
        for f in files:
            all_files.append(x + "/" + f)

    for filename in all_files:
        prepared_cmd = cmd.replace("@@",filename).split(" ")
        process = Popen(prepared_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        rc = process.returncode
        x = cache.insert(out.replace(filename,"").split(), last)
        if x == []:
            uniques = uniques + 1
        
        last = last + 1

    return 100.0 * (uniques - last_uniques) / len(all_files)

def aflcount(cmd, seeds):
    cmd = "./afl-count -m none -i "+seeds+" -o .afl-traces -- "+cmd
    #print(cmd)
    out = check_output(cmd, shell=True)

    try:
      return int(out)
    except:
      return -1


