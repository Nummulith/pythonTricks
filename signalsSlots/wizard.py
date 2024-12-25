import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QWizard, QSpinBox
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class NumberWizard(QWizard):
    valueChanged = pyqtSignal(int, str)  # Добавляем второй параметр для идентификатора источника

    def __init__(self, initial_value=0, initial_value2=0):
        super().__init__()

        self.setWindowTitle("Number Wizard")

        # Load the entire wizard from a single .ui file
        loadUi("wizard.ui", self)

        # Первое значение
        self.spinBoxWizard1 = self.findChild(QSpinBox, "spinBoxWizard1")
        self.spinBoxWizard1.setValue(initial_value)
        self.spinBoxWizard1.valueChanged.connect(lambda value: self.valueChanged.emit(value, "Wizard1"))

        # Второе значение
        self.spinBoxWizard2 = self.findChild(QSpinBox, "spinBoxWizard2")
        self.spinBoxWizard2.setValue(initial_value2)
        self.spinBoxWizard2.valueChanged.connect(lambda value: self.valueChanged.emit(value, "Wizard2"))

    @pyqtSlot(int, str)
    def setValue(self, value, source):
        if source == "Wizard1" or source == "Main1":
            self.spinBoxWizard1.setValue(value)
        elif source == "Wizard2" or source == "Main2":
            self.spinBoxWizard2.setValue(value)

class MainWindow(QMainWindow):
    valueChanged = pyqtSignal(int, str)  # Добавляем идентификатор источника

    def __init__(self):
        super().__init__()

        self._value1 = 0
        self._value2 = 0

        self.setWindowTitle("Главное окно")

        # Первое значение
        self.spinBoxMain1 = QSpinBox()
        self.spinBoxMain1.setValue(self._value1)
        self.spinBoxMain1.valueChanged.connect(lambda value: self.setValue(value, "Main1"))

        # Второе значение
        self.spinBoxMain2 = QSpinBox()
        self.spinBoxMain2.setValue(self._value2)
        self.spinBoxMain2.valueChanged.connect(lambda value: self.setValue(value, "Main2"))

        button = QPushButton("Открыть визард")
        button.clicked.connect(self.open_wizard)

        layout = QVBoxLayout()
        layout.addWidget(self.spinBoxMain1)
        layout.addWidget(self.spinBoxMain2)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    @pyqtSlot(int, str)
    def setValue(self, value, source):
        if source == "Main1" or source == "Wizard1":
            self._value1 = value
            self.spinBoxMain1.setValue(value)
        elif source == "Main2" or source == "Wizard2":
            self._value2 = value
            self.spinBoxMain2.setValue(value)
        self.valueChanged.emit(value, source)

    def getValue1(self):
        return self._value1

    def getValue2(self):
        return self._value2

    def open_wizard(self):
        self.wizard = NumberWizard(self.getValue1(), self.getValue2())
        self.valueChanged.connect(self.wizard.setValue)
        self.wizard.valueChanged.connect(self.setValue)
        self.wizard.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
