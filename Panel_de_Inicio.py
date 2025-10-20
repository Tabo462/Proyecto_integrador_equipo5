from tkinter import Tk, Frame
from container import Container


# Esta clase crea la ventana principal y controla qué pantalla se muestra
class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Caja registradora")  # Nombre de la ventana
        self.resizable(False, False)  # No dejamos que cambien el tamaño
        self.configure(bg="#FDC32F")  # Color de fondo
        self.geometry("800x400+120+20")  # Tamaño y posición en la pantalla

        self.container = Frame(self, bg="#DE2924")  # Caja que contiene las pantallas
        self.container.pack(fill="both", expand=True)  # Que ocupe todo el espacio

        # Guardamos las pantallas por clase para poder mostrarlas fácil
        self.frames = {
            Container: None
        }

        self.load_frames()  # Creamos las pantallas
        self.show_frames(Container)  # Mostramos la pantalla inicial

    # Crea cada pantalla y la guarda en el diccionario
    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame

    # Muestra la pantalla que le digas
    def show_frames(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    # Trata de aplicar un tema bonito si la librería está instalada
    def set_theme(self):
        try:
            from ttkthemes import ThemedStyle
            style = ThemedStyle(self)
            style.set_theme("breeze")  # Cambia esto por otro tema si quieres
        except ImportError:
            pass  # Si no está instalado, seguimos con el tema por defecto

# Punto de entrada para correr la app
def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()