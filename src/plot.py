#!/usr/bin/env python2.7

import cma


if __name__ == '__main__':

    cma.plot()
    try:
        raw_input()
    except SyntaxError:
        pass
