from tree import Node

data = {
    "0": [
            {
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 340
                    },
                    {
                        "key": "timespent",
                        "val": 260
                    }
                ]
            }
    ],
    "1": [
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "IN"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 120
                    }, 
                    {
                        "key": "timespent",
                        "val": 80
                    }
                ]
            },
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "US"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 220
                    }, 
                    {
                        "key": "timespent",
                        "val": 180
                    }
                ]
            }
    ],
    "2": [
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "IN"
                    },
                    {
                        "key": "device",
                        "val": "mobile"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 70
                    }, 
                    {
                        "key": "timespent",
                        "val": 30
                    }
                ]
            },
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "IN"
                    },
                    {
                        "key": "device",
                        "val": "web"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 50
                    }, 
                    {
                        "key": "timespent",
                        "val": 50
                    }
                ]
            }
    ],
    "3": [
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "US"
                    },
                    {
                        "key": "device",
                        "val": "tablet"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 30
                    }, 
                    {
                        "key": "timespent",
                        "val": 50
                    }
                ]
            },
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "US"
                    },
                    {
                        "key": "device",
                        "val": "mobile"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 80
                    }, 
                    {
                        "key": "timespent",
                        "val": 70
                    }
                ]
            },
            {
                "dim": [
                    {
                        "key": "country",
                        "val": "US"
                    },
                    {
                        "key": "device",
                        "val": "web"
                    }
                ], 
                "metrics": [
                    {
                        "key": "webreq",
                        "val": 110
                    }, 
                    {
                        "key": "timespent",
                        "val": 60
                    }
                ]
            }
    ],
}

def create_tree():
    root = Node(0, data['0'][0])
    root.add_child(Node(1, data['1'][0]))
    root.add_child(Node(1, data['1'][1]))
    root.children[0].add_child(Node(2, data['2'][0]))
    root.children[0].add_child(Node(2, data['2'][1]))
    root.children[1].add_child(Node(2, data['3'][0]))
    root.children[1].add_child(Node(2, data['3'][1]))
    root.children[1].add_child(Node(2, data['3'][2]))

    return root
