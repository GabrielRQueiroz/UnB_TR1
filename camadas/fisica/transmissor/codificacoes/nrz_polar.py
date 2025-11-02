import numpy as np

from .base import CodificacaoBase

class NRZPolar(CodificacaoBase):
    """ Codificação NRZ Polar: 
        Bits 1 são representados por +1 e bits 0 por -1.
    """
    def codificar(self, bits: np.ndarray) -> np.ndarray:
        saida = []
        for simbolo in bits:
            if simbolo.ndim > 0:
                simbolo_saida = []
                for b in simbolo:
                    if b == 1:
                        simbolo_saida.append(1.0)
                    else:
                        simbolo_saida.append(-1.0)

                saida.append(simbolo_saida)
            else:
                if simbolo == 1:
                    saida.append(1.0)
                else:
                    saida.append(-1.0)
            
        return np.array(saida)
