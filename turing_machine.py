import enum
    
class TuringMachine:
    """ Contains the internal configuration of the machine and functions to evolve the configuration """

    def __init__(self):
        self._name = ""
        self._max_length = 0
        self._max_steps = 0

        self._states = [] # Q
        self._input_alphabet = [] # Σ
        self._tape_alphabet = [] # Γ
        self._initial_state = "" # q_0
        self._accept_state = "" # q_accept
        self._reject_state = "" # q_reject
        self._transitions = [] # δ

        self._current_state = "" # q_current
        self._current_step = 0
        self._head_position = 0
        self._tape = []
        self._initial_strings = []

    # Using enum class create enumerations
    class FinalState(enum.Enum):
        ACCEPTED = 0
        REJECTED = 1
        OUTSIDE = 2
        UNDECIDABLE = 3

    def load_machine_definition(self, filename):
        """ Loads the definition of the machine with the format specified on the assigment """

        with open(filename) as f:
            line = f.readline()
            elements = line.strip().split(',')
            self._name, self._max_length, self._max_steps = elements[0], int(elements[1]), int(elements[2])

            line = f.readline()
            self._states = line.strip().split(',')
            
            line = f.readline()
            self._input_alphabet = line.strip().split(',')
            
            line = f.readline()
            self._tape_alphabet = line.strip().split(',')

            line = f.readline()
            self._initial_state = line.strip()

            line = f.readline()
            self._accept_state, self._reject_state = line.strip().split(',')
            
            line = f.readline()
            while(line):
                self._transitions.append(line.strip().split(','))
                line = f.readline()
                        
        self._current_state = self._initial_state
        self._tape = [None for i in range(self._max_length)]

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
        self._tape = [None for i in range(self._max_length)]
        self._current_step = 0
        self._head_position = 0

    def _init_tape(self):
        """Fills the tape with the input string"""
        self._tape = [None for i in range(self._max_length)]
        initial_string = self._initial_strings.pop(0)
        return_character = '\0'
        for index, character in enumerate(initial_string):
            if (character not in self._input_alphabet):
                return character, True

            self._tape[index] = character
            return_character = character
            
        return return_character, False
            

    def _decode(self):
        """Search for the rule that applies to the current symbol"""
        current_values = list([self._current_state, self._tape[self._head_position]])
        for rule  in self._transitions:
            if rule[0] == current_values[0] and rule[1] == current_values[1]:
                return rule
        return None

    def _execute(self, current_rule, quiet=False):
        """"Applies the rule, moves the head to the left or right"""
        self._current_state = current_rule[2]
        self._tape[self._head_position] = current_rule[3]
        if(current_rule[-1] == 'R'):
            self._head_position += 1
        elif(current_rule[-1] == 'L'):
            self._head_position -= 1
        if not quiet:
            self._print_step()
    
    def _verify(self):
        """Checks whats the final state of the TM"""
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

    def _print_step(self):
        """Prints the tape with its respective state"""
        output_string = ""
        for idx, character in enumerate(self._tape):
            if(character == None):
                break
            if(idx == self._head_position):
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
                        f"Σ: {self._input_alphabet}\n" \
                        f"Γ: {self._tape_alphabet}\n" \
                        f"Q_o: {self._initial_state}\n" \
                        f"Q_accept, Q_reject: {self._accept_state}, {self._reject_state}\n" \
                        f"δ: \n"
        for element in self._transitions:
            output_string += f"{element}\n"
        
        output_string += "----TEST STRINGS:----\n"
        for element in self._initial_strings:
            output_string += f"{element}\n"


        return output_string
