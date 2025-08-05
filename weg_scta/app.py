from flask import Flask, request, jsonify, send_from_directory
from backend import adicionar_produto, simular_venda, limpar_dados, listar_produtos

app = Flask(__name__, static_folder="static", static_url_path="")

# Rota principal: carrega o index.html da pasta static
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# Rota para adicionar um produto via frontend
@app.route("/adicionar", methods=["POST"])
def rota_adicionar():
    data = request.get_json()
    adicionar_produto(
        nome=data["nome"],
        categoria=data["categoria"],
        quantidade=int(data["quantidade"]),
        demanda=int(data["demanda"]),
        imagem=data["imagem"]
    )
    return jsonify({"status": "ok"})

# Rota para simular uma venda
@app.route("/simular", methods=["POST"])
def rota_simular():
    simular_venda()
    return jsonify({"status": "simulado"})

# Rota para limpar os dados
@app.route("/limpar", methods=["POST"])
def rota_limpar():
    limpar_dados()
    return jsonify({"status": "limpo"})

# Rota para listar todos os produtos
@app.route("/listar", methods=["GET"])
def rota_listar():
    df = listar_produtos()
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)