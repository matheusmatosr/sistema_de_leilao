from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados de amostra - uma lista de itens com preço de oferta inicial
itens = [
    {"id": 1, "produto": "chuteira Nike", "preco": 100.00, "lance_atual": 10.00, "status": "ativo"}
]

# Solicitação GET para recuperar todos os itens
@app.route('/itens', methods=['GET'])
def obter_itens():
    return jsonify({'itens': itens})

# Solicitação GET para encontrar leilões em potencial
# Rota de exemplo para teste: http://localhost:5000/buscar?termo_busca=Nike
@app.route('/buscar', methods=['GET'])
def buscar_itens():
    termo_busca = request.args.get('termo_busca')
    if termo_busca:
        resultados = [item for item in itens if termo_busca.lower() in item['produto'].lower()]
        return jsonify({'itens': resultados})
    else:
        return jsonify({'mensagem': 'Nenhum termo de busca fornecido'}), 400
    
# Solicitação GET para totalizar os valores arrecadados no leilão até então
@app.route('/total_arrecadado', methods=['GET'])
def total_arrecadado():
    total = sum(item['lance_atual'] for item in itens if item.get('status') == 'encerrado')
    return jsonify({'total_arrecadado': total})

# Solicitação PUT para fazer um lance em um item
@app.route('/itens/<int:index>/lance', methods=['PUT'])
def fazer_lance(index):
    if 0 <= index < len(itens):
        dados = request.get_json()
        if 'valor_lance' in dados and isinstance(dados['valor_lance'], (int, float)) and dados['valor_lance'] > itens[index]['lance_atual']:
            itens[index]['lance_atual'] = dados['valor_lance']
            return jsonify({'mensagem': 'Lance realizado com sucesso'})
        else:
            return jsonify({'mensagem': 'Valor do lance inválido ou inferior ao lance atual'}), 400
    else:
        return jsonify({'mensagem': 'Item não encontrado'}), 404
    
# Solicitação PUT para alterar o status do produto do leilão: encerrado, ativo e previsto
@app.route('/itens/<int:index>/status', methods=['PUT'])
def atualizar_status_item(index):
    if 0 <= index < len(itens):
        dados = request.get_json()
        if 'status' in dados and dados['status'] in ['encerrado', 'ativo', 'previsto']:
            itens[index]['status'] = dados['status']
            return jsonify({'mensagem': f'Status do item {itens[index]["id"]} atualizado com sucesso'})
        else:
            return jsonify({'mensagem': 'Status inválido'}), 400
    else:
        return jsonify({'mensagem': 'Item não encontrado'}), 404

# Solicitação POST para adicionar um novo item ao leilão
@app.route('/itens', methods=['POST'])
def adicionar_item():
    dados = request.get_json()
    if 'produto' in dados and 'preco' in dados:
        item = {
            'id': len(itens) + 1,
            'produto': dados['produto'],
            'preco': dados['preco'],
            'lance_atual': dados['preco'],
            'status': 'ativo'
        }
        itens.append(item)
        return jsonify({'mensagem': 'Item adicionado ao leilão com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Dados de solicitação inválidos'}), 400

# Solicitação DELETE para remover um item do leilão
@app.route('/itens/<int:index>', methods=['DELETE'])
def remover_item(index):
    if 0 <= index < len(itens):
        del itens[index]
        return jsonify({'mensagem': 'Item removido do leilão com sucesso'})
    else:
        return jsonify({'mensagem': 'Item não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)