from flask import Blueprint, request, jsonify
from services.node_service import register_node, assign_tasks_to_nodes, receive_model

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/api/register_node', methods=['POST'])
def register_node_route():
    node_data = request.json
    response = register_node(node_data)
    return jsonify(response)

@routes_blueprint.route('/api/upload_dataset', methods=['POST'])
def upload_dataset():
    dataset = request.json
    response = assign_tasks_to_nodes(dataset)
    return jsonify(response)

@routes_blueprint.route('/api/send_model', methods=['POST'])
def receive_model_route():
    model_data = request.json
    response = receive_model(model_data)
    return jsonify(response)
