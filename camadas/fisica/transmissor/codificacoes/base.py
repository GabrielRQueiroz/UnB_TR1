from abc import ABC, abstractmethod

import numpy as np

class CodificacaoBase(ABC):
    """Interface para esquemas de codificação de linha."""

    @abstractmethod
    def codificar(self, bits: np.ndarray, taxa_amostragem: float, **args) -> np.ndarray:
        """Retorna o sinal codificado em tensão (níveis elétricos)."""
        pass
