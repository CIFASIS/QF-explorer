def write_freq_file(freqs, spec, filename):

    freq_list = []
    i = 0

    for (t, s) in spec:
        freq = freqs[i:i+s]
        if freq == [0] * s:
            freq = [1] * s
        freq_list.append((t, freq))
        i = i + s

    f = open(filename, "w+")
    f.write(str(freq_list).replace("\'","\""))
    f.close()
