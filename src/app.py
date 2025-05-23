import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Sistema de Gestão de Calibração - Teste de Deploy"

@app.route('/teste-db')
def teste_db():
    try:
        # Apenas para teste, sem conexão real com banco
        return "Rota de teste funcionando!"
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
