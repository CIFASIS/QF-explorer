from ast import literal_eval

def read_spec_file(filename):
    return literal_eval(open(filename,"r").read())

def get_spec_size(freq_spec):
    return sum(map(lambda x: x[1], freq_spec))

