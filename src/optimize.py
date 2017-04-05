from cma import CMAEvolutionStrategy

# from objective    import  ???
from specs        import get_spec_size

def f(ps):

    global cmd_to_exec, freq_spec, fmt
    r = qf_outcount(ps, freq_spec, fmt, cmd_to_exec, 100, 300, 1000, "outdir")


def optimize(fmt, freq_spec, cmd, fuzzer, iterations, verbose):

    spec_size = get_spec_size(freq_spec) 
    initial_probs = spec_size * [1]

    es = CMAEvolutionStrategy (initial_probs, 1, {'verb_disp': 1, 'bounds': [-0.99,10]})
    es.optimize(f, iterations=iterations)
    #print map(int,es.result()[0])

