########################################################################################################
#
#	turing_machine.py -- Provides the code for executing a Turing Machine
#
#	version 1.0
#
########################################################################################################
#
#   CONTENTS
#
#   -- On this implementation
#   1. Definition of Turing Machine used
#   2. Implementation remarks
#   
#-------------------------------------------------------------------------------------------------------
#	1.	Definition of Turing Machine used in this implementation
#
#	All definitions and some of the examples provided in this implementation of
#	Turing machines are based on (Sipser, 2012)*. For each definition and
#	example, a reference to the corresponding element in that book is provided
#	enclosed in square brackets:
#
#	A Turing machine (TM) [p.168] is a 7-tuple (Q,Sigma,Gamma,Delta,Q0,Qa,Qr),
#	where
#
#		Q     : set of possible states for the machines
#		Sigma : input alphabet
#		Gamma : tape alphabet
#		Delta : transition function
#		Q0    : initial state
#		Qa    : accept state
#		Qr    : reject state
#
#		and each element of Delta is of the form [qi,si,qf,sf,m], where
#
#			qi,qj are states in Q
#			si,sf are symbols in Gamma
#			m is a valid head movement code
#
#	Sipser, M. (2012). Introduction to the Theory of Computation. 3rd edition,
#		Cengage Learning.
#
#-------------------------------------------------------------------------------------------------------
#   2. Implementation remarks
#   a. Current version: There are two TMs: a deterministic and a nondeterministic one. Tapes are 
#       implemented as as lists and displayed as strings.   
#

import enum # Allows for the usage of enumerators, which have codes for the possible results after 
            # a turing machine runs through an input String
import os    
########################################################################################################
# TuringMachine class. Contains all the methods in order to create a Turing machine based on a config
# file and run all the strings input strings, deciding (or not) from a input strings file. 
class MultitapeTuringMachine:
    """ Contains the internal configuration of the machine and functions to run the configuration """

    # Constructor method of the TM. Inicializes all the parameters needed for the class
    def __init__(self):
        self._name = "" # This will be how the TM is called
        self._max_length = 0 # The max size of the TM-tape. If a string needs more space, it is 'rejected'
        self._max_steps = 0 # The max steps for the imput string. If a string needs more space, it is 'undecidable'

        self._states = [] # Q
        self._input_alphabet = [] # Σ
        self._tapes_alphabet = [] # Γ
        self._initial_state = "" # q_0
        self._accept_state = "" # q_accept
        self._reject_state = "" # q_reject
        self._transitions = [] # δ
        
        self._number_of_tapes = 0

        self._current_state = "" # q_current
        self._current_step = 0 # Index for checking what is the current step and if I have reached 'max_steps'
        self._head_positions = [] # Index for where the head of the MT-tape is currently positioned
        self._tapes = [] # Is the tape of the turing machine that will store all the symbols and write on them
        self._initial_strings = [] # These are the strings that are given to be run on the TM.

    # Using enum class create enumerations
    class FinalState(enum.Enum):
        ACCEPTED = 0 # If the machine reaches an accepted state
        REJECTED = 1 # If the machine reaches a reject state or there is no transition from certain state and symbol
        OUTSIDE = 2 # If the input string requires more space than the given max_length
        UNDECIDABLE = 3 # If the input string requires more steps than given max_steps to be decided

    def load_machine_definition(self, filename):
        """ Loads the definition of the machine with the format specified on the assigment """

        with open(filename) as f:
            line = f.readline()
            elements = line.strip().split(',')
            self._name, self._number_of_tapes, self._max_length, self._max_steps = elements[0], int(elements[1]), int(elements[2]), int(elements[3])

            line = f.readline()
            self._states = line.strip().split(',')
            
            line = f.readline()
            self._input_alphabet = line.strip().split(',')
            
            # Alphabet for each tape
            for alphabet in range(self._number_of_tapes):
                line = f.readline()
                self._tapes_alphabet.append(line.strip().split(','))

            line = f.readline()
            self._initial_state = line.strip()

            line = f.readline()
            self._accept_state, self._reject_state = line.strip().split(',')
            
            line = f.readline()
            while(line):
                self._transitions.append(line.strip().split(','))
                line = f.readline()
                        
        self._current_state = self._initial_state
        
        for tape_index in range(self._number_of_tapes):
            self._head_positions.append(0)
            self._tapes.append([ "_" for i in range(self._max_length)])
        self._input_alphabet.append('_')

    def load_initial_strings(self, filename):
        """ Loads the initial strings from a file """
        with open(filename) as f:
            line = f.readline()
            while(line):
                stripped_string = line.strip()
                if(len(stripped_string) > 0 ):
                    self._initial_strings.append(list(stripped_string))
                line = f.readline()

    def _clean(self):
        """Cleans the TM current configuration"""
        self._current_state = self._initial_state
        for tape_index in range(self._number_of_tapes):
            self._tapes[tape_index] = ["_" for i in range(self._max_length)]
            self._head_positions[tape_index] = 0
        self._current_step = 0

    def _init_tape(self):
        """Fills the tape with the input string"""
        self._tapes[0] = ["_" for i in range(self._max_length)]
        initial_string = self._initial_strings.pop(0)
        return_character = '\0'
        for index, character in enumerate(initial_string):
            if (character not in self._input_alphabet):
                return character, True

            self._tapes[0][index] = character
            return_character = character
            
        return return_character, False
            

    def _decode(self):
       # Comparar si el estado igual es igual al de la regla, si todos los
       # valores de simbolos iniciales hacen match en el tape.
        for rule in self._transitions:
            if (rule[0] == self._current_state):
                rule_applies = True
                # For every initial symbol in each tape
                for initial_symbols in range(1, (self._number_of_tapes + 1)):
                    if (self._tapes[initial_symbols - 1][self._head_positions[initial_symbols-1]] != rule[initial_symbols]):
                        rule_applies = False
                if (rule_applies):
                    return rule        
        return None

    def _execute(self, current_rule, quiet=False):
        """"Applies the rule, moves the TMhead to the left or right"""
        final_state_position = self._number_of_tapes + 1
        self._current_state = current_rule[final_state_position]

        for tape_index in range(self._number_of_tapes):
            final_state_position +=1
        
            self._tapes[tape_index][self._head_positions[tape_index]] = current_rule[final_state_position]
            if(current_rule[final_state_position + self._number_of_tapes ] == 'r'):
                self._head_positions[tape_index] += 1
            elif(current_rule[final_state_position + self._number_of_tapes] == 'l'):
                self._head_positions[tape_index] -= 1
            elif(current_rule[final_state_position + self._number_of_tapes] == 's'):
                pass
            
        
        if not quiet:
            self._print_step()
    
    def _verify(self):
        """Checks whats the final state of the TM"""
        if self._current_state == self._accept_state:
            return True, self.FinalState.ACCEPTED
        elif self._current_state == self._reject_state:
            return True, self.FinalState.REJECTED
        elif self._head_positions[0] == self._max_length:
            return True, self.FinalState.UNDECIDABLE 
        elif self._current_step >= self._max_steps:
            return True, self.FinalState.REJECTED
        else:
            return False,-1

    def _print_step(self):
        """Prints the tape with its respective state"""
        print("----STEP----")
        for tape_idx, dummy in enumerate(self._tapes):
            print(f"Tape: {tape_idx}")
            output_string = ""
            for idx, character in enumerate(self._tapes[tape_idx]):
                if(character == None):
                    break
                if(idx == self._head_positions[tape_idx]):
                    output_string += f" {self._current_state} "
                output_string += f" {character} "
            print(output_string)

    def run(self,quiet=False):
        """Gets the next string, loads it into the TM tape and process it."""
        while(len(self._initial_strings) > 0):
            self._clean()
            character, error = self._init_tape()

            if(error):
                print("Caracter inválido: \'" + character + "\'")
            else:
                stop = False
                reason = -1
                while(not stop):
                    current_rule = self._decode()
                    if(current_rule == None):
                        reason = self.FinalState.REJECTED
                        break
                    self._execute(current_rule, quiet)
                    stop, reason = self._verify()
                    self._current_step += 1

                if reason == self.FinalState.ACCEPTED:
                    print("Aceptado")
                elif reason == self.FinalState.REJECTED:
                    print("Rechazado")
                elif reason == self.FinalState.OUTSIDE:
                    print("Fuera")
                elif reason == self.FinalState.UNDECIDABLE:
                    print("Indecidible")
                elif reason == self.FinalState.REJECTED:
                    print("Rechazado")


    def __str__(self):
        output_string = f"Name: {self._name}\n"\
                        f"Max length: {self._max_length}\n"\
                        f"Max steps: {self._max_steps}\n" \
                        f"Q: {self._states}\n" \
                        #f"Σ: {self._input_alphabet}\n" \
                        #f"Γ: {self._tape_alphabet}\n" \
                        #f"Q_o: {self._initial_state}\n" \
                        #f"Q_accept, Q_reject: {self._accept_state}, {self._reject_state}\n" \
                        #f"δ: \n"
        for element in self._transitions:
            output_string += f"{element}\n"
        
        output_string += "----TEST STRINGS:----\n"
        for element in self._initial_strings:
            output_string += f"{element}\n"


        return output_string
