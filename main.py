from typing import List, Dict
import json


MAX = 10000000000.0

class Dataset:
    def __init__(self, class_names: List[str], class_props: List[str], name=''):
        self.name = name or '::'.join(class_names)
        self.class_set: Dict[str, 'Class'] = dict(
                                [(cls_name, Class(cls_name, class_props)) \
                                for cls_name in class_names])

    def train(self, class_name: str, data: Dict[str, int]):
        class_ = self.get_class(class_name)
        class_.train(data)

    def get_class(self, class_name):
        class_ = self.class_set.get(class_name)
        if class_ is None:
            raise Exception(f'Invalid class name {class_name} for dataset {self.name}')
        return class_

    def __str__(self):
        res = ''
        for _, cls_ in self.class_set.items():
            res += str(cls_)
        return res


class Class:
    def __init__(self, name: str, props: List[str]):
        self.name = name
        self.props = props
        self.props_info: Dict[str: 'PropInfo'] = dict(
                                [(prop_name, PropInfo(prop_name)) \
                                for prop_name in self.props])

    def train(self, data: Dict[str, int]):
        for prop_name, prop_value in data.items():
            prop_info = self.get_prop_info(prop_name)
            prop_info.add(prop_value)

    def get_prop_info(self, prop_name):
        prop_info = self.props_info.get(prop_name)
        if prop_info is None:
            raise Exception(f'Invalid prop_name {prop_name} for class {self.name}')
        return prop_info

    def __str__(self):
        nl = '\n'
        res = f'Class: {self.name}{nl}'
        for pname, pinfo in self.props_info.items():
            res += f'{str(pinfo)}{nl}'
        return res

class PropInfo:
    def __init__(self, prop_name: str):
        self.prop_name = prop_name
        self.d = 0.0
        self.m = 0.0
        self.exp = 0.0
        self.max = 0.0
        self.min = MAX

        self.count = 0
        self.values = []

    def add(self, value: float):
        self.count += 1
        self.values.append(value)

        self.set_max(value)
        self.set_min(value)
        self.set_m(value)
        self.set_exp()
        self.set_d()

    def set_max(self, value):
        if value > self.max:
            self.max = value

    def set_min(self, value):
        if value < self.min:
            self.min = value

    def set_m(self, value):
        self.m = (self.m * (self.count - 1) + value) / self.count

    def set_exp(self):
        self.exp = (self.max - self.min) / 2

    def set_d(self):
        self.d = self.D(self.values)

    @staticmethod
    def squ(X):
        return [x**2 for x in X]

    @staticmethod
    def M(X):
        return sum(X) / len(X)

    @classmethod
    def D(cls, X):
        return cls.M(cls.squ(X)) - cls.M(X)**2

    def __str__(self):
        nl = '\n'
        return f'{self.prop_name}:{nl}M: {self.m}{nl}D: {self.d}{nl}exp: {self.exp}{nl}'


if __name__ == '__main__':
    filename = 'train.json'
    with open(filename, 'r') as f:
        data = json.loads(f.read())

        class_names = data["class_names"]
        prop_names = data["prop_names"]

        dataset = Dataset(class_names, prop_names, name="Movie")
        for class_name, class_data in data["data"].items():
            for d in class_data:
                dataset.train(class_name, d)

        print(dataset)
