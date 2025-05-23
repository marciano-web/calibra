import matplotlib.pyplot as plt
import numpy as np
import os

# Diretório para salvar os gráficos
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'img')
os.makedirs(output_dir, exist_ok=True)

def gerar_grafico_erros():
    """
    Gera um gráfico de erros de calibração para o exemplo do certificado
    """
    # Dados do exemplo
    pontos_nominais = [0, 25, 50, 75, 100, 150]
    erros = [0.002, 0.015, 0.022, 0.018, 0.025, 0.030]
    incertezas = [0.008, 0.010, 0.014, 0.012, 0.016, 0.018]
    
    # Limites de erro
    erro_max = 0.05
    erro_min = -0.05
    
    # Criar figura
    plt.figure(figsize=(10, 6))
    
    # Plotar área de conformidade
    plt.fill_between([-5, 155], erro_max, erro_min, color='lightgreen', alpha=0.3, label='Área de conformidade')
    
    # Plotar linhas de limite
    plt.axhline(y=erro_max, color='r', linestyle='--', label='Erro máximo permitido')
    plt.axhline(y=erro_min, color='r', linestyle='--')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Plotar pontos de erro com barras de incerteza
    plt.errorbar(pontos_nominais, erros, yerr=incertezas, fmt='o', color='blue', 
                 ecolor='blue', elinewidth=1, capsize=5, label='Erro de medição')
    
    # Plotar linha de tendência
    plt.plot(pontos_nominais, erros, 'b-', alpha=0.7)
    
    # Configurar gráfico
    plt.xlabel('Valor Nominal (mm)')
    plt.ylabel('Erro (mm)')
    plt.title('Erros de Medição com Incertezas Expandidas')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Ajustar limites
    plt.xlim(-5, 155)
    plt.ylim(-0.06, 0.06)
    
    # Salvar gráfico
    output_path = os.path.join(output_dir, 'grafico_erros.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def gerar_grafico_contribuicoes():
    """
    Gera um gráfico de contribuições de incerteza para o exemplo do certificado
    """
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
    output_path = os.path.join(output_dir, 'contribuicoes_incerteza.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

if __name__ == "__main__":
    gerar_grafico_erros()
    gerar_grafico_contribuicoes()
    print("Gráficos gerados com sucesso!")
