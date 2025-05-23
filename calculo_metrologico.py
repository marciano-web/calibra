"""
Módulo de cálculos metrológicos para o Sistema de Gestão de Calibração
Implementa funções para cálculo de erro de medição e incerteza conforme normas técnicas
"""

import numpy as np
from scipy import stats
import math

class CalculoMetrologico:
    def __init__(self, nivel_confianca=0.95):
        """
        Inicializa a classe de cálculos metrológicos
        
        Args:
            nivel_confianca: Nível de confiança para cálculos de incerteza (padrão: 0.95 ou 95%)
        """
        self.nivel_confianca = nivel_confianca
    
    def calcular_erro(self, valor_lido, valor_referencia):
        """
        Calcula o erro de medição
        
        Args:
            valor_lido: Valor indicado pelo instrumento em calibração
            valor_referencia: Valor do padrão de referência
            
        Returns:
            Erro de medição (valor_lido - valor_referencia)
        """
        return valor_lido - valor_referencia
    
    def calcular_incerteza_tipo_a(self, valores):
        """
        Calcula a incerteza Tipo A baseada em análise estatística de série de observações
        
        Args:
            valores: Lista de valores medidos
            
        Returns:
            Dicionário com resultados do cálculo de incerteza Tipo A
        """
        if len(valores) < 2:
            return {
                'desvio_padrao': 0,
                'desvio_padrao_media': 0,
                'graus_liberdade': 0,
                'fator_t': 0,
                'incerteza_padrao': 0
            }
        
        # Média dos valores
        media = np.mean(valores)
        
        # Desvio padrão experimental
        desvio_padrao = np.std(valores, ddof=1)
        
        # Desvio padrão da média (incerteza padrão Tipo A)
        desvio_padrao_media = desvio_padrao / np.sqrt(len(valores))
        
        # Graus de liberdade
        graus_liberdade = len(valores) - 1
        
        # Fator t de Student para o nível de confiança
        fator_t = stats.t.ppf((1 + self.nivel_confianca) / 2, graus_liberdade)
        
        return {
            'media': media,
            'desvio_padrao': desvio_padrao,
            'desvio_padrao_media': desvio_padrao_media,
            'graus_liberdade': graus_liberdade,
            'fator_t': fator_t,
            'incerteza_padrao': desvio_padrao_media
        }
    
    def calcular_incerteza_tipo_b(self, fontes_incerteza):
        """
        Calcula a incerteza Tipo B baseada em outras fontes que não a análise estatística
        
        Args:
            fontes_incerteza: Lista de dicionários com informações das fontes de incerteza
                Cada fonte deve conter:
                - valor: Valor da incerteza
                - distribuicao: Tipo de distribuição ('normal', 'retangular', 'triangular')
                - divisor: Divisor para converter para incerteza padrão (opcional)
                - coeficiente_sensibilidade: Coeficiente de sensibilidade (opcional, padrão: 1.0)
                - graus_liberdade: Graus de liberdade (opcional)
                
        Returns:
            Dicionário com resultados do cálculo de incerteza Tipo B
        """
        incertezas = []
        graus_liberdade = []
        
        for fonte in fontes_incerteza:
            valor = fonte['valor']
            distribuicao = fonte.get('distribuicao', 'normal')
            coef_sensibilidade = fonte.get('coeficiente_sensibilidade', 1.0)
            
            # Determinar divisor com base na distribuição
            if 'divisor' in fonte:
                divisor = fonte['divisor']
            else:
                if distribuicao == 'retangular':
                    divisor = np.sqrt(3)
                elif distribuicao == 'triangular':
                    divisor = np.sqrt(6)
                else:  # normal ou outras
                    divisor = 1.0
            
            # Calcular incerteza padrão
            incerteza_padrao = valor / divisor
            
            # Aplicar coeficiente de sensibilidade
            contribuicao = incerteza_padrao * coef_sensibilidade
            
            # Graus de liberdade (infinito para Tipo B se não especificado)
            gl = fonte.get('graus_liberdade', float('inf'))
            
            incertezas.append({
                'fonte': fonte.get('descricao', f"Fonte {len(incertezas) + 1}"),
                'valor': valor,
                'distribuicao': distribuicao,
                'divisor': divisor,
                'incerteza_padrao': incerteza_padrao,
                'coeficiente_sensibilidade': coef_sensibilidade,
                'contribuicao': contribuicao,
                'contribuicao_quadratica': contribuicao ** 2,
                'graus_liberdade': gl
            })
            
            graus_liberdade.append(gl)
        
        # Incerteza combinada (raiz quadrada da soma dos quadrados)
        soma_quadratica = sum(inc['contribuicao_quadratica'] for inc in incertezas)
        incerteza_combinada = np.sqrt(soma_quadratica)
        
        return {
            'fontes': incertezas,
            'incerteza_combinada': incerteza_combinada,
            'graus_liberdade': graus_liberdade
        }
    
    def calcular_incerteza_combinada(self, incerteza_tipo_a, incerteza_tipo_b):
        """
        Calcula a incerteza combinada a partir das incertezas Tipo A e Tipo B
        
        Args:
            incerteza_tipo_a: Resultado do cálculo de incerteza Tipo A
            incerteza_tipo_b: Resultado do cálculo de incerteza Tipo B
            
        Returns:
            Dicionário com resultados do cálculo de incerteza combinada
        """
        u_a = incerteza_tipo_a['incerteza_padrao']
        u_b = incerteza_tipo_b['incerteza_combinada']
        
        # Incerteza combinada (raiz quadrada da soma dos quadrados)
        incerteza_combinada = np.sqrt(u_a**2 + u_b**2)
        
        # Cálculo dos graus de liberdade efetivos (fórmula de Welch-Satterthwaite)
        gl_a = incerteza_tipo_a['graus_liberdade']
        gl_b_list = incerteza_tipo_b['graus_liberdade']
        
        # Contribuições para o denominador da fórmula
        if u_a > 0 and gl_a > 0:
            termo_a = (u_a**4) / gl_a
        else:
            termo_a = 0
            
        termos_b = []
        for i, gl in enumerate(gl_b_list):
            if gl < float('inf') and incerteza_tipo_b['fontes'][i]['contribuicao'] > 0:
                u_bi = incerteza_tipo_b['fontes'][i]['contribuicao']
                termos_b.append((u_bi**4) / gl)
        
        # Cálculo dos graus de liberdade efetivos
        denominador = termo_a + sum(termos_b)
        
        if incerteza_combinada > 0 and denominador > 0:
            graus_liberdade_efetivos = (incerteza_combinada**4) / denominador
        else:
            graus_liberdade_efetivos = float('inf')
        
        # Arredondar para o inteiro inferior (mais conservador)
        if graus_liberdade_efetivos < float('inf'):
            graus_liberdade_efetivos = math.floor(graus_liberdade_efetivos)
        
        return {
            'incerteza_tipo_a': u_a,
            'incerteza_tipo_b': u_b,
            'incerteza_combinada': incerteza_combinada,
            'graus_liberdade_efetivos': graus_liberdade_efetivos
        }
    
    def calcular_fator_abrangencia(self, graus_liberdade_efetivos):
        """
        Calcula o fator de abrangência k com base nos graus de liberdade efetivos
        
        Args:
            graus_liberdade_efetivos: Graus de liberdade efetivos
            
        Returns:
            Fator de abrangência k
        """
        # Se graus de liberdade for infinito, usar distribuição normal
        if graus_liberdade_efetivos == float('inf'):
            return stats.norm.ppf((1 + self.nivel_confianca) / 2)
        
        # Caso contrário, usar distribuição t de Student
        return stats.t.ppf((1 + self.nivel_confianca) / 2, graus_liberdade_efetivos)
    
    def calcular_incerteza_expandida(self, incerteza_combinada, fator_k=None, graus_liberdade_efetivos=None):
        """
        Calcula a incerteza expandida
        
        Args:
            incerteza_combinada: Incerteza combinada
            fator_k: Fator de abrangência (opcional)
            graus_liberdade_efetivos: Graus de liberdade efetivos (opcional)
            
        Returns:
            Incerteza expandida
        """
        # Se o fator k não for fornecido, calcular com base nos graus de liberdade
        if fator_k is None and graus_liberdade_efetivos is not None:
            fator_k = self.calcular_fator_abrangencia(graus_liberdade_efetivos)
        elif fator_k is None:
            # Valor padrão para k se não for possível calcular
            fator_k = 2.0
        
        return incerteza_combinada * fator_k
    
    def calcular_incerteza_completa(self, valores_medidos, fontes_incerteza_b):
        """
        Realiza o cálculo completo de incerteza
        
        Args:
            valores_medidos: Lista de valores medidos para cálculo da incerteza Tipo A
            fontes_incerteza_b: Lista de fontes de incerteza para cálculo da incerteza Tipo B
            
        Returns:
            Dicionário com todos os resultados do cálculo de incerteza
        """
        # Calcular incerteza Tipo A
        incerteza_a = self.calcular_incerteza_tipo_a(valores_medidos)
        
        # Calcular incerteza Tipo B
        incerteza_b = self.calcular_incerteza_tipo_b(fontes_incerteza_b)
        
        # Calcular incerteza combinada
        incerteza_comb = self.calcular_incerteza_combinada(incerteza_a, incerteza_b)
        
        # Calcular fator de abrangência
        fator_k = self.calcular_fator_abrangencia(incerteza_comb['graus_liberdade_efetivos'])
        
        # Calcular incerteza expandida
        incerteza_expandida = self.calcular_incerteza_expandida(
            incerteza_comb['incerteza_combinada'], 
            fator_k
        )
        
        return {
            'incerteza_tipo_a': incerteza_a,
            'incerteza_tipo_b': incerteza_b,
            'incerteza_combinada': incerteza_comb,
            'fator_k': fator_k,
            'incerteza_expandida': incerteza_expandida,
            'nivel_confianca': self.nivel_confianca
        }
    
    def avaliar_conformidade(self, erro, incerteza_expandida, erro_maximo_permitido):
        """
        Avalia a conformidade do instrumento com base no erro e na incerteza
        
        Args:
            erro: Erro de medição
            incerteza_expandida: Incerteza expandida
            erro_maximo_permitido: Erro máximo permitido para o instrumento
            
        Returns:
            Dicionário com resultado da avaliação de conformidade
        """
        # Verificar se o erro (considerando a incerteza) está dentro do limite
        conforme = abs(erro) + incerteza_expandida <= abs(erro_maximo_permitido)
        
        # Calcular a razão entre o erro e o erro máximo permitido (em %)
        if erro_maximo_permitido != 0:
            razao_erro = (abs(erro) / abs(erro_maximo_permitido)) * 100
        else:
            razao_erro = float('inf')
        
        return {
            'conforme': conforme,
            'erro': erro,
            'incerteza_expandida': incerteza_expandida,
            'erro_maximo_permitido': erro_maximo_permitido,
            'razao_erro': razao_erro
        }

# Exemplo de uso:
if __name__ == "__main__":
    # Criar instância da classe
    calc = CalculoMetrologico(nivel_confianca=0.95)
    
    # Exemplo de cálculo de erro
    valor_lido = 100.05
    valor_referencia = 100.00
    erro = calc.calcular_erro(valor_lido, valor_referencia)
    print(f"Erro de medição: {erro}")
    
    # Exemplo de cálculo de incerteza Tipo A
    valores_medidos = [100.02, 100.05, 100.03, 100.06, 100.04]
    incerteza_a = calc.calcular_incerteza_tipo_a(valores_medidos)
    print(f"Incerteza Tipo A: {incerteza_a['incerteza_padrao']}")
    
    # Exemplo de cálculo de incerteza Tipo B
    fontes_incerteza_b = [
        {
            'descricao': 'Resolução do instrumento',
            'valor': 0.01,
            'distribuicao': 'retangular'
        },
        {
            'descricao': 'Incerteza do padrão',
            'valor': 0.005,
            'distribuicao': 'normal',
            'divisor': 2.0,
            'graus_liberdade': 50
        },
        {
            'descricao': 'Deriva do padrão',
            'valor': 0.002,
            'distribuicao': 'retangular'
        }
    ]
    
    incerteza_b = calc.calcular_incerteza_tipo_b(fontes_incerteza_b)
    print(f"Incerteza Tipo B: {incerteza_b['incerteza_combinada']}")
    
    # Cálculo completo de incerteza
    resultado = calc.calcular_incerteza_completa(valores_medidos, fontes_incerteza_b)
    print(f"Incerteza expandida (k={resultado['fator_k']:.2f}): {resultado['incerteza_expandida']}")
    
    # Avaliação de conformidade
    erro_maximo_permitido = 0.1
    conformidade = calc.avaliar_conformidade(erro, resultado['incerteza_expandida'], erro_maximo_permitido)
    print(f"Conformidade: {'Aprovado' if conformidade['conforme'] else 'Reprovado'}")
    print(f"Razão de erro: {conformidade['razao_erro']:.1f}% do erro máximo permitido")
