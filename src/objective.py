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


from fuzzywuzzy import process as fuzzy
from fuzzywuzzy.string_processing import StringProcessor

class FuzzyCount:
    '''A parsed ELF file'''

    def __init__(self, patterns, tolerance = 80):
        self.fuzzy_patterns = list(patterns)
        self.collected_patterns = list(patterns)
        self.processor = StringProcessor.strip
        self.tolerance = tolerance

    def fitness(self, cmd, outtype, verbose):
    
        exe = cmd[0]
        patterns = []
        out_file = "out.dat"
        r = 0

        if outtype == ["stdout"]:
            cmd_shell = exe + ' "'+('" "'.join(cmd[1:]))+'" > ' + out_file 
            process = Popen(cmd_shell, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=1)

        elif outtype == ["stderr"]:
            cmd_shell = exe + ' "'+('" "'.join(cmd[1:]))+'" 2> ' + out_file
            process = Popen(cmd_shell, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=1)

        else:
            print "ERROR"
            assert(0)

        out, _ = process.communicate()
        patterns = open(out_file,"r+").read().split("\n")
         

        if self.fuzzy_patterns == []: # just collect patterns
            for line in patterns:

                line = self.processor(line)

                if len(line) <= 4: #or (not line[0].isalpha()):
                    continue

                if line not in self.collected_patterns:
                    if self.collected_patterns == []:
                        self.collected_patterns.append(line) 

                    _, match = fuzzy.extractOne(line, self.collected_patterns, processor=None) 
                    if match < self.tolerance:
                        self.collected_patterns.append(line)

            return 0 # no need to continue


        for line in patterns:
            line = self.processor(line)

            if len(line) <= 4: #or (not line[0].isalpha()):
                continue

            if line not in self.fuzzy_patterns:

                _, match = fuzzy.extractOne(line, self.fuzzy_patterns, processor=None)
                if match < self.tolerance:
                    r = r + (100-match)

                _, match = fuzzy.extractOne(line, self.collected_patterns, processor=None) 
                if match < self.tolerance:
                    if line not in self.collected_patterns:
                        self.collected_patterns.append(line)


        return r
