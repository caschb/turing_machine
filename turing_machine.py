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
#   a. Current version: There are two TMs: a single taped turing machine and a multitape one. Tapes are 
#       implemented as as lists and displayed as strings.     
#

import enum # Allows for the usage of enumerators, which have codes for the possible results after 
            # a turing machine runs through an input String
    
########################################################################################################
# TuringMachine class. Contains all the methods in order to create a Turing machine based on a config
# file and run all the strings input strings, deciding (or not) from a input strings file. 
class TuringMachine:
    """ Contains the internal configuration of the machine and functions to run the configuration """

    # Constructor method of the TM. Inicializes all the parameters needed for the class
    def __init__(self):
        self._name = "" # This will be how the TM is called
        self._max_length = 0 # The max size of the TM-tape. If a string needs more space, it is 'rejected'
        self._max_steps = 0 # The max steps for the imput string. If a string needs more space, it is 'undecidable'

        self._states = [] # Q
        self._input_alphabet = [] # Σ
        self._tape_alphabet = [] # Γ
        self._initial_state = "" # q_0
        self._accept_state = "" # q_accept
        self._reject_state = "" # q_reject
        self._transitions = [] # δ

        self._current_state = "" # q_current
        self._current_step = 0 # Index for checking what is the current step and if I have reached 'max_steps'
        self._head_position = 0 # Index for where the head of the MT-tape is currently positioned
        self._tape = [] # Is the tape of the turing machine that will store all the symbols and write on them
        self._initial_strings = [] # These are the strings that are given to be run on the TM.

    # Using enum class create enumerations
    class FinalState(enum.Enum):
        ACCEPTED = 0 # If the machine reaches an accepted state
        REJECTED = 1 # If the machine reaches a reject state or there is no transition from certain state and symbol
        OUTSIDE = 2 # If the input string requires more space than the given max_length
        UNDECIDABLE = 3 # If the input string requires more steps than given max_steps to be decided

    """ Loads the definition of the machine with the format specified on the project instructions """
    def load_machine_definition(self, filename):

        # open the file to read the configurations
        with open(filename) as f:
            line = f.readline()

            # Separate the string with comma as a sepparator, as the file comes in the format (name, numberofTapas, maxlenght, maxsteps)
            elements = line.strip().split(',')
            
            # Assign the values to the class attributes
            self._name, self._max_length, self._max_steps = elements[0], int(elements[1]), int(elements[2])

            line = f.readline()
            self._states = line.strip().split(',') # The states come in the format "q1,q2,q3,q4,..."
            
            line = f.readline()
            self._input_alphabet = line.strip().split(',') # The alphabet comes in the format "acceptedCharacter1, accepterCharacter2,...""
            
            line = f.readline()
            self._tape_alphabet = line.strip().split(',') # Alphabet of the tape

            line = f.readline()
            self._initial_state = line.strip() # REad the initial state

            line = f.readline()
            self._accept_state, self._reject_state = line.strip().split(',') # Read the accept and reject states
            
            # Read all the transitions available in the turing machine
            line = f.readline()
            while(line):
                self._transitions.append(line.strip().split(','))
                line = f.readline()
                 
        # Set the start state       
        self._current_state = self._initial_state

        # Start the _tape in Null for each symbol
        self._tape = [None for i in range(self._max_length)]

        # Always add the blank symbol to the input alphabet
        self._input_alphabet.append('_')

    """ Loads the initial strings from a file """
    def load_initial_strings(self, filename):

        # Opens the file that has the strings of a language to see if it is recognized by the TM
        with open(filename) as f:
            line = f.readline()

            # Read each of the transitions
            while(line):
                stripped_string = line.strip()
                if(len(stripped_string) > 0 ):
                    self._initial_strings.append(list(stripped_string))
                line = f.readline()

    """Cleans the TM current configuration"""
    def _clean(self):

        # Make the machine be in the initial state again
        self._current_state = self._initial_state

        # Reset the index and the head position of the tape
        self._tape = [None for i in range(self._max_length)]
        self._current_step = 0
        self._head_position = 0


    """Fills the tape with the input string"""
    def _init_tape(self):
        self._tape = [None for i in range(self._max_length)]
        initial_string = self._initial_strings.pop(0)
        return_character = '\0'

        # Checks all the characters in the string
        for index, character in enumerate(initial_string):
            # Checks if the character is not in the alphabet
            if (character not in self._input_alphabet):
                return character, True # Returns the character and an error

            # The character was valid, add it to the list
            self._tape[index] = character
            return_character = character
            
        # No error was found, return the character and False
        return return_character, False
            

    # Method that finds transitions from current state to others.
    def _decode(self):
        current_values = list([self._current_state, self._tape[self._head_position]])
        
        # Search through all the transtitions to check if one is valid from current state and symbol
        for rule  in self._transitions:
            # Checks if the current symbol in the tape matches the one in the transition, to check if they match
            if rule[0] == current_values[0] and rule[1] == current_values[1]:
                return rule
        return None


    """"Applies the rule, moves the TMhead to the left or right"""
    def _execute(self, current_rule, quiet=False):
        self._current_state = current_rule[2]
        self._tape[self._head_position] = current_rule[3]

        if(current_rule[-1] == 'R'): # Right
            self._head_position += 1
        elif(current_rule[-1] == 'L'): # Left
            self._head_position -= 1
        if not quiet:
            self._print_step()
    

    """Checks whats the final state of the TM"""
    def _verify(self):

        # Uses the enumerate to set the final state
        if self._current_state == self._accept_state:
            return True, self.FinalState.ACCEPTED
        elif self._current_state == self._reject_state:
            return True, self.FinalState.REJECTED
        elif self._head_position == self._max_length:
            return True, self.FinalState.UNDECIDABLE 
        elif self._current_step >= self._max_steps:
            return True, self.FinalState.REJECTED
        else:
            return False,-1


    """Prints the tape with its respective state"""
    def _print_step(self):
        output_string = ""
        for idx, character in enumerate(self._tape):
            if(character == None):
                break
            if(idx == self._head_position):
                output_string += f" {self._current_state} "
            output_string += f" {character} "
        print(output_string)


    """Gets the next string, loads it into the TM tape and process it."""
    def run(self,quiet=False):
        # Loop while there are strings to read
        while(len(self._initial_strings) > 0):
            # Calls the method to restart the variables
            self._clean()

            # Starts the turing machine, and stores if any error was found
            character, error = self._init_tape()

            # Detects that a invalid character was entered and prints an error message
            if(error):
                print("Caracter inválido: \'" + character + "\'")
            else: # If everything worked well initializing the TM
                stop = False
                reason = -1

                # Loop as long as the machine is not accepted, rejected or reached max steps
                while(not stop):
                    # Calls the method to find a transition from the current state
                    current_rule = self._decode()

                    # No rule was found from this state to another, reject
                    if(current_rule == None):
                        reason = self.FinalState.REJECTED
                        break
                    self._execute(current_rule, quiet)

                    # Calls the method to find transitions and check if the machine terminated (reason)
                    stop, reason = self._verify()
                    self._current_step += 1

                # Detects if the string was accepted, rejected, or other
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


    # Method to print the turing machine
    def __str__(self):
        # Creates a string with name, lenght, steps and states
        output_string = f"Name: {self._name}\n"\
                        f"Max length: {self._max_length}\n"\
                        f"Max steps: {self._max_steps}\n" \
                        f"Q: {self._states}\n" \
                        f"Σ: {self._input_alphabet}\n" \
                        f"Γ: {self._tape_alphabet}\n" \
                        f"Q_o: {self._initial_state}\n" \
                        f"Q_accept, Q_reject: {self._accept_state}, {self._reject_state}\n" \
                        f"δ: \n"
        
        # Adds the transitions to the string
        for element in self._transitions:
            output_string += f"{element}\n"
        
        output_string += "----TEST STRINGS:----\n"

        # Prints the strings that were passed to the TM
        for element in self._initial_strings:
            output_string += f"{element}\n"


        return output_string
