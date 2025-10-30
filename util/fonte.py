import numpy as np
import matplotlib.pyplot as plt

class FonteDeInformacao:
    ### Classe que simula uma fonte de tensão gerando uma sequência de pulsos elétricos ideais
    ### representando bits a partir de uma mensagem de texto. O sinal gerado é continuo no tempo.

    def __init__(self, mensagem: str, tempo_de_simbolo: float = 1.0/8, bits_por_simbolo: int = 4, tensao_pico: float = 3.3):
        self.mensagem = mensagem
        self.tempo_de_simbolo = tempo_de_simbolo
        self.bits_por_simbolo = bits_por_simbolo
        self.tensao_pico = tensao_pico
        self.passo_de_tensao = tensao_pico / (2 ** bits_por_simbolo - 1)
        self.sinal = self.__gerar_sinal()
        
    # Usar pyplot.pre ao invés de várias amostras
    def __gerar_sinal(self) -> np.ndarray:
        # Converte a mensagem em uma sequência de bits
        bits = ''.join(format(ord(c), '08b') for c in self.mensagem)
        bits = np.array([int(b) for b in bits])
        
        # Gera o sinal de tensão contínuo no tempo
        sinal = []

        if self.bits_por_simbolo > 1:
            num_simbolos = len(bits) // self.bits_por_simbolo
            bits = bits[:num_simbolos * self.bits_por_simbolo]  # Trunca bits extras
            simbolos = bits.reshape((num_simbolos, self.bits_por_simbolo))
            for simbolo in simbolos:
                valor_simbolo = 0
                for i, bit in enumerate(simbolo):
                    valor_simbolo += bit * (2 ** (self.bits_por_simbolo - 1 - i))
                nivel_tensao = valor_simbolo * self.passo_de_tensao
                sinal.append(nivel_tensao)
        else:
            for bit in bits:
                nivel_tensao = bit * self.passo_de_tensao
                sinal.append(nivel_tensao)

        return np.array(sinal, dtype=float)
    
    def plotar_sinal(self):
        tempo_total = len(self.sinal) * self.tempo_de_simbolo
        tempo = np.linspace(0, tempo_total, len(self.sinal), endpoint=False)
        
        plt.figure(figsize=(10, 4))
        plt.plot(tempo, self.sinal, drawstyle='steps-post')
        plt.title("Sinal Gerado pela Fonte de Informação")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Tensão (V)")
        plt.grid()
        plt.show()
