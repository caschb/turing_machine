#!/bin/python3

from turing_machine import TuringMachine
from sys import argv
from sys import exit

if __name__=="__main__":
    if len(argv) < 3:
        print(f"Error: Call format: {argv[0]} <config_file> <initial_strings_file> [--verbose]")
        exit(1)
    
    verbose = False
    if (len(argv) > 3 and argv[3] == '--verbose'):
        verbose = True

    tm = TuringMachine()
    tm.load_machine_definition(argv[1])
    tm.load_initial_strings(argv[2])
    print(tm)
    tm.run(verbose)