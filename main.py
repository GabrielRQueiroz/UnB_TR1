import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import numpy as np
from camadas.fisica.transmissor.modulador import Modulador

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class JanelaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__(title=" Transmissor ")
        self.set_default_size(500, 400)

        layout = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.add(layout)

        # Entrada da mensagem
        self.entry_msg = Gtk.Entry()
        self.entry_msg.set_placeholder_text("Digite a mensagem")
        layout.pack_start(self.entry_msg, False, False, 0)

        # Caixa de modulação
        self.combo_mod = Gtk.ComboBoxText()
        for m in ["ask", "fsk", "psk", "qpsk", "16-qam"]:
            self.combo_mod.append_text(m)
        self.combo_mod.set_active(0)
        layout.pack_start(self.combo_mod, False, False, 0)

        # Frequência
        self.entry_freq = Gtk.Entry()
        self.entry_freq.set_placeholder_text("Frequência da portadora (ex: 1000)")
        layout.pack_start(self.entry_freq, False, False, 0)

        # Bits por símbolo
        self.entry_bps = Gtk.Entry()
        self.entry_bps.set_placeholder_text("Bits por símbolo (ex: 1,2,4)")
        layout.pack_start(self.entry_bps, False, False, 0)

        # Botão Transmitir
        self.btn = Gtk.Button(label="Transmitir")
        self.btn.connect("clicked", self.on_transmitir)
        layout.pack_start(self.btn, False, False, 0)

        # Resultado
        self.output = Gtk.Label(label="")
        layout.pack_start(self.output, False, False, 0)

    def on_transmitir(self, widget):
        mensagem = self.entry_msg.get_text()
        tipo_mod = self.combo_mod.get_active_text()
        freq = float(self.entry_freq.get_text())
        bps = int(self.entry_bps.get_text())

        # CONVERTE MENSAGEM PARA BITS
        bits = np.array(
            [int(b) for b in "".join(format(ord(c), "08b") for c in mensagem)]
        )

        # CRIA O MODULADOR
        self.mod = Modulador(
            modulacao=tipo_mod,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=1000 * freq,
            debug=False,
        )

        # PROCESSA O SINAL
        self.sinal = self.mod.processar_sinal(bits)

        self.output.set_text(f"Sinal transmitido com {len(self.sinal)} amostras!")

        plot_window = PlotSubwindow(self.sinal, self.mod.taxa_amostragem)
        plot_window.show_all()


class PlotSubwindow(Gtk.Window):
    def __init__(self, sinal: np.ndarray, taxa_amostragem: int):
        super().__init__(title="Sinal Modulado")
        self.set_default_size(800, 600)

        fig = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(fig)
        self.add(self.canvas)

        ax = fig.add_subplot(1, 1, 1)
        tempo = np.arange(0, len(sinal)) / taxa_amostragem
        ax.plot(tempo, sinal)
        ax.set_title("Sinal Modulado")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Amplitude")
        ax.grid()

        self.show_all()


win = JanelaPrincipal()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
