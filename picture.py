from contextlib import contextmanager


class Neuron:
    init_value = 0

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
        return (i / x_center) * (j / y_center)

    def train(self, input_matrix):
        self.validate_input(input_matrix)
        self.train_count += 1
        for i, j in self.iterover():
            self.matrix[i][j] += input_matrix[i][j] * self.weight_matrix[i][j]
            self.matrix[i][j] /= self.train_count

    def recognize(self, input_matrix):
        p = 0
        self.validate_input(input_matrix)
        for i, j in self.iterover():
            p += self.matrix[i][j] * input_matrix[i][j] * self.weight_matrix[i][j] / self.size
        return p

    def iterover(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                yield i, j

    def validate_input(self, input_matrix):
        if len(input_matrix) != self.y_size or len(input_matrix[0]) != self.x_size:
            raise Exception(f'Invalid input size. Must be x = {self.x_size}, y = {self.y_size}. But have x = {len(input_matrix)} y = {len(input_matrix[0])}')

    def show(self):
        res = ''
        for row in self.matrix:
            res_ = ''
            for item in row:
                res_ += str(item)
            res += res_ + '\n'
        return res


class Brain:
    def __init__(self):
        self.neurons = []

    def add(self, neuron: Neuron):
        self.neurons.append(neuron)

    def recognize(self, input_string):
        rerults = {}
        input_matrix = self.build_matrix(input_string)
        for neuron in self.neurons:
            rerults[neuron.name] = neuron.recognize(input_matrix)
        return rerults

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
    def train_neuron(cls, neuron, trainfilename):
        with open(trainfilename, 'r') as f:
            train_staff = f.read()
        train_digits = train_staff.split('***')
        for train_digit in train_digits:
            neuron.train(cls.build_matrix(train_digit))
        return neuron

def main():
    X_SIZE = Y_SIZE = 28
    digits = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    neurons = dict((symbol, Neuron(symbol, X_SIZE, Y_SIZE)) for symbol in digits)

    for digit in digits:
        with open(f'digits/{digit}.digit', 'r') as f:
            train_string = f.read()
            Brain.train_neuron(neurons[digit], f'digits/{digit}.digit')

    string = '''
    ............................
    ............................
    ............................
    ............................
    ............................
    ......................@.....
    .....................@@.....
    ....................@@......
    ....................@.......
    ...................@........
    .............@....@.........
    ............@....@@.........
    ..........@@.....@..........
    ..........@.....@...........
    .........@@....@@...........
    .........@@@@@@@@@@@........
    ..............@.............
    .............@@.............
    .............@..............
    ............@@..............
    ............@...............
    ...........@................
    ...........@................
    ..........@.................
    ..........@.................
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
