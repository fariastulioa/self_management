from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from datetime import timedelta
from PyQt5.QtCore import QTimer, QTime, QObject, QThread, pyqtSignal, QRunnable, QThreadPool
import time


# Define a classe de worker (trabalhador de thread) a partir da classe QObject do PyQt5
class Worker(QObject):

    # Definicao de sinal para interrupcao do trabalhador
    finished = pyqtSignal()
    
    # Permite que o trabalhador receba variaveis no momento de sua instancializacao
    def __init__(self, almoco, retorno, saida, parent=None):
        QObject.__init__(self, parent)
        self.almoco = almoco
        self.retorno = retorno
        self.saida = saida
    
    # Define o metodo a ser executado repetidamente durante a execucao do programa, na thread de trabalho criada
    def long_running(self):
        time.sleep(1)
        QtWidgets.QApplication.processEvents()
        while True:
            
            agora = QTime.currentTime().toString('hh:mm')
            td_agora = timedelta(hours=int(agora.split(':')[0]), minutes=int(agora.split(':')[1]))

            # Mede o intervalo de tempo ate um dos momentos de interesse (eventos para gerar alarme)
            s_ate_almoco = (self.almoco - td_agora).seconds 
            s_ate_retorno = (self.retorno - td_agora).seconds
            s_ate_saida = (self.saida - td_agora).seconds
            
            # Checa de algum dos momentos de interesse esta proximo o suficiente (tolerancia de +/- 5 segundos)
            if -5 < s_ate_almoco < 5:
                self.alarme_almoco()

            if -5 < s_ate_retorno < 5:
                self.alarme_retorno()

            if -5 < s_ate_saida < 5:
                self.alarme_saida()

            QtWidgets.QApplication.processEvents()
            time.sleep(1)
            QtWidgets.QApplication.processEvents()


    # Define os metodos de alarme para cada um dos eventos
    def alarme_almoco(self):
        self.show_popup("ALMOCO", "Bate ponto e vai comer!")

    def alarme_retorno(self):
        self.show_popup("RETORNO", "Bate ponto e trabalha!")

    def alarme_saida(self):
        self.show_popup("SAIDA", "Bate ponto e LARGA!")

    # Define o metodo generico para geracao de popup em caso de evento
    def show_popup(self, title, message):
        QtMultimedia.QSound.play(f"./ping.wav")
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)       
        x = msg.exec_()
        print("funcao popup executada") # para fins de debug, avisa no terminal quando a funcao for executada
        time.sleep(10)
        msg.buttonClicked.connect(self.long_running())





QtMultimedia.QSound.play(f"./ping.wav")
# define a classe Ui_MainWindow, a ser criada de uma QMainWindow do PyQt5
class Ui_MainWindow(object):
    
    # Metodo a ser executado quando o botao 'Calcular' for clicado, calculando os outputs e iniciado o temporizador
    def clicked(self):
        
        print('clicked') # retorno ao terminal para indicar clique no botao, para fins de debug apenas
        self.pushButton.setText("Pronto!")
        
        # Recebe os valores de horas e minutos da hora de chegada
        hora_chega = self.timeEdit.time().hour()
        minuto_chega = self.timeEdit.time().minute()
        chegada = timedelta(hours=hora_chega, minutes=minuto_chega)

        # Recebe os valores de horas e minutos da hora de almoço        
        hora_almoca = self.timeEdit_2.time().hour()
        minuto_almoca = self.timeEdit_2.time().minute()
        almoco = timedelta(hours=hora_almoca, minutes=minuto_almoca)

        # Recebe os valores de horas e minutos a se cumprir hoje
        hora_hoje = self.timeEdit_3.time().hour()
        minuto_hoje = self.timeEdit_3.time().minute()
        hoje = timedelta(hours=hora_hoje,minutes=minuto_hoje)

        
        # Calculando os outputs
        retorno = almoco + timedelta(hours=1,minutes=1)
        saida = chegada + hoje + timedelta(hours=1, minutes=2)

        # Exibe os outputs calculados nos displays estilo LCD na janela/GUI
        self.lcdNumber.display(self.converte_display(retorno))
        self.lcdNumber_2.display(self.converte_display(saida))
        
        QtWidgets.QApplication.processEvents()
        self.almoco = almoco
        self.retorno = retorno
        self.saida = saida
        time.sleep(1)
        QtWidgets.QApplication.processEvents()
        bg_worker = Worker(almoco, retorno, saida)
        bg_worker.long_running()

    # Cria uma string de hora formatada, a partir do objeto timedelta
    def converte_display(self, td):
        horas = td.seconds // 3600
        minutos = (td.seconds%3600)//60

        minutos_str = str(minutos)
        horas_str = str(horas)
        
        if len(minutos_str) < 2:
            minutos_str = "0" + minutos_str
        if len(horas_str) < 2:
            horas_str = "0" + horas_str

        display_string = horas_str + ":" + minutos_str
        return(display_string)



    
    def setupUi(self, MainWindow):
        
        # Atributos gerais da janela/UI
        MainWindow.setObjectName("Gerenciador de Expediente")
        MainWindow.resize(320, 460)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Input para hora de chegada
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(20, 40, 120, 48))
        self.timeEdit.setObjectName("inputEntry")
        
        # Input para hora de almoco
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setGeometry(QtCore.QRect(180, 40, 120, 48))
        self.timeEdit_2.setObjectName("inputLunch")
        
        # Input para horas a se trabalhar no dia
        self.timeEdit_3 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_3.setGeometry(QtCore.QRect(20, 140, 180, 48))
        self.timeEdit_3.setObjectName("inputToDo")
        
        
        # Titulo para o input de chegada
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 120, 28))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setIndent(0)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("textEntry")
        
        # Titulo para o input de hora de almoco
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 10, 120, 28))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setIndent(0)
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("textLunch")
        
        # Titulo para o input de horas a cumprir hoje
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 180, 28))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setIndent(0)
        self.label_3.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_3.setObjectName("textToDo")
        
        
        # Display estilo LCD para output da hora de retorno
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(85, 250, 150, 60))
        self.lcdNumber.setObjectName("displayBack")
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setDigitCount(5)
        
        # Display estilo LCD para output da hora de saida
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(85, 370, 150, 60))
        self.lcdNumber_2.setObjectName("displayLeave")
        self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_2.setDigitCount(5)
        
        
        # Titulo para o display da hora de retorno
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 220, 180, 28))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setIndent(0)
        self.label_4.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_4.setObjectName("textBack")
        
        # Titulo para o display da hora de saida
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(70, 340, 180, 28))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAutoFillBackground(False)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setIndent(0)
        self.label_5.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_5.setObjectName("textLeave")
        
        # Botao para calcular os outputs a partir dos inputs e iniciar os timers para alarme
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 110, 90, 78))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setObjectName("calcButton")
        self.pushButton.clicked.connect(self.clicked)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Chegada"))
        self.label_2.setText(_translate("MainWindow", "Almoço"))
        self.label_3.setText(_translate("MainWindow", "Horas a fazer hoje"))
        self.label_4.setText(_translate("MainWindow", "Retorno do Almoço"))
        self.label_5.setText(_translate("MainWindow", "Fim de Expediente"))
        self.pushButton.setText(_translate("MainWindow", "Calcular"))


# Inicializacao da janela/UI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
