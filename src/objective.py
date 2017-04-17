from subprocess import Popen, PIPE

DEVNULL = open("/dev/null","w")
maxout = ""
minout = ""

def outcount(cmd, outtype, verbose):
    
    exe = cmd[0]

    if outtype == ["stdout"]:
        cmd_shell = exe + ' "'+('" "'.join(cmd[1:]))+'" | wc -c' 
        process = Popen(cmd_shell, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=1)

    elif outtype == ["stderr"]:
        cmd_shell = exe + ' "'+('" "'.join(cmd[1:]))+'" 2>&1 >/dev/null | wc -c' 
        process = Popen(cmd_shell, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=1)

    else:
        print "ERROR"
        assert(0)

    out, _ = process.communicate()
    r = int(out)

    return r


"""

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

"""
