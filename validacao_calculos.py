"""
Script para validação dos cálculos metrológicos
Testa as funções de cálculo de erro e incerteza com exemplos reais
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Adicionar o diretório pai ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.calculo_metrologico import CalculoMetrologico

def validar_calculo_erro():
    """Valida o cálculo de erro de medição com exemplos"""
    print("\n=== VALIDAÇÃO DO CÁLCULO DE ERRO ===")
    
    # Exemplo 1: Erro positivo
    valor_lido_1 = 100.05
    valor_referencia_1 = 100.00
    
    # Exemplo 2: Erro negativo
    valor_lido_2 = 99.95
    valor_referencia_2 = 100.00
    
    # Exemplo 3: Sem erro
    valor_lido_3 = 100.00
    valor_referencia_3 = 100.00
    
    # Instanciar calculadora
    calc = CalculoMetrologico()
    
    # Calcular erros
    erro_1 = calc.calcular_erro(valor_lido_1, valor_referencia_1)
    erro_2 = calc.calcular_erro(valor_lido_2, valor_referencia_2)
    erro_3 = calc.calcular_erro(valor_lido_3, valor_referencia_3)
    
    # Exibir resultados
    print(f"Exemplo 1: Valor lido = {valor_lido_1}, Valor referência = {valor_referencia_1}")
    print(f"Erro calculado = {erro_1} (Esperado: 0.05)")
    
    print(f"\nExemplo 2: Valor lido = {valor_lido_2}, Valor referência = {valor_referencia_2}")
    print(f"Erro calculado = {erro_2} (Esperado: -0.05)")
    
    print(f"\nExemplo 3: Valor lido = {valor_lido_3}, Valor referência = {valor_referencia_3}")
    print(f"Erro calculado = {erro_3} (Esperado: 0.00)")
    
    # Validação
    assert abs(erro_1 - 0.05) < 1e-10, "Erro no cálculo do exemplo 1"
    assert abs(erro_2 - (-0.05)) < 1e-10, "Erro no cálculo do exemplo 2"
    assert abs(erro_3 - 0.00) < 1e-10, "Erro no cálculo do exemplo 3"
    
    print("\n✓ Cálculo de erro validado com sucesso!")

def validar_incerteza_tipo_a():
    """Valida o cálculo de incerteza Tipo A com exemplos"""
    print("\n=== VALIDAÇÃO DO CÁLCULO DE INCERTEZA TIPO A ===")
    
    # Exemplo 1: Conjunto de medições com baixa dispersão
    valores_1 = [100.02, 100.03, 100.01, 100.02, 100.02]
    
    # Exemplo 2: Conjunto de medições com alta dispersão
    valores_2 = [100.05, 99.95, 100.10, 99.90, 100.00]
    
    # Exemplo 3: Conjunto com apenas um valor (deve retornar incerteza zero)
    valores_3 = [100.00]
    
    # Instanciar calculadora
    calc = CalculoMetrologico(nivel_confianca=0.95)
    
    # Calcular incertezas
    incerteza_1 = calc.calcular_incerteza_tipo_a(valores_1)
    incerteza_2 = calc.calcular_incerteza_tipo_a(valores_2)
    incerteza_3 = calc.calcular_incerteza_tipo_a(valores_3)
    
    # Exibir resultados
    print(f"Exemplo 1: Valores = {valores_1}")
    print(f"Média = {incerteza_1['media']}")
    print(f"Desvio padrão = {incerteza_1['desvio_padrao']}")
    print(f"Desvio padrão da média = {incerteza_1['desvio_padrao_media']}")
    print(f"Graus de liberdade = {incerteza_1['graus_liberdade']}")
    print(f"Fator t = {incerteza_1['fator_t']}")
    print(f"Incerteza padrão = {incerteza_1['incerteza_padrao']}")
    
    print(f"\nExemplo 2: Valores = {valores_2}")
    print(f"Média = {incerteza_2['media']}")
    print(f"Desvio padrão = {incerteza_2['desvio_padrao']}")
    print(f"Desvio padrão da média = {incerteza_2['desvio_padrao_media']}")
    print(f"Graus de liberdade = {incerteza_2['graus_liberdade']}")
    print(f"Fator t = {incerteza_2['fator_t']}")
    print(f"Incerteza padrão = {incerteza_2['incerteza_padrao']}")
    
    print(f"\nExemplo 3: Valores = {valores_3}")
    print(f"Incerteza padrão = {incerteza_3['incerteza_padrao']}")
    
    # Validação
    assert incerteza_1['incerteza_padrao'] < incerteza_2['incerteza_padrao'], "Erro: incerteza com baixa dispersão deve ser menor"
    assert incerteza_3['incerteza_padrao'] == 0, "Erro: incerteza com um único valor deve ser zero"
    
    print("\n✓ Cálculo de incerteza Tipo A validado com sucesso!")

def validar_incerteza_tipo_b():
    """Valida o cálculo de incerteza Tipo B com exemplos"""
    print("\n=== VALIDAÇÃO DO CÁLCULO DE INCERTEZA TIPO B ===")
    
    # Exemplo 1: Fontes de incerteza típicas para um paquímetro
    fontes_1 = [
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
    
    # Exemplo 2: Fontes de incerteza para um termômetro
    fontes_2 = [
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
    
    # Instanciar calculadora
    calc = CalculoMetrologico()
    
    # Calcular incertezas
    incerteza_1 = calc.calcular_incerteza_tipo_b(fontes_1)
    incerteza_2 = calc.calcular_incerteza_tipo_b(fontes_2)
    
    # Exibir resultados
    print("Exemplo 1: Fontes de incerteza para um paquímetro")
    for i, fonte in enumerate(incerteza_1['fontes']):
        print(f"Fonte {i+1}: {fonte['fonte']}")
        print(f"  Valor: {fonte['valor']}")
        print(f"  Distribuição: {fonte['distribuicao']}")
        print(f"  Divisor: {fonte['divisor']}")
        print(f"  Incerteza padrão: {fonte['incerteza_padrao']}")
        print(f"  Contribuição: {fonte['contribuicao']}")
    print(f"Incerteza combinada: {incerteza_1['incerteza_combinada']}")
    
    print("\nExemplo 2: Fontes de incerteza para um termômetro")
    for i, fonte in enumerate(incerteza_2['fontes']):
        print(f"Fonte {i+1}: {fonte['fonte']}")
        print(f"  Incerteza padrão: {fonte['incerteza_padrao']}")
    print(f"Incerteza combinada: {incerteza_2['incerteza_combinada']}")
    
    # Validação manual para o exemplo 1
    u1 = 0.01 / np.sqrt(3)  # Resolução (retangular)
    u2 = 0.005 / 2.0        # Padrão (normal com divisor 2)
    u_combinada = np.sqrt(u1**2 + u2**2)
    
    print(f"\nValidação manual exemplo 1:")
    print(f"u1 (resolução): {u1}")
    print(f"u2 (padrão): {u2}")
    print(f"u combinada calculada manualmente: {u_combinada}")
    print(f"u combinada calculada pela função: {incerteza_1['incerteza_combinada']}")
    
    # Verificação
    assert abs(incerteza_1['incerteza_combinada'] - u_combinada) < 1e-10, "Erro no cálculo da incerteza combinada"
    
    print("\n✓ Cálculo de incerteza Tipo B validado com sucesso!")

def validar_incerteza_completa():
    """Valida o cálculo completo de incerteza com um exemplo real"""
    print("\n=== VALIDAÇÃO DO CÁLCULO COMPLETO DE INCERTEZA ===")
    
    # Exemplo: Calibração de um paquímetro
    # Valores medidos (repetições)
    valores_medidos = [10.02, 10.03, 10.01, 10.02, 10.03]
    
    # Fontes de incerteza Tipo B
    fontes_incerteza_b = [
        {
            'descricao': 'Resolução do paquímetro',
            'valor': 0.01,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Incerteza do bloco padrão',
            'valor': 0.001,
            'distribuicao': 'normal',
            'divisor': 2.0,
            'graus_liberdade': 50
        },
        {
            'descricao': 'Efeito da temperatura',
            'valor': 0.002,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Erro de paralelismo',
            'valor': 0.003,
            'distribuicao': 'retangular'
        }
    ]
    
    # Instanciar calculadora
    calc = CalculoMetrologico(nivel_confianca=0.95)
    
    # Calcular incerteza completa
    resultado = calc.calcular_incerteza_completa(valores_medidos, fontes_incerteza_b)
    
    # Exibir resultados
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
    valor_referencia = 10.00
    erro = calc.calcular_erro(resultado['incerteza_tipo_a']['media'], valor_referencia)
    erro_maximo_permitido = 0.05
    
    conformidade = calc.avaliar_conformidade(erro, resultado['incerteza_expandida'], erro_maximo_permitido)
    
    print(f"\nValor de referência: {valor_referencia}")
    print(f"Erro de medição: {erro}")
    print(f"Erro máximo permitido: {erro_maximo_permitido}")
    print(f"Conformidade: {'Aprovado' if conformidade['conforme'] else 'Reprovado'}")
    print(f"Razão de erro: {conformidade['razao_erro']:.1f}% do erro máximo permitido")
    
    # Validação
    assert resultado['incerteza_expandida'] > resultado['incerteza_combinada']['incerteza_combinada'], "Erro: incerteza expandida deve ser maior que a combinada"
    assert resultado['fator_k'] > 0, "Erro: fator k deve ser positivo"
    
    print("\n✓ Cálculo completo de incerteza validado com sucesso!")

def gerar_grafico_contribuicoes(fontes_incerteza_b):
    """Gera um gráfico de barras com as contribuições de incerteza"""
    print("\n=== GERANDO GRÁFICO DE CONTRIBUIÇÕES DE INCERTEZA ===")
    
    # Instanciar calculadora
    calc = CalculoMetrologico()
    
    # Calcular incertezas
    incerteza_b = calc.calcular_incerteza_tipo_b(fontes_incerteza_b)
    
    # Preparar dados para o gráfico
    descricoes = [fonte['fonte'] for fonte in incerteza_b['fontes']]
    contribuicoes = [fonte['contribuicao'] for fonte in incerteza_b['fontes']]
    
    # Criar DataFrame para facilitar a ordenação
    df = pd.DataFrame({
        'Fonte': descricoes,
        'Contribuição': contribuicoes
    })
    
    # Ordenar por contribuição (maior para menor)
    df = df.sort_values('Contribuição', ascending=False)
    
    # Criar gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['Fonte'], df['Contribuição'], color='skyblue')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                 f'{height:.6f}',
                 ha='center', va='bottom', rotation=0)
    
    plt.title('Contribuições de Incerteza por Fonte')
    plt.xlabel('Fontes de Incerteza')
    plt.ylabel('Contribuição (u)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('contribuicoes_incerteza.png')
    print("Gráfico salvo como 'contribuicoes_incerteza.png'")

def main():
    """Função principal para executar todas as validações"""
    print("VALIDAÇÃO DOS CÁLCULOS METROLÓGICOS")
    print("===================================")
    
    # Validar cálculos
    validar_calculo_erro()
    validar_incerteza_tipo_a()
    validar_incerteza_tipo_b()
    validar_incerteza_completa()
    
    # Gerar gráfico de exemplo
    fontes_exemplo = [
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
        },
        {
            'descricao': 'Efeito da temperatura',
            'valor': 0.003,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Erro de paralelismo',
            'valor': 0.002,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Erro de Abbe',
            'valor': 0.001,
            'distribuicao': 'retangular'
        }
    ]
    
    gerar_grafico_contribuicoes(fontes_exemplo)
    
    print("\nTodos os testes de validação foram concluídos com sucesso!")

if __name__ == "__main__":
    main()
