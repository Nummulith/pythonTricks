import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QWizard, QSpinBox
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class NumberWizard(QWizard):
    valueChanged = pyqtSignal(int, str)

    def initProperty(self, mainWindow, name):
        control = self.findChild(QSpinBox, name)
        if control:
            control.valueChanged.connect(lambda value: self.valueChanged.emit(value, name))
            value = getattr(mainWindow, name, 0)
            # control.setValue(value)
            self.setValue(value, name)

    @pyqtSlot(int, str)
    def setValue(self, value, name):
        control = self.findChild(QSpinBox, name)
        if control:
            control.setValue(value)

    def __init__(self, mainWindow):
        super().__init__()

        loadUi("wizard.ui", self)

        self.initProperty(mainWindow, "LayerN")

class MainWindow(QMainWindow):
    valueChanged = pyqtSignal(int, str)

    def initProperty(self, name, value):
        control = self.findChild(QSpinBox, name)
        if control:
            control.valueChanged.connect(lambda value: self.setValue(value, name))
        self.setValue(value, name)
         
    @pyqtSlot(int, str)
    def setValue(self, value, name):
        control = self.findChild(QSpinBox, name)
        if control:
            control.setValue(value)
        setattr(self, name, value)
        self.valueChanged.emit(value, name)

    def open_wizard(self):
        self.wizard = NumberWizard(self)
        self.valueChanged.connect(self.wizard.setValue)
        self.wizard.valueChanged.connect(self.setValue)
        self.wizard.show()

    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)

        self.initProperty("LayerN", 444)

        button = QPushButton("Открыть визард", self)
        button.clicked.connect(self.open_wizard)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
