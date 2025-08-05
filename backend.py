from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Permite CORS, útil para desenvolvimento local

# Dados em memória — aqui você pode trocar por um banco de dados depois
products = []
history = {}  # histórico de vendas: produto -> lista cumulativa vendas ao longo do tempo

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products, 'history': history})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    if any(p['name'] == name for p in products):
        return jsonify({'error': 'Produto já existe'}), 400
    product = {
        'name': name,
        'category': data.get('category'),
        'quantity': data.get('quantity', 0),
        'demand': data.get('demand', 0),
        'sold': data.get('sold', 0),
        'image': data.get('image') or 'https://via.placeholder.com/40',
    }
    products.append(product)
    history[name] = history.get(name, [0])
    return jsonify({'message': 'Produto adicionado'}), 201

@app.route('/products/<string:name>', methods=['PUT'])
def update_product(name):
    data = request.json
    for i, p in enumerate(products):
        if p['name'] == name:
            new_name = data.get('name')
            if new_name != name and any(prod['name'] == new_name for prod in products):
                return jsonify({'error': 'Novo nome já existe'}), 400
            # Atualiza produto e mantém o histórico
            products[i] = {
                'name': new_name,
                'category': data.get('category'),
                'quantity': data.get('quantity', 0),
                'demand': data.get('demand', 0),
                'sold': data.get('sold', 0),
                'image': data.get('image') or 'https://via.placeholder.com/40',
            }
            if new_name != name:
                # Transferir histórico para novo nome
                history[new_name] = history.pop(name, [0])
            return jsonify({'message': 'Produto atualizado'})
    return jsonify({'error': 'Produto não encontrado'}), 404

@app.route('/products/<string:name>', methods=['DELETE'])
def delete_product(name):
    global products, history
    products = [p for p in products if p['name'] != name]
    history.pop(name, None)
    return jsonify({'message': 'Produto excluído'})

@app.route('/simulate', methods=['POST'])
def simulate_sales():
    import random
    for p in products:
        if p['quantity'] > 0 and random.random() < p['demand'] / 100:
            p['quantity'] -= 1
            p['sold'] += 1
            if p['name'] in history:
                history[p['name']].append(history[p['name']][-1] + 1)
            else:
                history[p['name']] = [0, 1]
        else:
            if p['name'] in history:
                history[p['name']].append(history[p['name']][-1])
            else:
                history[p['name']] = [0]
    return jsonify({'message': 'Simulação realizada'})

@app.route('/clear', methods=['POST'])
def clear_data():
    global products, history
    products.clear()
    history.clear()
    return jsonify({'message': 'Dados e histórico limpos'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)