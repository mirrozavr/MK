import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
from struct import *
import functools



class Window(QMainWindow): # главное окно
    def __init__(self):
        super(Window, self).__init__() # возвращает родительский объект

        uic.loadUi("D:/pythonProject/labs/terminal.ui", self) # Возвращает ссылку на объект формы, сконвертированный из формы диайнера в питон объект
        self.setWindowTitle('GUI') #заголовок окна
        #self.show()

        self.serial = QSerialPort() # доступ к последовательным портам
        self.serial.setBaudRate(115200) # cкорость передачи данных для желаемого направления (115200 - частота передачи данных для UART).
        portList = [] # список доступных портов
        portType = []
        ports = QSerialPortInfo().availablePorts() # информация о доступных последовательных портах
        #print(ports)
        for port in ports:
            portList.append(port.portName()) # заполняем список
            portType.append(port.description())
        # print(portList)
        # print(portType)
        self.comL.addItems(portList) # загружаем полученный список в ComboBox

        self.serial.readyRead.connect(self.onRead) # считываем данные,если они есть

        self.OpenB.clicked.connect(self.onOpen) # открываем порт по кнопке
        self.CloseB.clicked.connect(self.onClose)

        self.LED_blue.stateChanged.connect(self.turn_on_blue) # отвечает за состояние диода
        self.LED_red.stateChanged.connect(self.turn_on_red)
        self.LED_green.stateChanged.connect(self.turn_on_green)

    def onOpen(self): # открыть порт
        self.serial.setPortName(self.comL.currentText()) # меняем имя порта
        self.serial.open(QIODevice.ReadWrite) # открываем порт для чтения и записи

    def onClose(self): # закрыть порт
        self.serial.close()

    def onRead(self): # чтение данных, которые отправляется в порт
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split('.')


    def serialSend(self, data): # конвертирование значений и запись данных
        txs = data
        self.serial.write(txs)

    def turn_on_blue(self, val):
        message = b'\xAB\xA1\x01'
        self.serialSend(message)

    def turn_on_red(self, val):
        message = b'\xAB\xA2\x01'
        self.serialSend(message)

    def turn_on_green(self, val):
        message = b'\xAB\xA3\x01'
        self.serialSend(message)


def application(): # создание окна
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())


application()
