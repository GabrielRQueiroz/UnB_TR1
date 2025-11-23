import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import numpy as np
from CamadaFisica import Modulador, Demodulador, TransmissorBandaBase, Decodificador, CODIFICACOES, MODULACOES

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
        for m in MODULACOES:
            self.combo_mod.append_text(m)
        self.combo_mod.set_active(0)
        layout.pack_start(self.combo_mod, False, False, 0)
        
        # Caixa de codificacao
        self.combo_cod = Gtk.ComboBoxText()
        for c in CODIFICACOES:
            self.combo_cod.append_text(c)
        self.combo_cod.set_active(0)
        layout.pack_start(self.combo_cod, False, False, 0)

        # Frequência
        self.entry_freq = Gtk.Entry()
        self.entry_freq.set_placeholder_text("Frequência da portadora (ex: 1000)")
        self.entry_freq.set_text("1000")
        layout.pack_start(self.entry_freq, False, False, 0)

        # Bits por símbolo
        self.entry_bps = Gtk.Entry()
        self.entry_bps.set_placeholder_text("Bits por símbolo (ex: 1,2,4)")
        self.entry_bps.set_text("4")
        layout.pack_start(self.entry_bps, False, False, 0)

        # Botão Transmitir
        self.btn = Gtk.Button(label="Transmitir")
        self.btn.connect("clicked", self.on_transmitir)
        layout.pack_start(self.btn, False, False, 0)

        # Resultado
        self.output = Gtk.Label(label="")
        layout.pack_start(self.output, False, False, 0)
        
        self.sinal_modulado = None
        self.sinal_codificado = None
        
        self.connect("delete-event", Gtk.main_quit)
        self.connect("destroy", Gtk.main_quit)

    def on_transmitir(self, widget):
        mensagem = self.entry_msg.get_text()
        tipo_mod = self.combo_mod.get_active_text()
        tipo_cod = self.combo_cod.get_active_text()
        freq = float(self.entry_freq.get_text())
        bps = int(self.entry_bps.get_text())

        # CONVERTE MENSAGEM PARA BITS
        bits = np.array(
            [int(b) for b in "".join(format(ord(c), "08b") for c in mensagem)]
        )
        
        self.mod = Modulador(
            modulacao=tipo_mod,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=1000 * freq,
            debug=False,
        )
        
        self.demod = Demodulador(
            modulacao=tipo_mod,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=1000 * freq,
        )
        
        self.cod = TransmissorBandaBase(
            codificacao=tipo_cod,
            bits_por_simbolo=bps,
            frequencia_de_simbolo=freq,
            taxa_amostragem=1000 * freq,
            debug=False,
        )
        
        self.decod = Decodificador(
            codificacao=tipo_cod,
            bits_por_simbolo=bps,
            frequencia_de_simbolo=freq,
            taxa_amostragem=1000 * freq,
        )
        
        bits_codificados = self.cod.processar_sinal(bits).flatten()
        bits_modulados = self.mod.processar_sinal(bits)
        bits_decodificados = self.decod.processar_sinal(bits_codificados).flatten()
        bits_demodulados = self.demod.processar_sinal(bits_modulados).flatten()

        self.output.set_text(f"Sinal transmitido com {len(bits_modulados)} amostras!")
                
        fig = Figure(figsize=(12, 12), dpi=100)

        ax = fig.add_subplot(2, 2, 1)
        tempo = np.arange(0, len(bits_modulados)) / self.mod.taxa_amostragem
        ax.plot(tempo, bits_modulados)
        ax.set_title("Sinal Modulado")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylim(-3.5, 3.5)
        ax.set_ylabel("Amplitude")
        ax.grid()        
        
        ax2 = fig.add_subplot(2, 2, 2)
        tempo2 = np.arange(0, len(bits_demodulados) + 1) / self.demod.taxa_amostragem
        ax2.plot(tempo2, np.append(bits_demodulados, bits_demodulados[-1]), drawstyle="steps-post")
        ax2.set_title("Sinal Demodulado")
        ax2.set_xlabel("Tempo (s)")
        ax2.set_ylabel("Amplitude")
        ax2.grid()
        
        ax3 = fig.add_subplot(2, 2, 3)
        tempo3 = np.arange(0, len(bits_codificados)) / self.cod.taxa_amostragem
        ax3.plot(tempo3, bits_codificados)
        ax3.set_title("Sinal Codificado")
        ax3.set_xlabel("Tempo (s)")
        ax3.set_ylim(-3.5, 3.5)
        ax3.set_ylabel("Amplitude")
        ax3.grid()

        ax4 = fig.add_subplot(2, 2, 4)
        tempo4 = np.arange(0, len(bits_decodificados) + 1) / self.decod.taxa_amostragem
        ax4.plot(tempo4, np.append(bits_decodificados, bits_decodificados[-1]), drawstyle="steps-post")
        ax4.set_title("Sinal Decodificado")
        ax4.set_xlabel("Tempo (s)")
        ax4.set_ylabel("Amplitude")
        ax4.grid()

        subwindow = Gtk.Window()
        subwindow.set_default_size(1500, 1200)
        subwindow.set_border_width(10)
    
        self.canvas = FigureCanvas(fig)
        subwindow.add(self.canvas)
        
        subwindow.show_all()

win = JanelaPrincipal()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
