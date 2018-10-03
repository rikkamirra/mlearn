from model import Model, Dataset, Kind


if __name__ == '__main__':

    dataset = Dataset([])

    columns = {'sepal_length': float, 'sepal_width': float, 'petal_length': float, 'petal_wigth': float, 'kind': str}
    fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_wigth']

    with open('iris.csv', 'r') as f:
        for line in f:
            model = Model(columns, line)
            dataset.add(model, fields=fields)

    some_model = Model(columns, '6.2,2.9,4.3,1.3,Iris-versicolor')

    print(dataset.define(some_model))

    print('It is ', model.kind)
