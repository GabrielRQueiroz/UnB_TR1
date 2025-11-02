import matplotlib.pyplot as plt
import numpy as np

from util.ruido import Ruido
from util.sinal import Sinal

from .base import TransmissorBase
from .codificacoes.bipolar import Bipolar
from .codificacoes.manchester import Manchester
from .codificacoes.nrz_polar import NRZPolar

CODIFICACOES = {
    "manchester": Manchester,
    "nrz_polar": NRZPolar,
    "bipolar": Bipolar,
}


class TransmissorBandaBase(TransmissorBase):
    def __init__(
        self,
        codificacao: str,
        taxa_amostragem: float = 1000,
        tempo_de_simbolo: float = 1.0 / 8,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        debug=False,
    ):
        super().__init__(taxa_amostragem)
        if codificacao.lower() not in CODIFICACOES:
            raise ValueError(f"Codificação '{codificacao}' não implementada.")
        self.codificador = CODIFICACOES[codificacao]()
        self.tempo_de_simbolo = tempo_de_simbolo
        self.bits_por_simbolo = bits_por_simbolo
        self.tensao_pico = tensao_pico
        self.debug = (
            debug  # Flag para printar sinal intermediário e pular adição de ruído
        )

    def processar_sinal(self, mensagem: str) -> np.ndarray:
        # Converte a mensagem em uma sequência de bits
        sinal = Sinal(self.bits_por_simbolo)
        ruido = Ruido()
        bits = sinal.gerar_sinal(mensagem)

        # Codifica os bits usando o esquema de codificação selecionado
        sinal_codificado = self.codificador.codificar(bits)

        if self.debug:
            print("DEBUG: ", sinal_codificado)

        # Aplica valor decimal de cada símbolo
        sinal_codificado = sinal.binario_para_decimal(sinal_codificado)

        sinal_codificado *= (
            self.tensao_pico
        )  # Ajusta o nível de tensão do sinal codificado

        if not self.debug:
            sinal_codificado += ruido.gerar_ruido(
                sinal_codificado
            )  # Adiciona ruído ao sinal codificado

        return sinal_codificado

    def plotar_sinal(self, sinal: np.ndarray, tempo_de_simbolo: float) -> None:
        tempo_total = len(sinal) * tempo_de_simbolo
        tempo = np.linspace(0, tempo_total, len(sinal), endpoint=False)

        plt.figure(figsize=(10, 4))
        plt.plot(tempo, sinal, drawstyle="steps-post")
        plt.title("Sinal Gerado pela Fonte de Informação")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Tensão (V)")
        plt.grid()
        plt.show()
