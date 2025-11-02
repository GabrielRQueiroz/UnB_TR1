import unittest

import numpy as np
import numpy.testing as npt

from camadas.fisica.transmissor.codificacoes.bipolar import Bipolar
from camadas.fisica.transmissor.codificacoes.manchester import Manchester
from camadas.fisica.transmissor.codificacoes.nrz_polar import NRZPolar


class TestCodificacoes(unittest.TestCase):
    def test_nrz_polar(self):
        codificador = NRZPolar()
        
        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])
        mensagem_4bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        sinal_codificado = codificador.codificar(mensagem_8bits)
        npt.assert_array_equal(sinal_codificado[0], [-1, 1, -1, 1, -1, 1, -1, -1])

        sinal_codificado = codificador.codificar(mensagem_4bits)
        npt.assert_array_equal(sinal_codificado[0], [-1, 1, -1, 1])
        npt.assert_array_equal(sinal_codificado[1], [-1, 1, -1, -1])

        sinal_codificado = codificador.codificar(mensagem_1bit)
        npt.assert_array_equal(sinal_codificado[0], [-1])
        npt.assert_array_equal(sinal_codificado[1], [1])
        npt.assert_array_equal(sinal_codificado[2], [-1])
        npt.assert_array_equal(sinal_codificado[3], [1])
        npt.assert_array_equal(sinal_codificado[4], [-1])
        npt.assert_array_equal(sinal_codificado[5], [1])
        npt.assert_array_equal(sinal_codificado[6], [-1])
        npt.assert_array_equal(sinal_codificado[7], [-1])

    def test_bipolar(self):
        codificador = Bipolar()
        
        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])
        mensagem_4bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        sinal_codificado = codificador.codificar(mensagem_8bits)
        npt.assert_array_equal(sinal_codificado[0], [0, 1, 0, 1, 0, 1, 0, 0])
        npt.assert_array_equal(sinal_codificado[1], [0, 0, 0, 0, 0, 0, 0, 0])
        
        sinal_codificado = codificador.codificar(mensagem_4bits)
        npt.assert_array_equal(sinal_codificado[0], [0, 1, 0, 1])
        npt.assert_array_equal(sinal_codificado[1], [0, 0, 0, 0])
        npt.assert_array_equal(sinal_codificado[2], [0, -1, 0, 0])
        
        sinal_codificado = codificador.codificar(mensagem_1bit)
        npt.assert_array_equal(sinal_codificado[0], [0])
        npt.assert_array_equal(sinal_codificado[1], [0])
        npt.assert_array_equal(sinal_codificado[2], [1])
        npt.assert_array_equal(sinal_codificado[3], [0])
        npt.assert_array_equal(sinal_codificado[4], [0])
        npt.assert_array_equal(sinal_codificado[5], [0])
        npt.assert_array_equal(sinal_codificado[6], [-1])
        npt.assert_array_equal(sinal_codificado[7], [0])
        npt.assert_array_equal(sinal_codificado[8], [0])
        npt.assert_array_equal(sinal_codificado[9], [0])
        npt.assert_array_equal(sinal_codificado[10], [1])
        npt.assert_array_equal(sinal_codificado[11], [0])
        npt.assert_array_equal(sinal_codificado[12], [0])
        npt.assert_array_equal(sinal_codificado[13], [0])
        npt.assert_array_equal(sinal_codificado[14], [0])
        npt.assert_array_equal(sinal_codificado[15], [0])

    def test_manchester(self):
        codificador = Manchester()

        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])
        mensagem_4bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        sinal_codificado = codificador.codificar(mensagem_8bits)
        npt.assert_array_equal(
            sinal_codificado[0], [1, 0, 1, 0, 1, 0, 1, 1]
        )  # 01010100 ^ 1 = 01010100
        npt.assert_array_equal(
            sinal_codificado[1], [0, 1, 0, 1, 0, 1, 0, 0]
        )  # 01010100 ^ 0 = 10101011
        
        sinal_codificado = codificador.codificar(mensagem_4bits)
        npt.assert_array_equal(sinal_codificado[0], [1, 0, 1, 0])
        npt.assert_array_equal(sinal_codificado[1], [0, 1, 0, 1])

        sinal_codificado = codificador.codificar(mensagem_1bit)
        npt.assert_array_equal(sinal_codificado[0], [1])
        npt.assert_array_equal(sinal_codificado[1], [0])


if __name__ == "__main__":
    unittest.main()
