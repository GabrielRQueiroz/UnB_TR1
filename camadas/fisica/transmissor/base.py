from abc import ABC, abstractmethod

import numpy as np

from util.sinal import Sinal


class TransmissorBase(ABC):
    @abstractmethod
    def processar_sinal(self, mensagem: str) -> np.ndarray:
        """Processa a mensagem de entrada e retorna o sinal modulado"""
        pass

    def gerar_dicionario_de_formas_de_onda(self) -> dict:
        """Gera um dicionário com as formas de onda de cada símbolo possível."""
        sinal = Sinal(self.bits_por_simbolo, self.taxa_amostragem)
        num_simbolos = 2**self.bits_por_simbolo
        simbolos = np.arange(num_simbolos)
        dicionario: dict[int, np.ndarray] = {}

        for simbolo in simbolos:
            bits = sinal.decimal_para_binario(simbolo)
            sinal_eletrico = self.processar_sinal(bits)
            dicionario[simbolo] = sinal_eletrico

        return dicionario
