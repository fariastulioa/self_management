from datetime import timedelta
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from sys import exit


# Define a funcao que retorna o resultado de uma operacao, recebida na forma de string
# A string em questao e recebida como input do usuario
def opera(expressao):
    sinais = ["+", "-"]
    for sinal in sinais:
        if sinal in expressao:
            hora1 = expressao.split(sinal)[0]
            hora2 = expressao.split(sinal)[1]
            h1 = timedelta(minutes=int(hora1[-2:]), hours=int(hora1[:-2]))
            h2 = timedelta(minutes=int(hora2[-2:]), hours=int(hora2[:-2]))
            if sinal == "+":
                return (h1 + h2)
            if sinal == "-":
                return (h1 - h2)

# Formata o resultado (objeto timedelta) como string contendo apenas as grandezas de interesse (hora e minutos)
def formata(resultado):
    print(resultado)
    output_string = ":".join(str(resultado).split(":")[:2])
    return(output_string)

# Define uma classe de aplicação GUI herdando de QMainWindow, a janela principal do PyQt5
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle("CalculadHora")
        
        self.line = QLineEdit(self)
        
        
        self.line.move(80,20)
        self.line.resize(200,32)
        
        pybutton = QPushButton('Calcular', self)
        pybutton.clicked.connect(self.executar)
        pybutton.resize(200,32)
        pybutton.move(80,60)
        
        
        self.statusBar().showMessage("Digite a operacao acima e clica em calcular")
        
    def executar(self):

        self.line.setText(formata(opera(self.line.text())))

# Inicializa a execução do programa, que pode ser interrompida fechando a janela normalmente
app = QtWidgets.QApplication([])
janelinha = MainWindow()
janelinha.show()
exit(app.exec_())