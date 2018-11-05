from typing import List, Dict, Any
import json
from itertools import combinations

from mathstat import Vector, M, D, r


MAX = 10000000000.0


class Dataset:
    def __init__(self, class_names: List[str], prop_names: List[str], name=''):
        self.name = name or '::'.join(class_names)
        self.classes: Dict[str, 'Class'] = dict(
                                [(cls_name, Class(cls_name, prop_names)) \
                                for cls_name in class_names])

    def train(self, class_name: str, data: Dict[str, Any]):
        class_ = self.get_class(class_name)
        class_.train(data)

    def get_class(self, class_name) -> 'Class':
        class_ = self.classes.get(class_name)
        if class_ is None:
            raise Exception(f'Invalid class name {class_name} for dataset {self.name}')
        return class_

    def __str__(self):
        res = ''
        for _, cls_ in self.classes.items():
            res += str(cls_)
            res += f'Regressions: {cls_.regressions}' + '\n'
        return res


class Class:
    ACCEPT_REGRESSION = 0.7

    def __init__(self, name: str, prop_names: List[str]):
        self.name = name
        self.prop_names = prop_names
        self.props_info: Dict[str: 'PropInfo'] = dict(
                                [(prop_name, PropInfo(prop_name)) \
                                for prop_name in self.prop_names])
        self.regressions = []

    def train(self, data: Dict[str, Any]):
        for prop_name, prop_value in data.items():
            prop_info = self.get_prop_info(prop_name)
            prop_info.add(prop_value)

    def get_prop_info(self, prop_name) -> 'PropInfo':
        prop_info = self.props_info.get(prop_name)
        if prop_info is None:
            raise Exception(f'Invalid prop_name {prop_name} for class {self.name}')
        return prop_info

    def find_recursion(self):
        props_combinations = combinations(self.prop_names, 2)
        for combination in props_combinations:
            reg = r(self.props_info[combination[0]].values, self.props_info[combination[1]].values)
            if abs(reg) >= self.ACCEPT_REGRESSION:
                lcomb = list(combination)
                lcomb.append(reg)
                self.regressions.append(lcomb)
        self.acceptance_number = len(self.regressions)

    def is_that(self, data: Dict[str, Any]):
        res = 0
        for k, v in data.items():
            prop = self.props_info[k]
            if self.verify(prop, v):
                res += 1
        return res / len(data)

    def verify(self, prop: 'PropInfo', value):
        return abs(prop.M - value) <= prop.exp

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


def build_json_from_csv(file_name, class_name):
    def get_list_items(line):
        return [i.strip() for i in line.split(',')]

    def build_item(items, prop_names, class_index, to_type=float):
        res = {}
        for i, _ in enumerate(prop_names):
            if i == class_index:
                continue
            res[prop_names[i]] = to_type(items[i])
        return res

    with open(file_name, 'r') as src_file:
        headers = get_list_items(src_file.readline())
        prop_names = [h for h in headers if h != class_name]
        class_index = headers.index(class_name)
        jsond = {'prop_names': prop_names, 'class_names': [], 'data': {}}
        for line in src_file:
            items = get_list_items(line)
            new_class_name = items[class_index]
            if jsond['data'].get(new_class_name) is None:
                jsond['data'][new_class_name] = []
                jsond['class_names'].append(new_class_name)
            jsond['data'][new_class_name].append(build_item(items, prop_names, class_index))
    with open('new_iris.json', 'w') as f:
        f.write(json.dumps(jsond));
    return jsond


if __name__ == '__main__':
    filename = 'iris.csv'
    json_data = build_json_from_csv(filename, 'class')
    dataset = Dataset(class_names=json_data['class_names'], prop_names=json_data['prop_names'])
    for class_name, class_data in json_data['data'].items():
        for data in class_data:
            dataset.train(class_name, data)
    print(dataset)

    test_data = {"val1": 7.0, "val2": 3.2, "val3": 4.7, "val4": 1.4}
    class_ = "Iris-setosa"

    for class_name, class_ in dataset.classes.items():
        print(class_name, class_.is_that(test_data))
