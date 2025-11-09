import unittest

import numpy as np
import numpy.testing as npt
from matplotlib import pyplot as plt

from camadas.fisica.transmissor.banda_base import TransmissorBandaBase


class TestTransmissorBandaBase(unittest.TestCase):
    def test_nrz_polar(self):
        transmissor_8bits = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=8, debug=True
        )
        transmissor_4bits = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=4, debug=True
        )
        transmissor_1bit = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=1, debug=True
        )

        out_8bits = transmissor_8bits.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        out_4bits = transmissor_4bits.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        out_1bit = transmissor_1bit.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # [-1, 1, -1, 1, -1, 1, -1, -1] = -128 + 64 - 32 + 16 - 8 + 4 - 2 - 1 = -87
        # 1/(2**8-1) = 0.00392156862
        # => -87 * 0.00392156862 = -0.34117647058
        npt.assert_array_almost_equal(
            out_8bits[0], -0.34117647058 * transmissor_8bits.tensao_pico
        )

        # [-1, 1, -1, 1] = -8 + 4 - 2 + 1 = -5
        # 1/(2**4-1) = 0.06666666667
        # => -5 * 0.06666666667 = -0.33333333335
        npt.assert_array_almost_equal(
            out_4bits[0], -0.33333333335 * transmissor_4bits.tensao_pico
        )

        # [-1] = -1
        # 1/(2**1-1) = 1
        # => -1 * 1 = -1
        npt.assert_array_equal(out_1bit[0], -1 * transmissor_1bit.tensao_pico)

        plt.figure(figsize=(20, 6))
        plt.subplot(3, 1, 1)
        plt.title("Codificação NRZ Polar - 8 bits por símbolo")
        plt.plot(
            np.append(out_8bits.flatten(), out_8bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Codificação NRZ Polar - 4 bits por símbolo")
        plt.plot(
            np.append(out_4bits.flatten(), out_4bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Codificação NRZ Polar - 1 bit por símbolo")
        plt.plot(
            np.append(out_1bit.flatten(), out_1bit.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/transmissor_codificacao_nrz_polar.png")

    def test_bipolar(self):
        transmissor_8bits = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=8, debug=True
        )
        transmissor_4bits = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=4, debug=True
        )
        transmissor_1bit = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=1, debug=True
        )

        out_8bits = transmissor_8bits.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        out_4bits = transmissor_4bits.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        out_1bit = transmissor_1bit.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # [0, 1, 0, 1, 0, 1, 0, 0] = 64 + 16 + 4 = 84
        # 1/(2**8-1) = 0.00392156862
        # => 84 * 0.00392156862 = 0.32941176408
        npt.assert_array_almost_equal(
            out_8bits[0], [0.32941176408 * transmissor_8bits.tensao_pico]
        )
        npt.assert_array_equal(out_8bits[1], [0.0])
        # [0, -1, -1, 0, -1, 0, 0, 0] = -64 -32 -8 = -104
        # 1/(2**8-1) = 0.00392156862
        # => -104 * 0.00392156862 = -0.40784313748
        npt.assert_array_almost_equal(
            out_8bits[2], [-0.40784313748 * transmissor_8bits.tensao_pico]
        )

        # [0, 1, 0, 1] = 4 + 1 = 5
        # 1/(2**4-1) = 0.06666666667
        # => 5 * 0.06666666667 = 0.33333333335
        npt.assert_array_almost_equal(
            out_4bits[0], [0.33333333335 * transmissor_4bits.tensao_pico]
        )
        npt.assert_array_equal(out_4bits[1], [0.0])
        # [0, -1, 0, 0] = -4
        # 1/(2**4-1) = 0.06666666667
        # => -4 * 0.06666666667 = -0.26666666668
        npt.assert_array_almost_equal(
            out_4bits[2], [-0.26666666668 * transmissor_4bits.tensao_pico]
        )

        npt.assert_array_equal(out_1bit[0], [0.0])
        npt.assert_array_equal(out_1bit[1], [0.0])
        npt.assert_array_equal(out_1bit[2], [1.0 * transmissor_1bit.tensao_pico])

        plt.figure(figsize=(20, 6))
        plt.subplot(3, 1, 1)
        plt.title("Codificação Bipolar - 8 bits por símbolo")
        plt.plot(
            np.append(out_8bits.flatten(), out_8bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Codificação Bipolar - 4 bits por símbolo")
        plt.plot(
            np.append(out_4bits.flatten(), out_4bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Codificação Bipolar - 1 bit por símbolo")
        plt.plot(
            np.append(out_1bit.flatten(), out_1bit.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/transmissor_codificacao_bipolar.png")

    def test_manchester(self):
        transmissor_8bits = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=8, debug=True
        )
        transmissor_4bits = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=4, debug=True
        )
        transmissor_1bit = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=1, debug=True
        )

        out_8bits = transmissor_8bits.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        out_4bits = transmissor_4bits.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        out_1bit = transmissor_1bit.processar_sinal(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # 01010100 ^ 1 = 01010100
        # [1, 0, 1, 0, 1, 0, 1, 1] = 128 + 0 + 32 + 0 + 8 + 0 + 2 + 1 = 171
        # 1/(2**8-1) = 0.00392156862
        # => 171 * 0.00392156862 = 0.67058823502
        npt.assert_array_almost_equal(
            out_8bits[0], [0.67058823502 * transmissor_8bits.tensao_pico]
        )
        # 01010100 ^ 0 = 10101011
        # [0, 1, 0, 1, 0, 1, 0, 0] = 64 + 16 + 4 = 84
        # 1/(2**8-1) = 0.00392156862
        # => 84 * 0.00392156862 = 0.32941176408
        npt.assert_array_almost_equal(
            out_8bits[1], [0.32941176408 * transmissor_8bits.tensao_pico]
        )

        # 0101 ^ 1 = 0101
        # [1, 0, 1, 0] = 8 + 0 + 2 + 0 = 10
        # 1/(2**4-1) = 0.06666666667
        # => 10 * 0.06666666667 = 0.6666666667
        npt.assert_array_almost_equal(
            out_4bits[0], [0.6666666667 * transmissor_4bits.tensao_pico]
        )
        # 0101 ^ 0 = 1010
        # [0, 1, 0, 1] = 4 + 0 + 1 = 5
        # 1/(2**4-1) = 0.06666666667
        # => 5 * 0.06666666667 = 0.33333333335
        npt.assert_array_almost_equal(
            out_4bits[1], [0.33333333335 * transmissor_4bits.tensao_pico]
        )

        npt.assert_array_equal(out_1bit[0], [1 * transmissor_1bit.tensao_pico])
        npt.assert_array_equal(out_1bit[1], [0])

        plt.figure(figsize=(20, 6))
        plt.subplot(3, 1, 1)
        plt.title("Codificação Manchester - 8 bits por símbolo")
        plt.plot(
            np.append(out_8bits.flatten(), out_8bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Codificação Manchester - 4 bits por símbolo")
        plt.plot(
            np.append(out_4bits.flatten(), out_4bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Codificação Manchester - 1 bit por símbolo")
        plt.plot(
            np.append(out_1bit.flatten(), out_1bit.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/transmissor_codificacao_manchester.png")


if __name__ == "__main__":
    unittest.main()
