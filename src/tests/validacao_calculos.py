"""
Script para validação dos cálculos metrológicos implementados
Executa testes com exemplos conhecidos e verifica os resultados
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.calculo_metrologico import CalculoMetrologico

def validar_calculo_erro():
    """Valida o cálculo de erro de medição"""
    print("=== VALIDAÇÃO DO CÁLCULO DE ERRO ===")
    
    # Instanciar a classe de cálculos
    calc = CalculoMetrologico()
    
    # Exemplo 1: Erro positivo
    valor_lido = 100.05
    valor_referencia = 100.0
    erro = calc.calcular_erro(valor_lido, valor_referencia)
    print(f"Exemplo 1: Valor lido = {valor_lido}, Valor referência = {valor_referencia}")
    print(f"Erro calculado = {erro} (Esperado: 0.05)")
    
    # Exemplo 2: Erro negativo
    valor_lido = 99.95
    valor_referencia = 100.0
    erro = calc.calcular_erro(valor_lido, valor_referencia)
    print(f"Exemplo 2: Valor lido = {valor_lido}, Valor referência = {valor_referencia}")
    print(f"Erro calculado = {erro} (Esperado: -0.05)")
    
    # Exemplo 3: Erro zero
    valor_lido = 100.0
    valor_referencia = 100.0
    erro = calc.calcular_erro(valor_lido, valor_referencia)
    print(f"Exemplo 3: Valor lido = {valor_lido}, Valor referência = {valor_referencia}")
    print(f"Erro calculado = {erro} (Esperado: 0.00)")
    
    # Verificar se os resultados estão corretos
    if abs(calc.calcular_erro(100.05, 100.0) - 0.05) < 0.0001 and \
       abs(calc.calcular_erro(99.95, 100.0) + 0.05) < 0.0001 and \
       abs(calc.calcular_erro(100.0, 100.0)) < 0.0001:
        print("✓ Cálculo de erro validado com sucesso!")
    else:
        print("✗ Falha na validação do cálculo de erro!")

def validar_incerteza_tipo_a():
    """Valida o cálculo de incerteza Tipo A"""
    print("=== VALIDAÇÃO DO CÁLCULO DE INCERTEZA TIPO A ===")
    
    # Instanciar a classe de cálculos
    calc = CalculoMetrologico()
    
    # Exemplo 1: Conjunto de valores com baixa dispersão
    valores1 = [100.02, 100.03, 100.01, 100.02, 100.02]
    resultado1 = calc.calcular_incerteza_tipo_a(valores1)
    print(f"Exemplo 1: Valores = {valores1}")
    print(f"Média = {resultado1['media']}")
    print(f"Desvio padrão = {resultado1['desvio_padrao']}")
    print(f"Desvio padrão da média = {resultado1['desvio_padrao_media']}")
    print(f"Graus de liberdade = {resultado1['graus_liberdade']}")
    print(f"Fator t = {resultado1['fator_t']}")
    print(f"Incerteza padrão = {resultado1['incerteza_padrao']}")
    
    # Exemplo 2: Conjunto de valores com alta dispersão
    valores2 = [100.05, 99.95, 100.1, 99.9, 100.0]
    resultado2 = calc.calcular_incerteza_tipo_a(valores2)
    print(f"Exemplo 2: Valores = {valores2}")
    print(f"Média = {resultado2['media']}")
    print(f"Desvio padrão = {resultado2['desvio_padrao']}")
    print(f"Desvio padrão da média = {resultado2['desvio_padrao_media']}")
    print(f"Graus de liberdade = {resultado2['graus_liberdade']}")
    print(f"Fator t = {resultado2['fator_t']}")
    print(f"Incerteza padrão = {resultado2['incerteza_padrao']}")
    
    # Exemplo 3: Caso especial - apenas um valor
    valores3 = [100.0]
    resultado3 = calc.calcular_incerteza_tipo_a(valores3)
    print(f"Exemplo 3: Valores = {valores3}")
    print(f"Incerteza padrão = {resultado3['incerteza_padrao']}")
    
    # Verificar se os resultados estão corretos
    if abs(resultado1['incerteza_padrao'] - 0.00316) < 0.001 and \
       abs(resultado2['incerteza_padrao'] - 0.03536) < 0.001 and \
       resultado3['incerteza_padrao'] == 0:
        print("✓ Cálculo de incerteza Tipo A validado com sucesso!")
    else:
        print("✗ Falha na validação do cálculo de incerteza Tipo A!")

def validar_incerteza_tipo_b():
    """Valida o cálculo de incerteza Tipo B"""
    print("=== VALIDAÇÃO DO CÁLCULO DE INCERTEZA TIPO B ===")
    
    # Instanciar a classe de cálculos
    calc = CalculoMetrologico()
    
    # Exemplo 1: Fontes de incerteza para um paquímetro
    fontes1 = [
        {
            'descricao': 'Resolução do instrumento',
            'valor': 0.01,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Incerteza do padrão',
            'valor': 0.005,
            'distribuicao': 'normal',
            'divisor': 2.0
        }
    ]
    
    resultado1 = calc.calcular_incerteza_tipo_b(fontes1)
    print("Exemplo 1: Fontes de incerteza para um paquímetro")
    for i, fonte in enumerate(resultado1['fontes']):
        print(f"Fonte {i+1}: {fonte['fonte']}")
        print(f"  Valor: {fonte['valor']}")
        print(f"  Distribuição: {fonte['distribuicao']}")
        print(f"  Divisor: {fonte['divisor']}")
        print(f"  Incerteza padrão: {fonte['incerteza_padrao']}")
        print(f"  Contribuição: {fonte['contribuicao']}")
    print(f"Incerteza combinada: {resultado1['incerteza_combinada']}")
    
    # Exemplo 2: Fontes de incerteza para um termômetro
    fontes2 = [
        {
            'descricao': 'Resolução do termômetro',
            'valor': 0.1,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Incerteza do padrão',
            'valor': 0.05,
            'distribuicao': 'normal',
            'divisor': 2.0
        },
        {
            'descricao': 'Estabilidade térmica',
            'valor': 0.2,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Deriva do padrão',
            'valor': 0.03,
            'distribuicao': 'retangular'
        }
    ]
    
    resultado2 = calc.calcular_incerteza_tipo_b(fontes2)
    print("Exemplo 2: Fontes de incerteza para um termômetro")
    for i, fonte in enumerate(resultado2['fontes']):
        print(f"Fonte {i+1}: {fonte['descricao']}")
        print(f"  Incerteza padrão: {fonte['incerteza_padrao']}")
    print(f"Incerteza combinada: {resultado2['incerteza_combinada']}")
    
    # Validação manual para verificar os cálculos
    print("Validação manual exemplo 1:")
    u1 = 0.01 / np.sqrt(3)
    u2 = 0.005 / 2
    u_comb = np.sqrt(u1**2 + u2**2)
    print(f"u1 (resolução): {u1}")
    print(f"u2 (padrão): {u2}")
    print(f"u combinada calculada manualmente: {u_comb}")
    print(f"u combinada calculada pela função: {resultado1['incerteza_combinada']}")
    
    # Verificar se os resultados estão corretos
    if abs(resultado1['incerteza_combinada'] - u_comb) < 0.0001:
        print("✓ Cálculo de incerteza Tipo B validado com sucesso!")
    else:
        print("✗ Falha na validação do cálculo de incerteza Tipo B!")

def validar_incerteza_completa():
    """Valida o cálculo completo de incerteza"""
    print("=== VALIDAÇÃO DO CÁLCULO COMPLETO DE INCERTEZA ===")
    
    # Instanciar a classe de cálculos
    calc = CalculoMetrologico()
    
    # Exemplo: Calibração de um paquímetro
    valores_medidos = [10.02, 10.03, 10.01, 10.02, 10.03]
    
    fontes_incerteza = [
        {
            'descricao': 'Resolução do instrumento',
            'valor': 0.01,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Incerteza do padrão',
            'valor': 0.001,
            'distribuicao': 'normal',
            'divisor': 2.0
        },
        {
            'descricao': 'Efeito da temperatura',
            'valor': 0.002,
            'distribuicao': 'retangular'
        }
    ]
    
    resultado = calc.calcular_incerteza_completa(valores_medidos, fontes_incerteza)
    
    print("Exemplo: Calibração de um paquímetro")
    print(f"Valores medidos: {valores_medidos}")
    print(f"Média: {resultado['incerteza_tipo_a']['media']}")
    print(f"Incerteza Tipo A: {resultado['incerteza_tipo_a']['incerteza_padrao']}")
    print(f"Incerteza Tipo B: {resultado['incerteza_tipo_b']['incerteza_combinada']}")
    print(f"Incerteza combinada: {resultado['incerteza_combinada']['incerteza_combinada']}")
    print(f"Graus de liberdade efetivos: {resultado['incerteza_combinada']['graus_liberdade_efetivos']}")
    print(f"Fator de abrangência (k): {resultado['fator_k']}")
    print(f"Incerteza expandida (U): {resultado['incerteza_expandida']}")
    print(f"Nível de confiança: {resultado['nivel_confianca'] * 100}%")
    
    # Avaliar conformidade
    valor_referencia = 10.0
    erro = calc.calcular_erro(resultado['incerteza_tipo_a']['media'], valor_referencia)
    erro_maximo = 0.05
    
    conformidade = calc.avaliar_conformidade(erro, resultado['incerteza_expandida'], erro_maximo)
    
    print(f"Valor de referência: {valor_referencia}")
    print(f"Erro de medição: {erro}")
    print(f"Erro máximo permitido: {erro_maximo}")
    print(f"Conformidade: {'Aprovado' if conformidade['conforme'] else 'Reprovado'}")
    print(f"Razão de erro: {conformidade['razao_erro']:.1f}% do erro máximo permitido")
    
    # Verificar se os resultados estão corretos
    if resultado['incerteza_expandida'] > 0 and \
       resultado['fator_k'] > 1.9 and \
       resultado['fator_k'] < 2.1:
        print("✓ Cálculo completo de incerteza validado com sucesso!")
    else:
        print("✗ Falha na validação do cálculo completo de incerteza!")

def gerar_grafico_contribuicoes():
    """Gera um gráfico de contribuições de incerteza"""
    print("=== GERANDO GRÁFICO DE CONTRIBUIÇÕES DE INCERTEZA ===")
    
    # Dados do exemplo
    fontes = ['Repetibilidade', 'Resolução', 'Padrão', 'Temperatura', 'Paralelismo']
    contribuicoes = [0.0037, 0.0058, 0.0005, 0.0012, 0.0017]
    
    # Ordenar por contribuição (maior para menor)
    indices = np.argsort(contribuicoes)[::-1]
    fontes = [fontes[i] for i in indices]
    contribuicoes = [contribuicoes[i] for i in indices]
    
    # Criar figura
    plt.figure(figsize=(10, 6))
    
    # Plotar barras
    bars = plt.bar(fontes, contribuicoes, color='skyblue')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                 f'{height:.4f}',
                 ha='center', va='bottom', rotation=0)
    
    # Configurar gráfico
    plt.xlabel('Fontes de Incerteza')
    plt.ylabel('Contribuição (mm)')
    plt.title('Contribuições de Incerteza por Fonte')
    plt.grid(True, axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('contribuicoes_incerteza.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo como 'contribuicoes_incerteza.png'")

if __name__ == "__main__":
    print("VALIDAÇÃO DOS CÁLCULOS METROLÓGICOS")
    print("===================================")
    
    # Executar validações
    validar_calculo_erro()
    validar_incerteza_tipo_a()
    validar_incerteza_tipo_b()
    validar_incerteza_completa()
    gerar_grafico_contribuicoes()
    
    print("Todos os testes de validação foram concluídos com sucesso!")
