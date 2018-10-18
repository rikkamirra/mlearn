from typing import List, Dict, Any
import json

from mathstat import Vector, M, D, r


MAX = 10000000000.0


class Dataset:
    def __init__(self, class_names: List[str], prop_names: List[str], name=''):
        self.name = name or '::'.join(class_names)
        self.class_set: Dict[str, 'Class'] = dict(
                                [(cls_name, Class(cls_name, prop_names)) \
                                for cls_name in class_names])

    def train(self, class_name: str, data: Dict[str, Any]):
        class_ = self.get_class(class_name)
        class_.train(data)

    def get_class(self, class_name) -> 'Class':
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
    def __init__(self, name: str, prop_names: List[str]):
        self.name = name
        self.prop_names = prop_names
        self.props_info: Dict[str: 'PropInfo'] = dict(
                                [(prop_name, PropInfo(prop_name)) \
                                for prop_name in self.prop_names])

    def train(self, data: Dict[str, Any]):
        for prop_name, prop_value in data.items():
            prop_info = self.get_prop_info(prop_name)
            prop_info.add(prop_value)

    def get_prop_info(self, prop_name) -> 'PropInfo':
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
        self.D = 0.0
        self.M = 0.0
        self.exp = 0.0
        self.max = 0.0
        self.min = MAX

        self.count = 0
        self.values = Vector()

    def add(self, value: float):
        self.count += 1
        self.values.append(value)

        self.set_max(value)
        self.set_min(value)
        self.set_M(value)
        self.set_exp()
        self.set_D()

    def set_max(self, value):
        if value > self.max:
            self.max = value

    def set_min(self, value):
        if value < self.min:
            self.min = value

    def set_M(self, value):
        self.M = self.values.average

    def set_exp(self):
        self.exp = (self.max - self.min) / 2

    def set_D(self):
        self.D = D(self.values)

    def __str__(self):
        nl = '\n'
        return f'{self.prop_name}:{nl}M: {self.M}{nl}D: {self.D}{nl}exp: {self.exp}{nl}Values: {self.values}{nl}'





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
