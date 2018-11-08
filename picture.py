from contextlib import contextmanager


class Neuron:
    init_value = 0.0

    def __init__(self, name, x_size, y_size):
        self.name = name
        self.x_size = x_size
        self.y_size = y_size
        self.size = self.x_size * self.y_size
        self.train_count = 0
        self.matrix = [[self.init_value for i in range(x_size)] for j in range(y_size)]
        self.weight_matrix = [[self.get_weight(i, j) for i in range(x_size)] for j in range(y_size)]

    def get_weight(self, i, j):
        x_center = int(self.x_size / 2)
        y_center = int(self.y_size / 2)
        # return (i / x_center) * (j / y_center)
        return 1.0

    def train(self, input_matrix):
        self.validate_input(input_matrix)
        for i, j in self.iterover():
            self.matrix[i][j] = self._get_p(input_matrix, i, j)
        self.train_count += 1

    def train_error(self, input_matrix):
        for i, j in self.iterover():
            self.matrix[i][j] -= input_matrix[i][j]

    def recognize(self, input_matrix):
        p = 0
        self.validate_input(input_matrix)
        for i, j in self.iterover():
            p += self._add_p(input_matrix, i, j)
        return p / self.size * 100

    def _get_p(self, input_matrix, i, j):
        return (self.matrix[i][j] * self.train_count + input_matrix[i][j] * self.weight_matrix[i][j]) / (self.train_count + 1)

    def _add_p(self, input_matrix, i, j):
        return input_matrix[i][j] * self.matrix[i][j] * self.weight_matrix[i][j]

    def iterover(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                yield i, j

    def validate_input(self, input_matrix):
        if len(input_matrix) != self.y_size or len(input_matrix[0]) != self.x_size:
            raise Exception(f'Invalid input size. Must be x = {self.x_size}, y = {self.y_size}. But have x = {len(input_matrix)} y = {len(input_matrix[0])}')

    def show_matrix(self):
        tab = '\t'
        res = ''
        for row in self.matrix:
            for i in row:
                if i > 5:
                    res += f'{int(i)}{tab}'
                else:
                    res += '\t'
            res += '\n\n\n'
        return res



class Brain:
    def __init__(self):
        self.neurons = []

    def add(self, neuron: Neuron):
        self.neurons.append(neuron)

    def recognize(self, input_string):
        results = {}
        input_matrix = self.build_matrix(input_string)
        for neuron in self.neurons:
            results[neuron.name] = neuron.recognize(input_matrix)
        result = 0
        max_p = 0
        for k, v in results.items():
            if v > max_p:
                max_p = v
                result = k
        return result

    @classmethod
    def build_matrix(cls, string):
        def convert(item):
            if item == '@':
                return 1
            return 0

        rows = string.split('\n')
        matrix = []
        for row in rows:
            row_items = []
            for i in row.strip():
                row_items.append(convert(i))
            if row_items:
                matrix.append(row_items)
        return matrix

    @classmethod
    def train_neuron(cls, neuron, trainfilename, train_on_error_file_names=None):
        for train_matrix in cls.get_input_from_file(trainfilename):
            neuron.train(train_matrix)
        return neuron

    @classmethod
    def get_input_from_file(cls, filename):
        with open(filename, 'r') as f:
            stuff = f.read()
        digits = stuff.split('***')
        return [cls.build_matrix(d) for d in digits]



def main():
    X_SIZE = Y_SIZE = 28
    digits = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    neurons = dict((symbol, Neuron(symbol, X_SIZE, Y_SIZE)) for symbol in digits)

    for digit in digits:
        train_on_error_file_names = [f'digits/{d}.digit' for d in digits if d != digit]
        Brain.train_neuron(neurons[digit], f'digits/{digit}.digit', train_on_error_file_names=train_on_error_file_names)

    string = '''
............................
............................
..............@.............
.............@@.............
............@@..............
............@...............
...........@@...............
...........@................
...........@................
..........@.................
..........@.................
..........@........@........
.................@@@@@......
.........@.....@@.....@.....
.........@....@.......@.....
.........@...@........@.....
.........@...@.......@......
.........@..@.......@@......
.........@...@.....@@.......
..........@.......@@........
...........@@.@@@@..........
.............@@@............
............................
............................
............................
............................
............................
............................
    '''

    brain = Brain()
    for k, v in neurons.items():
        brain.add(v)

    print(brain.recognize(string))





if __name__ == '__main__':
    main()
