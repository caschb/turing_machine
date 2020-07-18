#!/bin/python3

from turing_machine import TuringMachine
from turing_machine_multitape import MultitapeTuringMachine
from sys import argv
from sys import exit
import argparse

def main():
    parser = argparse.ArgumentParser(description="Turing machine implementation.")
    parser.add_argument('config',
                        metavar='config_file',
                        type=str,
                        help="The configuration file of the Turing Machine")

    parser.add_argument('strings',
                        metavar='strings_file',
                        type=str,
                        help="The initial strings file for the Turing Machine")

    parser.add_argument('-q',
                        '--quiet',
                        action='store_true',
                        help='Disable step by step printing')

    parser.add_argument('-t',
                        '--type',
                        action='store',
                        type=str,
                        help='Type of Turing Machine')
    args = parser.parse_args()
    
    # Initialize the TM
    if(args.type == 'mtd'):
        tm = TuringMachine()
    elif(args.type == 'mtkc'):
        tm = MultitapeTuringMachine()
    elif(args.type == None):
        tm = TuringMachine()
    else:
        print("Unknown type of Turing machine, refer to the README.md")
        exit(0)

    tm.load_machine_definition(args.config)
    tm.load_initial_strings(args.strings)
    print(tm)
    # Start computing
    tm.run(args.quiet)

if __name__=="__main__":
    main()