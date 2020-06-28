# TODO
# Hacer la impresion paso por paso
# Revisar que los caracteres sean parte del alfabeto, si no lo son se rechaza
# Hacer el enum para los casos de rechazo, acpetado, etc

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
        self._current_state = self._initial_state
        self._tape = [None for i in range(self._max_length)]
        self._current_step = 0
        self._head_position = 0

    def _init_tape(self):
        self._tape = [None for i in range(self._max_length)]
        initial_string = self._initial_strings.pop(0)
        for index, character in enumerate(initial_string):
            self._tape[index] = character

    def _decode(self):
        current_values = list([self._current_state, self._tape[self._head_position]])
        for rule  in self._transitions:
            if rule[0] == current_values[0] and rule[1] == current_values[1]:
                return rule
        return None

    def _execute(self, current_rule):
        self._current_state = current_rule[2]
        self._tape[self._head_position] = current_rule[3]
        if(current_rule[-1] == 'R'):
            self._head_position += 1
        elif(current_rule[-1] == 'L'):
            self._head_position -= 1
    
    def _verify(self):
        if self._current_state == self._accept_state:
            return True, 0
        elif self._current_state == self._reject_state:
            return True, 1
        elif self._head_position == self._max_length:
            return True, 2
        elif self._current_step >= self._max_steps:
            return True, 3
        else:
            return False,-1

    def _print_step(self):
        output_string = ""
        for idx, character in enumerate(self._tape):
            if(character == None):
                break
            if(idx == self._current_step):
                output_string += f" {self._current_state} "
            output_string += f" {character} "

    def run(self):
        while(len(self._initial_strings) > 0):
            self._clean()
            self._init_tape()
            stop = False
            reason = -1
            while(not stop):
                current_rule = self._decode()
                if(current_rule == None):
                    reason = 4
                    break
                self._execute(current_rule)
                stop, reason = self._verify()
                self._current_step += 1
                #print(self._print_step())
            if reason == 0:
                print("Accepted")
            elif reason == 1:
                print("Rejected")
            elif reason == 2:
                print("Outside")
            elif reason == 3:
                print("Undecidable")
            elif reason == 4:
                print("Rejected")


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
