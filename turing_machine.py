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
        
        return output_string
