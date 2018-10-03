
class Dataset:

    def __init__(self, collection):
        self.collection = {}
        self.kinds = {}
        for item in collection:
            self.add(item)

    def add(self, model: 'Model', fields):
        if self.collection.get(model.kind) is None:
            self.collection[model.kind] = [model,]
            new_kind = Kind(model.kind, fields)
            new_kind.learn(model)
            self.kinds[new_kind.name] = new_kind
        else:
            self.collection[model.kind].append(model)
            self.kinds[model.kind].learn(model)

    def define(self, model: 'Model'):
        res = {}
        for name, kind in self.kinds.items():
            res[name] = kind.define(model)
        return res

    def __str__(self):
        s = ''
        for item in self.collection:
            s += f'{str(item)}\n'
        return s


class Kind:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        self.exp = {}
        self.average = {}
        self.values = {}
        for field in fields:
            self.exp[field] = 0
            self.average[field] = 0
            self.values[field] = []

    def learn(self, model):
        for field in self.fields:
            self.values[field].append(getattr(model, field))
            self.average[field] = sum(self.values[field]) / len(self.values[field])
            self.exp[field] = (max(self.values[field]) - min(self.values[field])) / 2

    def define(self, model):
        res = 0
        for field in self.fields:
            if self._in(field, getattr(model, field)):
                res += 1
        return res * 100 / 4

    def _in(self, field, value):
        return self.average[field] + self.exp[field] > value > self.average[field] - self.exp[field]

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'Kind: {self.name}'


class Model:

    def __init__(self, columns, line):
        if columns.get('kind') is None:
            raise Exception('kind must ne specified')

        self.columns = columns
        row = [r.split('\n')[0] for r in line.split(',')]
        if len(row) != len(columns):
            raise Exception('Wrong number of headers')

        _columns = list(columns.items())

        for i in range(len(row)):
            setattr(self, _columns[i][0], _columns[i][1](row[i]))

    def __str__(self):
        s = ''
        for header, _ in self.columns.items():
            s += f'{header}: {getattr(self, header)}; '
        return s
