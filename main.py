#!/bin/python3

from turing_machine import TuringMachine
from sys import argv
from sys import exit

if __name__=="__main__":
    if len(argv) != 3:
        print(f"Error: Call format: {argv[0]} <config_file> <initial_strings_file>")
        exit(1)
    
    tm = TuringMachine()
    tm.load_machine_definition(argv[1])
    tm.load_initial_strings(argv[2])
    print(tm)
    tm.run()