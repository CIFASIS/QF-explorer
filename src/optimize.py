from cma import CMAEvolutionStrategy

from objective    import outcount, FuzzyCount
from specs        import get_spec_size
from qf           import qf_exec

args = dict()

def f(ps):

    global args
    #print args
    qf_cmd = qf_exec(ps, args["spec"], args["fmt"], args["cmd"], args["nfiles"] ,50,1000, "outdir", args["fuzzer"], verbose=True)
    #print qf_cmd
    r = args["fitness"](qf_cmd)
    return r


def optimize(fmt, freq_spec, cmd, fuzzer, objective, iterations, verbose):

    spec_size = get_spec_size(freq_spec) 
    initial_probs = spec_size * [5]
    optimized = None
    nfiles = 10

    global args

    args["fmt"] = fmt
    args["spec"] = freq_spec
    args["cmd"] = cmd
    args["fuzzer"] = fuzzer
    args["verbose"] = verbose
    args["objective"] = objective
    args["nfiles"] = nfiles

    if objective == "min-out-count":
        args["fitness"] = lambda cmd: outcount(cmd, ["stdout"], verbose) / float(nfiles)
    elif objective == "max-out-count":
        args["fitness"] = lambda cmd: (-1) * outcount(cmd, ["stdout"], verbose) / float(nfiles)
    elif objective == "min-err-count":
        args["fitness"] = lambda cmd: outcount(cmd, ["stderr"], verbose) / float(nfiles)
    elif objective == "max-err-count":
        args["fitness"] = lambda cmd: (-1) * outcount(cmd, ["stderr"], verbose)  / float(nfiles)

    #else:
    #    print "Error: invalid objective function!"
    #    assert(0)



    while (True):
        if objective == "max-out-fuzzy":

            if optimized is None: 
                 optimized = FuzzyCount([])
            else:
                 optimized = FuzzyCount(optimized.collected_patterns)

            print optimized.collected_patterns
            args["fitness"] = lambda cmd: (-1) * optimized.fitness(cmd, ["stdout"], verbose)

        elif objective == "max-err-fuzzy":
            if optimized is None: 
                 optimized = FuzzyCount([])
            else:
                 optimized = FuzzyCount(optimized.collected_patterns)

            print optimized.collected_patterns
            args["fitness"] = lambda cmd: (-1) * optimized.fitness(cmd, ["stderr"], verbose)
       
        es = CMAEvolutionStrategy (initial_probs, 5, {'verb_disp': 1, 'bounds': [-0.99,10]})
        es.optimize(f, iterations=iterations)
        #print es.result
        #print es.result()
        print "Best freqs:"
        print map(int,es.result()[0])

