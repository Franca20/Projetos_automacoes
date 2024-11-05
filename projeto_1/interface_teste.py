from PySide6.QtWidgets import QApplication, QMainWindow
from interface_cadastro import Ui_MainWindow as interface
import sys

class MainWindow(QMainWindow, interface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setFixedHeight(330)
        self.setFixedWidth(400)

        self.salvar_files.clicked.connect(self.limpar_campos)

    def limpar_campos(self):
        self.cliente.clear()
        self.produto.clear()
        self.quantidade.clear()
        self.categoria.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()