from camadas.fisica.receptor.base import ReceptorBase
import numpy as np

class Decodificador(ReceptorBase):
    def __init__(
        self,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        taxa_amostragem: int = 1000,
        debug: bool = False,
    ):
        super().__init__()
        self.bits_por_simbolo = bits_por_simbolo
        self.tensao_pico = tensao_pico
        self.taxa_amostragem = taxa_amostragem
        self.debug = debug

    def processar_sinal(self, sinal: np.ndarray) -> str:
        # Fazer detecção de forma de onda:
        # 0) guardar em um mini db os a forma de onda de cada símbolo possível da codificacao esperada
        # 1) amostra o sinal recebido
        # 2) comprara com os níveis de tensão do mini db com um limiar de tolerância  
        
        mensagem_decodificada = "mensagem decodificada" 
        return mensagem_decodificada