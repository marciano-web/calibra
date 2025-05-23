from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import sqlite3
from datetime import datetime
import numpy as np
from scipy import stats

app = Flask(__name__)
app.secret_key = 'sistema_calibracao_key'

# Configuração do banco de dados SQLite para prototipagem rápida
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'calibracao.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))
    
    conn = get_db_connection()
    with open(os.path.join(os.path.dirname(__file__), 'database', 'schema_sqlite.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# Rotas para Instrumentos
@app.route('/instrumentos')
def listar_instrumentos():
    conn = get_db_connection()
    instrumentos = conn.execute('SELECT * FROM instrumentos WHERE ativo = 1').fetchall()
    conn.close()
    return render_template('instrumentos/listar.html', instrumentos=instrumentos)

@app.route('/instrumentos/novo', methods=['GET', 'POST'])
def novo_instrumento():
    if request.method == 'POST':
        codigo = request.form['codigo']
        descricao = request.form['descricao']
        tipo_id = request.form['tipo_id']
        fabricante = request.form['fabricante']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        resolucao = request.form['resolucao']
        faixa_minima = request.form['faixa_minima']
        faixa_maxima = request.form['faixa_maxima']
        unidade = request.form['unidade']
        setor_id = request.form['setor_id']
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO instrumentos (codigo, descricao, tipo_id, fabricante, modelo, numero_serie, '
            'resolucao, faixa_minima, faixa_maxima, unidade, setor_id, status, data_criacao) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (codigo, descricao, tipo_id, fabricante, modelo, numero_serie, resolucao, 
             faixa_minima, faixa_maxima, unidade, setor_id, 'ativo', datetime.now())
        )
        conn.commit()
        conn.close()
        
        flash('Instrumento cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_instrumentos'))
    
    conn = get_db_connection()
    tipos = conn.execute('SELECT * FROM tipos_instrumentos WHERE ativo = 1').fetchall()
    setores = conn.execute('SELECT * FROM setores WHERE ativo = 1').fetchall()
    conn.close()
    
    return render_template('instrumentos/novo.html', tipos=tipos, setores=setores)

# Rotas para Calibrações
@app.route('/calibracoes')
def listar_calibracoes():
    conn = get_db_connection()
    calibracoes = conn.execute('''
        SELECT c.*, i.codigo as instrumento_codigo, i.descricao as instrumento_descricao 
        FROM calibracoes c
        JOIN instrumentos i ON c.instrumento_id = i.id
        ORDER BY c.data_inicio DESC
    ''').fetchall()
    conn.close()
    return render_template('calibracoes/listar.html', calibracoes=calibracoes)

@app.route('/calibracoes/nova', methods=['GET', 'POST'])
def nova_calibracao():
    if request.method == 'POST':
        instrumento_id = request.form['instrumento_id']
        procedimento_id = request.form['procedimento_id']
        responsavel = request.form['responsavel']
        data_inicio = datetime.now()
        temperatura = request.form['temperatura']
        umidade = request.form['umidade']
        pressao = request.form['pressao']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO calibracoes (numero, instrumento_id, procedimento_id, responsavel, '
            'data_inicio, temperatura, umidade, pressao, status, data_criacao) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (f'CAL-{datetime.now().strftime("%Y%m%d")}-{instrumento_id}', 
             instrumento_id, procedimento_id, responsavel, data_inicio, 
             temperatura, umidade, pressao, 'em_andamento', datetime.now())
        )
        calibracao_id = cursor.lastrowid
        
        # Adicionar padrões utilizados
        padroes = request.form.getlist('padroes')
        for padrao_id in padroes:
            conn.execute(
                'INSERT INTO calibracao_padroes (calibracao_id, padrao_id, data_criacao) VALUES (?, ?, ?)',
                (calibracao_id, padrao_id, datetime.now())
            )
        
        conn.commit()
        conn.close()
        
        flash('Calibração iniciada com sucesso!', 'success')
        return redirect(url_for('registrar_medicoes', calibracao_id=calibracao_id))
    
    conn = get_db_connection()
    instrumentos = conn.execute('SELECT * FROM instrumentos WHERE ativo = 1').fetchall()
    procedimentos = conn.execute('SELECT * FROM procedimentos WHERE ativo = 1').fetchall()
    padroes = conn.execute('SELECT * FROM padroes WHERE ativo = 1').fetchall()
    conn.close()
    
    return render_template('calibracoes/nova.html', 
                          instrumentos=instrumentos, 
                          procedimentos=procedimentos,
                          padroes=padroes)

@app.route('/calibracoes/<int:calibracao_id>/medicoes', methods=['GET', 'POST'])
def registrar_medicoes(calibracao_id):
    conn = get_db_connection()
    calibracao = conn.execute('SELECT * FROM calibracoes WHERE id = ?', (calibracao_id,)).fetchone()
    instrumento = conn.execute('SELECT * FROM instrumentos WHERE id = ?', (calibracao['instrumento_id'],)).fetchone()
    procedimento = conn.execute('SELECT * FROM procedimentos WHERE id = ?', (calibracao['procedimento_id'],)).fetchone()
    
    if request.method == 'POST':
        # Processar os pontos de calibração
        sequencias = request.form.getlist('sequencia')
        valores_referencia = request.form.getlist('valor_referencia')
        valores_lidos = request.form.getlist('valor_lido')
        
        for i in range(len(sequencias)):
            valor_referencia = float(valores_referencia[i])
            valor_lido = float(valores_lidos[i])
            erro = valor_lido - valor_referencia
            
            # Cálculo simplificado de incerteza para o protótipo
            incerteza_padrao = abs(erro) * 0.1  # 10% do erro como exemplo
            fator_k = 2.0  # Fator de abrangência padrão
            incerteza_expandida = incerteza_padrao * fator_k
            
            # Verificar conformidade com base em critérios simples
            conforme = abs(erro) <= incerteza_expandida
            
            conn.execute(
                'INSERT INTO pontos_calibracao (calibracao_id, sequencia, valor_referencia, valor_lido, '
                'erro, incerteza_padrao, incerteza_expandida, fator_k, conforme, data_criacao) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (calibracao_id, sequencias[i], valor_referencia, valor_lido, erro, 
                 incerteza_padrao, incerteza_expandida, fator_k, conforme, datetime.now())
            )
        
        # Atualizar status da calibração
        conn.execute(
            'UPDATE calibracoes SET status = ?, data_fim = ? WHERE id = ?',
            ('concluida', datetime.now(), calibracao_id)
        )
        
        conn.commit()
        conn.close()
        
        flash('Medições registradas com sucesso!', 'success')
        return redirect(url_for('finalizar_calibracao', calibracao_id=calibracao_id))
    
    # Obter pontos de calibração do procedimento (simplificado para o protótipo)
    pontos_sugeridos = []
    if procedimento and procedimento['pontos_calibracao']:
        # Aqui seria feito o parsing dos pontos de calibração do procedimento
        # Para o protótipo, vamos usar valores fixos
        faixa_min = float(instrumento['faixa_minima'])
        faixa_max = float(instrumento['faixa_maxima'])
        pontos_sugeridos = [
            {'sequencia': 1, 'valor': faixa_min},
            {'sequencia': 2, 'valor': faixa_min + (faixa_max - faixa_min) * 0.25},
            {'sequencia': 3, 'valor': faixa_min + (faixa_max - faixa_min) * 0.5},
            {'sequencia': 4, 'valor': faixa_min + (faixa_max - faixa_min) * 0.75},
            {'sequencia': 5, 'valor': faixa_max}
        ]
    
    conn.close()
    return render_template('calibracoes/medicoes.html', 
                          calibracao=calibracao, 
                          instrumento=instrumento,
                          procedimento=procedimento,
                          pontos_sugeridos=pontos_sugeridos)

@app.route('/calibracoes/<int:calibracao_id>/finalizar', methods=['GET', 'POST'])
def finalizar_calibracao(calibracao_id):
    conn = get_db_connection()
    calibracao = conn.execute('''
        SELECT c.*, i.codigo as instrumento_codigo, i.descricao as instrumento_descricao 
        FROM calibracoes c
        JOIN instrumentos i ON c.instrumento_id = i.id
        WHERE c.id = ?
    ''', (calibracao_id,)).fetchone()
    
    pontos = conn.execute('SELECT * FROM pontos_calibracao WHERE calibracao_id = ? ORDER BY sequencia', 
                         (calibracao_id,)).fetchall()
    
    # Determinar resultado geral
    todos_conformes = all(ponto['conforme'] for ponto in pontos)
    resultado = 'conforme' if todos_conformes else 'nao_conforme'
    
    if request.method == 'POST':
        observacoes = request.form['observacoes']
        
        conn.execute(
            'UPDATE calibracoes SET resultado = ?, observacoes = ?, status = ? WHERE id = ?',
            (resultado, observacoes, 'aprovada' if todos_conformes else 'reprovada', calibracao_id)
        )
        
        # Gerar certificado
        numero_certificado = f'CERT-{datetime.now().strftime("%Y%m%d")}-{calibracao_id}'
        conn.execute(
            'INSERT INTO certificados (numero, calibracao_id, data_emissao, status, data_criacao) '
            'VALUES (?, ?, ?, ?, ?)',
            (numero_certificado, calibracao_id, datetime.now(), 'emitido', datetime.now())
        )
        
        # Atualizar instrumento
        conn.execute(
            'UPDATE instrumentos SET data_ultima_calibracao = ?, data_proxima_calibracao = ? '
            'WHERE id = ?',
            (datetime.now().date(), 
             datetime.now().replace(year=datetime.now().year + 1).date(),  # Exemplo: próxima calibração em 1 ano
             calibracao['instrumento_id'])
        )
        
        conn.commit()
        conn.close()
        
        flash('Calibração finalizada com sucesso!', 'success')
        return redirect(url_for('visualizar_certificado', calibracao_id=calibracao_id))
    
    conn.close()
    return render_template('calibracoes/finalizar.html', 
                          calibracao=calibracao, 
                          pontos=pontos,
                          resultado=resultado)

@app.route('/calibracoes/<int:calibracao_id>/certificado')
def visualizar_certificado(calibracao_id):
    conn = get_db_connection()
    calibracao = conn.execute('''
        SELECT c.*, i.codigo as instrumento_codigo, i.descricao as instrumento_descricao,
        i.fabricante as instrumento_fabricante, i.modelo as instrumento_modelo,
        i.numero_serie as instrumento_numero_serie
        FROM calibracoes c
        JOIN instrumentos i ON c.instrumento_id = i.id
        WHERE c.id = ?
    ''', (calibracao_id,)).fetchone()
    
    certificado = conn.execute('SELECT * FROM certificados WHERE calibracao_id = ?', 
                              (calibracao_id,)).fetchone()
    
    pontos = conn.execute('SELECT * FROM pontos_calibracao WHERE calibracao_id = ? ORDER BY sequencia', 
                         (calibracao_id,)).fetchall()
    
    padroes = conn.execute('''
        SELECT p.* FROM padroes p
        JOIN calibracao_padroes cp ON p.id = cp.padrao_id
        WHERE cp.calibracao_id = ?
    ''', (calibracao_id,)).fetchall()
    
    conn.close()
    return render_template('certificados/visualizar.html', 
                          calibracao=calibracao,
                          certificado=certificado,
                          pontos=pontos,
                          padroes=padroes)

# Funções para cálculo de erro e incerteza
def calcular_erro(valor_lido, valor_referencia):
    """Calcula o erro de medição"""
    return valor_lido - valor_referencia

def calcular_incerteza_tipo_a(valores, nivel_confianca=0.95):
    """Calcula a incerteza Tipo A baseada em análise estatística"""
    if len(valores) < 2:
        return 0
    
    # Desvio padrão experimental
    desvio_padrao = np.std(valores, ddof=1)
    
    # Desvio padrão da média
    desvio_padrao_media = desvio_padrao / np.sqrt(len(valores))
    
    # Fator t de Student para o nível de confiança
    graus_liberdade = len(valores) - 1
    fator_t = stats.t.ppf((1 + nivel_confianca) / 2, graus_liberdade)
    
    # Incerteza expandida
    incerteza_expandida = desvio_padrao_media * fator_t
    
    return {
        'desvio_padrao': desvio_padrao,
        'desvio_padrao_media': desvio_padrao_media,
        'graus_liberdade': graus_liberdade,
        'fator_t': fator_t,
        'incerteza_expandida': incerteza_expandida
    }

def calcular_incerteza_tipo_b(fontes_incerteza):
    """Calcula a incerteza Tipo B baseada em outras fontes"""
    incertezas_quadraticas = []
    
    for fonte in fontes_incerteza:
        valor = fonte['valor']
        divisor = fonte['divisor']
        coef_sensibilidade = fonte.get('coeficiente_sensibilidade', 1.0)
        
        incerteza_padrao = valor / divisor
        contribuicao = incerteza_padrao * coef_sensibilidade
        incertezas_quadraticas.append(contribuicao ** 2)
    
    # Incerteza combinada (raiz quadrada da soma dos quadrados)
    incerteza_combinada = np.sqrt(sum(incertezas_quadraticas))
    
    return {
        'incertezas_individuais': [np.sqrt(i) for i in incertezas_quadraticas],
        'incerteza_combinada': incerteza_combinada
    }

def calcular_incerteza_combinada(incerteza_tipo_a, incerteza_tipo_b):
    """Calcula a incerteza combinada"""
    u_a = incerteza_tipo_a['desvio_padrao_media']
    u_b = incerteza_tipo_b['incerteza_combinada']
    
    # Incerteza combinada (raiz quadrada da soma dos quadrados)
    incerteza_combinada = np.sqrt(u_a**2 + u_b**2)
    
    return incerteza_combinada

def calcular_incerteza_expandida(incerteza_combinada, fator_k=2.0):
    """Calcula a incerteza expandida"""
    return incerteza_combinada * fator_k

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
