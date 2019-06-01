from PyQt5.QtCore import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget)

class Button(QToolButton):
    def __init__(self, text, suttonKioskTest, parent=None):
        super(Button, self).__init__(parent)
        self.suttonKioskTest = suttonKioskTest
        self.text = text
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
   
    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

    def mousePressEvent(self, event):
        self.suttonKioskTest.goToNextScreen()

class SuttonKioskTest(QWidget):
    def __init__(self, parent=None):
        
        super(SuttonKioskTest, self).__init__(parent)
        seanDoyleButton = Button("Sean Doyle", self)

        mainLayout = QGridLayout()
        #mainLayout.setFixedSize(500,500)
        mainLayout.addWidget(seanDoyleButton, 0, 0)
    

        self.setLayout(mainLayout)
        self.setWindowTitle("Sutton Buck Kiosk")
    
    def goToNextScreen(self):
        nameLabel = QLabel("Sean Doyle")
        amountLabel = QLabel("Sutton Bucks: 10")
        calculatorLabel = Button("Buy A calculator: 5 SB", self)
        soulLabel = Button("Buy a soul: 100 SB", self)

        mainLayout = QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(amountLabel, 1, 0)
        mainLayout.addWidget(calculatorLabel,2,0)
        mainLayout.addWidget(soulLabel,3,0)
        SuttonKioskTest().setLayout(mainLayout)


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = SuttonKioskTest()
    addressBook.show()

    sys.exit(app.exec_())

