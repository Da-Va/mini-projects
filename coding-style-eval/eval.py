#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Expecting an input file.'
    in_fn = sys.argv[1]

    with open(in_fn) as in_f:
        lines = in_f.readlines()
        
    print('---')
    print('fontfamily: merriweather')
    print('fontfamilyoptions: sfdefault')
    print('highlight-style: tango')
    print('---')
    print()
    print('## main.c')
    print('```{.c .numberLines startFrom=1}')
    for i, l in enumerate(lines):
        if i == 10:
            print('```')
            print('Test commentary')
            print('```{.c .numberLines startFrom=11}')
        print(l,end='')
    print('```')