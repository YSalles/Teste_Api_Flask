from flask import Flask, jsonify, request
from db import get_db

app = Flask(__name__)

# GET (BUSCAR TODOS OS REGISTROS) 
@app.route('/pessoas', methods=['GET'])
def todos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    records = cursor.fetchall()
    cursor.close()
    return jsonify(records)
#teste de alteração

# GET  (BUSCAR POR UM ID ESPECÍFICO)
@app.route('/pessoas/<int:id_registro>', methods=['GET'])
def por_id(id_registro: int) -> str:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas WHERE id = %s", (id_registro,))
    record = cursor.fetchone()
    cursor.close()
    if record:
        return jsonify(record)
    else:
        return jsonify({"message": f"Registro com o ID {id_registro} não encontrado."}), 404


# POST (CRIAR UM NOVO REGISTRO)Rota para criar um novo registro
@app.route('/pessoas', methods=['POST'])
def criar() -> str:
    conn = get_db()
    cursor = conn.cursor()

    # Buscar  último ID da tabela
    cursor.execute("SELECT MAX(id) FROM pessoas")
    ultimo_id = cursor.fetchone()[0]

    # Gerar novo ID
    novo_id = ultimo_id + 1
 
    dados = request.get_json()
    nome = dados[0]
    idade = dados[1]

    # Inserir novo registro na tabela 
    cursor.execute("INSERT INTO pessoas (id, nome, idade) VALUES (%s, %s, %s)", (novo_id, nome, idade))
    conn.commit()
    cursor.close()

    return jsonify({'status': 'sucesso', 'mensagem': 'Registro criado com sucesso.'})



# PUT (ATUALIZAR UM REGISTRO) 
@app.route('/pessoas/<int:id_registro>', methods=['PUT'])
def atualizar(id_registro: int) -> str:
    conn = get_db()
    cursor = conn.cursor()

    # Buscar dados para atualizar de acordo com ID informado
    dados = request.get_json()
    nome = dados[0]
    idade = dados[1]

    # Atualiza o registro com o ID 
    cursor.execute("UPDATE pessoas SET nome = %s, idade = %s WHERE id = %s", (nome, idade, id_registro))
    conn.commit()

    # Buscar informações do registro atualizado
    cursor.execute("SELECT * FROM pessoas WHERE id = %s", (id_registro,))
    registro_atualizado = cursor.fetchone()
    cursor.close()

    # Retorna as informações do registro atualizado
    return jsonify({'status': 'sucesso', 'mensagem': f"Registro com o ID {id_registro} atualizado com sucesso.", 'registro_atualizado': registro_atualizado})


# DELETE (DELETAR UM REGISTRO)
@app.route('/pessoas/<int:id_registro>', methods=['DELETE'])
def deletar(id_registro: int) -> str:
    conn = get_db()
    cursor = conn.cursor()

    # Deleta o registro com o ID especificado
    cursor.execute("DELETE FROM pessoas WHERE id = %s", (id_registro,))
    conn.commit()

    # Buscar a lista atualizada de registros
    cursor.execute("SELECT * FROM pessoas")
    records = cursor.fetchall()
    cursor.close()

    return jsonify({'Pessoas': records, 'mensagem': f'Registro com o ID {id_registro} deletado com sucesso.','status': 'sucesso'})

if __name__ == '__main__':
    app.run()
