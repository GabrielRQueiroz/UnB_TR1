import unittest

import numpy as np
import numpy.testing as npt

from util.sinal import Sinal


class TestFonteDeDados(unittest.TestCase):
    # T = "01010100"
    # h = "01101000"
    # e = "01100101"
    #   = "00100000"
    # q = "01110001"
    # u = "01110101"
    # i = "01101001"
    # c = "01100011"
    # k = "01101011"
    #   = "00100000"
    # b = "01100010"
    # r = "01110010"
    # o = "01101111"
    # w = "01110111"
    # n = "01101110"
    #   = "00100000"
    # f = "01100110"
    # o = "01101111"
    # x = "01111000"
    #   = "00100000"
    # j = "01101010"
    # u = "01110101"
    # m = "01101101"
    # p = "01110000"
    # s = "01110011"
    #   = "00100000"
    # o = "01101111"
    # v = "01110110"
    # e = "01100101"
    # r = "01110010"
    #   = "00100000"
    # t = "01110100"
    # h = "01101000"
    # e = "01100101"
    #   = "00100000"
    # l = "01101100"
    # a = "01100001"
    # z = "01111010"
    # y = "01111001"
    #   = "00100000"
    # d = "01100100"
    # o = "01101111"
    # g = "01100111"
    def test_fluxo_bits_1_bit_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=1)
        sinal = fonte.gerar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # T = "01010100"
        t = np.array(
            [
                0,
                1,
                0,
                1,
                0,
                1,
                0,
                0,
            ]
        )

        npt.assert_array_equal(sinal[:8], t)

    def test_fluxo_bits_2_bits_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=2)
        sinal = fonte.gerar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # T = "01" "01" "01" "00" = 1110
        t = np.array(
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 0],
            ]
        )

        npt.assert_array_equal(sinal[:4], t)

    def test_fluxo_bits_4_bits_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=4)
        sinal = fonte.gerar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # T = "0101" "0100" = 5 4
        t = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])

        npt.assert_array_equal(sinal[:2], t)

    def test_fluxo_bits_8_bits_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=8)
        sinal = fonte.gerar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # T = "01010100" = 84
        t = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])

        npt.assert_array_equal(sinal[:1], t)


if __name__ == "__main__":
    unittest.main()
