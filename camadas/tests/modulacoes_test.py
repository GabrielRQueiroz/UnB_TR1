import unittest

import numpy as np
import numpy.testing as npt
from matplotlib import pyplot as plt

import camadas.fisica.transmissor.modulacoes as modulacoes
from util.sinal import Sinal


class TestModulacoes(unittest.TestCase):
    def test_ask_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=1)
        decimal_mensagem_1bit = sinal.binario_para_decimal(
            np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0])
        )
        sinal.bits_por_simbolo = 4
        decimal_mensagem_4bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1], [0, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 0]])
        )
        sinal.bits_por_simbolo = 8
        decimal_mensagem_8bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0]])
        )

        ask_1bit = modulacoes.ASK(bits_por_simbolo=1)
        ask_4bits = modulacoes.ASK(bits_por_simbolo=4)
        ask_8bits = modulacoes.ASK(bits_por_simbolo=8)

        amplitudes_1bit = ask_1bit.gerar_parametros(decimal_mensagem_1bit)
        amplitudes_4bits = ask_4bits.gerar_parametros(decimal_mensagem_4bits)
        amplitudes_8bits = ask_8bits.gerar_parametros(decimal_mensagem_8bits)

        npt.assert_array_almost_equal(
            amplitudes_1bit, decimal_mensagem_1bit
        )

        npt.assert_array_almost_equal(
            amplitudes_4bits, decimal_mensagem_4bits
        )

        npt.assert_array_almost_equal(
            amplitudes_8bits, decimal_mensagem_8bits
        )

        plt.figure(figsize=(10, 4))
        plt.subplot(3, 1, 1)
        plt.title("Modulação ASK - Amplitudes dos Símbolos (1 bit por símbolo)")
        plt.stem(amplitudes_1bit)
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Modulação ASK - Amplitudes dos Símbolos (4 bits por símbolo)")
        plt.stem(amplitudes_4bits)
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Modulação ASK - Amplitudes dos Símbolos (8 bits por símbolo)")
        plt.stem(amplitudes_8bits)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_ask.png")

    def test_fsk_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=1)
        decimal_mensagem_1bit = sinal.binario_para_decimal(
            np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0])
        )
        sinal.bits_por_simbolo = 4
        decimal_mensagem_4bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1], [0, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 0]])
        )
        sinal.bits_por_simbolo = 8
        decimal_mensagem_8bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0]])
        )

        fsk_1bit = modulacoes.FSK(bits_por_simbolo=1)
        fsk_4bits = modulacoes.FSK(bits_por_simbolo=4)
        fsk_8bits = modulacoes.FSK(bits_por_simbolo=8)

        frequencias_1bit = fsk_1bit.gerar_parametros(decimal_mensagem_1bit)
        frequencias_4bits = fsk_4bits.gerar_parametros(decimal_mensagem_4bits)
        frequencias_8bits = fsk_8bits.gerar_parametros(decimal_mensagem_8bits)

        npt.assert_array_almost_equal(
            frequencias_1bit,
            decimal_mensagem_1bit / (2**1 - 1),
        )

        npt.assert_array_almost_equal(
            frequencias_4bits, decimal_mensagem_4bits / (2**4 - 1)
        )

        npt.assert_array_almost_equal(
            frequencias_8bits, decimal_mensagem_8bits / (2**8 - 1)
        )
        
        plt.figure(figsize=(10, 4))
        plt.subplot(3, 1, 1)
        plt.title("Modulação FSK - Frequências dos Símbolos (1 bit por símbolo)")
        plt.stem(frequencias_1bit)
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Modulação FSK - Frequências dos Símbolos (4 bits por símbolo)")
        plt.stem(frequencias_4bits)
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Modulação FSK - Frequências dos Símbolos (8 bits por símbolo)")
        plt.stem(frequencias_8bits)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_fsk.png")
