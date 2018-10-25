from mnist import MNIST


class Neuron:
    init_value = 0

    def __init__(self, name, x_size, y_size):
        self.name = name
        self.x_size = x_size
        self.y_size = y_size
        self.size = self.x_size * self.y_size
        self.train_count = 0
        self.matrix = [[self.init_value for i in range(x_size)] for j in range(y_size)]

    def train(self, input_matrix):
        self.validate_input(input_matrix)
        self.train_count += 1
        with self.iterover() as i, j:
            self.matrix[i][j] += input_matrix[i][j]
            self.matrix[i][j] /= self.train_count

    def recognize(self, input_matrix):
        p = 0
        self.validate_input(input_matrix)
        with self.iterover() as i, j:
            p += self.matrix[i][j] * input_matrix[i][j] / self.size
        return p

    def iterover(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                yield i, j

    def validate_input(self, input_matrix):
        if len(input_matrix) != self.y_size or len(input_matrix[0]) != self.x_size:
            raise Exception("Invalid input size")


class DigitCollection:
    def __init__(self, directory=''):
        self.data = MNIST(directory)
        self.images, self.labels = self.data.load_training()
        print(self.data.display(self.images[0]))
        for i in range(len(self.images)):
            # print(self.data.display(self.images[i]))
            print(self.data.display(self.labels))

if __name__ == '__main__':
    digits = DigitCollection()
