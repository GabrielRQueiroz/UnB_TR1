from camadas.fisica.receptor.base import ReceptorBase
import numpy as np


class Demodulador(ReceptorBase):
    def processar_sinal(self, sinal: np.ndarray) -> str:
        mensagem_decodificada = "mensagem decodificada"
        return mensagem_decodificada
