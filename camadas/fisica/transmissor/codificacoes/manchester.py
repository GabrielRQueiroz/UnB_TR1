import numpy as np
from .base import CodificacaoBase

class Manchester(CodificacaoBase):
    """ Codificação Manchester: 
        Faz uma operação XOR entre os bits da mensagem e o clock.
    """
    def codificar(self, bits: np.ndarray) -> np.ndarray:
        clock = self.__clock(bits)
        saida = []
        for i, clk in enumerate(clock):
            i_mensagem = i // 2 

            mais_de_um_bit_por_simbolo = (
                bits[i_mensagem].ndim > 0 if i_mensagem < len(bits) else False
            )

            if clk == 1.0: # XOR com 1 === inverte bits
                if mais_de_um_bit_por_simbolo:
                    simbolo_saida = []
                    for b in bits[i_mensagem]:
                        if b == 1:
                            simbolo_saida.append(0.0)
                        else:
                            simbolo_saida.append(1.0)
                    saida.append(simbolo_saida)
                else:
                    if bits[i_mensagem] == 1:
                        saida.append(0.0)
                    else:
                        saida.append(1.0)
            else: # XOR com 0 === mantém bits
                if mais_de_um_bit_por_simbolo:
                    simbolo_saida = []
                    for b in bits[i_mensagem]:
                        if b == 1:
                            simbolo_saida.append(1.0)
                        else:
                            simbolo_saida.append(0.0)
                    saida.append(simbolo_saida)
                else:
                    if bits[i_mensagem] == 1:
                        saida.append(1.0)
                    else:
                        saida.append(0.0)
                

        return np.array(saida)
    
    def __clock(self, bits: np.ndarray) -> np.ndarray:
        clock = np.zeros(len(bits) * 2)

        for i in range(len(clock)):
            if i % 2 == 0:
                clock[i] = 1.0
            else:
                clock[i] = 0.0
        return clock

            
    