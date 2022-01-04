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
    serializer = InsertSchema()
    try:
        data = serializer.load(data=request.get_json())
    except ValidationError as error:
        return jsonify(error.messages), 400
    except BadRequest:
        return jsonify({"detail": "Malformed JSON received"}), 400
    return jsonify(data)

@app.route('/v1/query', methods=["GET"])
def search():
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
        return "", 404
    return jsonify(result[0].data)

if __name__ == "__main__":
    app.run(debug=True)
