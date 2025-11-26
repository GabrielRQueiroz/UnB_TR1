from InterfaceGUI import JanelaPrincipal
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == "__main__":
    janela = JanelaPrincipal()
    janela.connect("destroy", Gtk.main_quit)
    janela.show_all()
    Gtk.main()