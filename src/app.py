from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from init_tree import create_tree
from serializers import InsertSchema, SearchSchema
from tree import Node

app = Flask(__name__)
tree = create_tree()


@app.route('/v1/insert', methods=["POST"])
def insert():
    global tree
    serializer = InsertSchema()
    try:
        data = serializer.load(data=request.get_json())
        Node.insert(tree, data)
    except ValidationError as error:
        return jsonify(error.messages), 400
    except BadRequest:
        return jsonify({"detail": "Malformed JSON received"}), 400
    updated_node = Node.search(tree, data)[0]
    return jsonify(updated_node.data), 200


@app.route('/v1/query', methods=["GET"])
def query():
    global tree
    serializer = SearchSchema()
    try:
        data = serializer.load(data=request.get_json())
    except ValidationError as error:
        return jsonify(error.messages), 400
    except BadRequest:
        return jsonify({"detail": "Malformed JSON received"}), 400
    result = Node.search(tree, data)
    if len(result) == 0:
        return jsonify({"detail": "Not Found"}), 404
    return jsonify(result[0].data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
