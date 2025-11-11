from abc import ABC, abstractmethod

import numpy as np


class ReceptorBase(ABC):
    @abstractmethod
    def processar_sinal(self, sinal: np.ndarray) -> str:
        """Processa o sinal recebido e retorna a mensagem decodificada"""
        pass
