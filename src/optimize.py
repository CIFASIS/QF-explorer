from cma import CMAEvolutionStrategy

from objective    import outcount
from specs        import get_spec_size
from qf           import qf_exec

args = dict()

def f(ps):

    global args
    qf_cmd = qf_exec(ps, args["spec"], args["fmt"], args["cmd"], args["nfiles"] ,50,1000, "outdir", args["fuzzer"], verbose=True)
    #print qf_cmd

    if args["objective"] == "min-out-count":
        r = outcount(qf_cmd, ["stdout"], args["verbose"])
    elif args["objective"] == "max-out-count":
        r = (-1) * outcount(qf_cmd, ["stdout"], args["verbose"])
    elif args["objective"] == "min-err-count":
        r = outcount(qf_cmd, ["stderr"], args["verbose"])
    elif args["objective"] == "max-err-count":
        r = (-1) * outcount(qf_cmd, ["stderr"], args["verbose"])
    else:
        print "Error: invalid objective function!"
        assert(0)

    r = r / args["nfiles"]

    return r


def optimize(fmt, freq_spec, cmd, fuzzer, objective, iterations, verbose):

    spec_size = get_spec_size(freq_spec) 
    initial_probs = spec_size * [5]

    global args

    args["fmt"] = fmt
    args["spec"] = freq_spec
    args["cmd"] = cmd
    args["fuzzer"] = fuzzer
    args["verbose"] = verbose
    args["objective"] = objective
    args["nfiles"] = 100

    es = CMAEvolutionStrategy (initial_probs, 5, {'verb_disp': 1, 'bounds': [-0.99,10]})
    es.optimize(f, iterations=iterations)
    #print map(int,es.result()[0])

