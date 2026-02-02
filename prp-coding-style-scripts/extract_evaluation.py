#!/usr/bin/env python3

import re
import sys


TASK_NAME = 'Načítání vstupu'


def extract_eval_comment(line):
    line_re = r'(.*)\s*//{([\d.-]*)}(.*)'
    match = re.search(line_re, line)
    if match:
        return match.group(1), match.group(2), match.group(3)
    else:
        return line.rstrip('\n'), "", ""
        

def print_eval_md(matched_lines, eval_lines):
    print('---')
    print('fontfamily: merriweather')
    print('fontfamilyoptions: sfdefault')
    print('highlight-style: tango')
    print('---')

    print(f'# Code review {TASK_NAME}')

    total_points = 0
    for _, points, _ in matched_lines:
        total_points += float(points) if points else 0

    print(f"CS penalty: {total_points} b\n\n")

    print(''.join(eval_lines))
    
    print('## main.c') 
    
    print('```{.c .numberLines startFrom=1}')

    for i, (oline, points, comment) in enumerate(matched_lines):
        print(oline)
        if comment:
            print('```')
            print(comment)
            if points:
                print(points, "b")
            print(f'```{{.c .numberLines startFrom={i+2}}}')

    print('```')
    print('---')
    print(total_points)
    
    
if __name__=='__main__':
    assert len(sys.argv) > 1, 'Expecting submission directory name.'
    sub_dirn = sys.argv[1]
    
    source_fn = sub_dirn + '/main.c'
    eval_fn = sub_dirn + '/eval.txt'
    
    with open(source_fn) as source_f:
        source_lines = source_f.readlines()
        
    matched_lines = [ extract_eval_comment(l) for l in source_lines ]
    
    with open(eval_fn) as eval_f:
        eval_lines = eval_f.readlines()
        
    print_eval_md(matched_lines, eval_lines)
