import json
from copy import deepcopy


class Node:
    def __init__(self, level, data):
        self.data = data
        self.level = level
        self.children = []
        self.parent = None

    @property
    def has_children(self):
        if len(self.children) > 0:
            return True
        return False

    @property
    def descendants(self):
        children = []
        if self.level == 2:
            return children
        
        if self.level == 1:
            return children + self.children 

        if self.level == 0:
            children += self.children
            for i in self.children:
                children += i.children

            return children

    def add_child(self, obj):
        obj.parent = self
        self.children.append(obj)

    def __repr__(self):
        return f"<Node: {json.dumps(self.data)}>"

    @staticmethod
    def search(node, data):
        result = []
        dimensions = []
        for item in data.get('dim', []):
            oj = []
            for key in item.items():
                oj.append(key)
            dimensions.append(oj)

        node_dimensions = []
        if node.data.get('dim'):
            for item in node.data['dim']:
                oj = []
                for key in item.items():
                    oj.append(key)
                node_dimensions.append(oj)
        
        if node.data.get('dim') is None:
            if data.items() <= node.data.items():
                result.append(node)
        elif (all([True if i in node_dimensions else False for i in dimensions]) 
                and node.data.get('dim') is not None):
            result.append(node)
        if node.has_children:
            for child in node.children:
                result.extend(Node.search(child, data))
        return result

    @staticmethod
    def check_for_parent(node, data):
        search_data = deepcopy(data)
        search_data.pop('metrics')
        parent_data = search_data
        parent_data['dim'] = [i for i in search_data['dim'] if i['key'] == "country"]
        return Node.search(node, parent_data)

    @staticmethod
    def search_for_insert(node, data):
        result = Node.search(node, data)

        if len(result) == 0:
            dimensions = [item["key"] for item in data['dim']]
            if len(dimensions) == 1:
                if ['country'] == dimensions:
                    node.add_child(Node(1, data))
            else:
                parent = Node.check_for_parent(node, data)
                if "country" in dimensions and len(parent) == 0:
                    new_data = deepcopy(data)
                    new_data['dim'] = [i for i in new_data['dim'] if i['key'] == "country"]

                    level_1 = Node(1, new_data)
                    node.add_child(level_1)
                    level_1.add_child(Node(2, data))
                else:
                    parent = parent[0]
                    node_metrics = {item['key']:item['val'] for item in parent.data['metrics']}
                    data_metrics = {j['key']:j['val'] for j in data['metrics']}
                    for key, val in node_metrics.items():
                        data_metrics[key] += val
                    metrics_data = [
                        {
                            "key": key,
                            "val": value
                        }
                        for key, value in data_metrics.items()
                    ]
                    parent.add_child(Node(2, data))
                    parent.data['metrics'] = metrics_data
        else:
            found_node = result[0]
            node_metrics = {item['key']:item['val'] for item in found_node.data['metrics']}
            data_metrics = {j['key']:j['val'] for j in data['metrics']}
            for key, val in node_metrics.items():
                if data_metrics.get(key):
                    data_metrics[key] += val
                else:
                    data_metrics.setdefault(key, val)
            metrics_data = [
                {
                    "key": key,
                    "val": value
                }
                for key, value in data_metrics.items()
            ]
            found_node.data['metrics'] = metrics_data


