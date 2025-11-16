import unittest

from camadas.fisica.receptor.demodulador import Demodulador
from camadas.fisica.transmissor.modulador import Modulador

import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt

from util.sinal import Sinal


class TestReceptor(unittest.TestCase):

    def test_demodulador_ask(self):
        # Gera o sinal modulado em ASK
        modulador = Modulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(bits=[0, 1, 0, 1, 0, 1, 0, 0])  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (ASK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_demodulados:
            print(bits_demodulados)
            forma_onda = formas_de_onda.get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_ask.png")
        plt.close()

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        npt.assert_array_equal(bits_demodulados, expected_bits)
        
    def test_demodulador_ask_4bits(self):
        modulador = Modulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (ASK 4 bits por símbolo)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_ask_4bits.png")
        plt.close()

        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_fsk(self):
        # Gera o sinal modulado em FSK
        modulador = Modulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(bits=[0, 1, 0, 1, 0, 1, 0, 0])  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (FSK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_demodulados:
            forma_onda = formas_de_onda.get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_fsk.png")
        plt.close()

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        npt.assert_array_equal(bits_demodulados, expected_bits)
        
    def test_demodulador_fsk_4bits(self):
        modulador = Modulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (FSK 4 bits por símbolo)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_fsk_4bits.png")
        plt.close()
        
        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )
        
        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_psk(self):
        # Gera o sinal modulado em PSK
        modulador = Modulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(bits=[0, 1, 0, 1, 0, 1, 0, 0])  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (PSK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_demodulados:
            forma_onda = formas_de_onda.get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_psk.png")
        plt.close()

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_psk_4bits(self):
        modulador = Modulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (PSK 4 bits por símbolo)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_psk_4bits.png")
        plt.close()
        
        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )
        
        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_qpsk(self):
        # Gera o sinal modulado em QPSK
        modulador = Modulador(
            modulacao="qpsk",
            frequencia_portadora=1000,
            bits_por_simbolo=2,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 1, 1, 0, 1, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="qpsk",
            frequencia_portadora=1000,
            bits_por_simbolo=2,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=2, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (QPSK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**2 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_qpsk.png")
        plt.close()

        expected_bits = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_qam16(self):
        # Gera o sinal modulado em QAM16
        modulador = Modulador(
            modulacao="16-qam",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="16-qam",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (QAM16)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_qam16.png")
        plt.close()

        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )

        npt.assert_array_equal(bits_demodulados, expected_bits)


if __name__ == "__main__":
    unittest.main()
