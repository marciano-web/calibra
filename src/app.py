import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Sistema de Gestão de Calibração - Funcionando!"

@app.route('/teste-db')
def teste_db():
    try:
        # Código para testar a conexão com o banco
        return "Conexão com o banco de dados bem-sucedida!"
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
