import numpy as np


class Sinal:
    """Classe que converte uma mensagem de texto em um sinal digital."""

    def __init__(self, bits_por_simbolo: int = 1):
        self.bits_por_simbolo = bits_por_simbolo

    # Usar pyplot.pre ao invés de várias amostras
    def gerar_sinal(self, mensagem: str) -> np.ndarray:
        """Converte a mensagem em uma sequência de bits."""
        bits = "".join(format(ord(c), "08b") for c in mensagem)
        bits = np.array([int(b) for b in bits])

        # Gera o sinal de tensão contínuo no tempo

        if self.bits_por_simbolo > 1:
            num_simbolos = len(bits) // self.bits_por_simbolo
            bits = bits[: num_simbolos * self.bits_por_simbolo]  # Trunca bits extras
            bits = bits.reshape((num_simbolos, self.bits_por_simbolo))

        return bits

    def binario_para_decimal(self, bits: np.ndarray) -> np.ndarray:
        """Converte uma sequência de símbolos em uma sequência de seus respectivos decimais."""
        sinal = []
        passo_de_tensao = 1 / (2**self.bits_por_simbolo - 1)

        if self.bits_por_simbolo > 1:
            for simbolo in bits:
                valor_simbolo = 0
                for i, bit in enumerate(simbolo):
                    valor_simbolo += bit * (2 ** (self.bits_por_simbolo - i - 1))
                nivel_tensao = valor_simbolo * passo_de_tensao
                sinal.append(nivel_tensao)
        else:
            for bit in bits:
                nivel_tensao = bit * passo_de_tensao
                sinal.append(nivel_tensao)

        return np.array(sinal)
