import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad


class Sinal:
    """Classe que converte uma mensagem de texto em um sinal digital."""

    def __init__(self, bits_por_simbolo: int = 1, taxa_amostragem: int = 1000):
        self._bits_por_simbolo = bits_por_simbolo
        self._taxa_amostragem = taxa_amostragem

    @property
    def bits_por_simbolo(self) -> int:
        return self._bits_por_simbolo

    @property
    def taxa_amostragem(self) -> int:
        return self._taxa_amostragem

    @bits_por_simbolo.setter
    def bits_por_simbolo(self, valor: int):
        self._bits_por_simbolo = valor

    @staticmethod
    def gerar_sinal_binario(mensagem: str) -> np.ndarray:
        """Converte a mensagem em uma sequência de bits."""
        bits = "".join(format(ord(c), "08b") for c in mensagem)
        bits = np.array([int(b) for b in bits])
        return bits

    def gerar_pulso_tensao(
        self, simbolos_decimais: np.ndarray, tempo_de_simbolo: float = 1.0
    ) -> np.ndarray:
        """
        Gera uma curva de tensão simulando um pulso elétrico utilizando série de Fourier
        simbolos_decimais é um array com os símbolos em decimal -> [simbolo1, simbolo2, simbolo3, ...].
        Devolve um array numpy com a forma de onda de cada símbolo -> [[forma_de_onda1], [forma_de_onda2], [forma_de_onda3], ...].
        """

        if self.bits_por_simbolo == 1:
            simbolos_decimais = np.reshape(
                simbolos_decimais, (-1, 1)
            )  # trata cada bit como um símbolo

        forma_de_onda = self.__serie_de_fourier(
            simbolos_decimais, tempo_de_simbolo=tempo_de_simbolo, harmonicas=8
        )

        return forma_de_onda

    def sequencia_de_bits_para_simbolos(
        self, bits: np.ndarray
    ) -> np.ndarray:  # TODO testar
        """Agrupa a sequência de bits em símbolos de acordo com bits_por_simbolo."""
        if self.bits_por_simbolo == 1:
            return bits

        num_simbolos = len(bits) // self.bits_por_simbolo
        bits = bits[: num_simbolos * self.bits_por_simbolo]
        simbolos = bits.reshape((num_simbolos, self.bits_por_simbolo))

        return simbolos

    def binario_para_decimal(self, bits: np.ndarray) -> np.ndarray:
        """Converte uma sequência de símbolos em uma sequência de seus respectivos decimais, normalizados (de 0 a 1)."""
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

    def decimal_para_binario(self, decimal: int) -> np.ndarray:
        """Converte um número decimal em sua representação binária com bits_por_simbolo bits."""
        formato = "{0:0" + str(self.bits_por_simbolo) + "b}"
        binario_str = formato.format(decimal)
        binario = np.array([int(bit) for bit in binario_str])
        return binario

    def __serie_de_fourier(
        self, simbolos: np.ndarray, tempo_de_simbolo: float, harmonicas: int
    ) -> np.ndarray:
        """Gera uma série de Fourier."""
        periodo = len(simbolos) * tempo_de_simbolo
        t = np.linspace(0, periodo, int(periodo * self.taxa_amostragem), endpoint=False)
        c = 2 / periodo * np.sum(simbolos)

        resultado = np.zeros_like(t) + c / 2

        for n in range(1, harmonicas + 1):
            y_an = lambda t: simbolos[int(t // tempo_de_simbolo)] * np.sin(
                2 * np.pi * n * t / periodo
            )
            y_bn = lambda t: simbolos[int(t // tempo_de_simbolo)] * np.cos(
                2 * np.pi * n * t / periodo
            )

            an = (
                np.sin(2 * np.pi * n * t / periodo)
                * (2.0 / periodo)
                * np.array(quad(y_an, 0, periodo))[0]  # descarta o valor do erro
            )
            bn = (
                np.cos(2 * np.pi * n * t / periodo)
                * (2.0 / periodo)
                * np.array(quad(y_bn, 0, periodo))[0]  # descarta o valor do erro
            )

            resultado += an + bn

        return np.reshape(resultado, (len(simbolos), -1))
