from PyQt5.QtCore import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget, QStackedWidget)

from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget
import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

class SchoolClass:
    def __init__(self, name, students):
        self.name = name
        self.students = students

class Student:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

student1 = Student("Student1", 10)
student2 = Student("Student2", 20)
student3 = Student("Student3", 30)
student4 = Student("Student4", 40)
student5 = Student("Student5", 55)
student6 = Student("Student6", 70)
student7 = Student("Student7", 300)

calcClass = SchoolClass("APCalc", [student1, student2])
statsClass = SchoolClass("APStats", [student3, student4, student5])
IM3Class = SchoolClass("IM3", [student6, student7])

variableClassList = [calcClass, statsClass, IM3Class]

product1 = Product("Product1", 5)
product2 = Product("Product2", 15)
product3 = Product("Product3", 35)
product4 = Product("Product4", 50)
product5 = Product("Product5", 100)

variableListOfProducts = [product1,product2,product3,product4, product5]

def subtractSuttonBucks(student, price):
    student.balance = student.balance - price

class ConfirmingPurchaseWindow (QWidget):
    def __init__(self,student, product, suttonKiosk, previousIndex, parent=None):
        super(ConfirmingPurchaseWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50
        self.suttonKiosk = suttonKiosk
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(previousIndex))
        self.purchasedConfirmedLayout = QGridLayout()
        purchasedConfirmedLabel = QLabel("You have just purchased: " + product.name)
        
        self.purchasedDeniedLayout = QGridLayout()
        purchasedDeniedLabel = QLabel("You do not have enough Sutton Bucks to buy: " + product.name)

        self.purchasedConfirmedLayout.addWidget(purchasedConfirmedLabel)
        self.purchasedDeniedLayout.addWidget(purchasedDeniedLabel)
        
        self.purchasedConfirmedLayout.addWidget(backButton)
        self.purchasedDeniedLayout.addWidget(backButton)
        
        self.student = student
        self.product = product
        self.previousIndex = previousIndex
        

    def setAsCurrentIndex(self):
        if (self.product.price > self.student.balance):
            self.setLayout(self.purchasedDeniedLayout)
        else:
            self.setLayout(self.purchasedConfirmedLayout)
            subtractSuttonBucks(self.student, self.product.price)
        self.suttonKiosk.setStackIndex(self.stackIndex)


class CheckOutWindow (QWidget):
    def __init__(self,student, product, suttonKiosk, previousIndex, parent=None):
        super(CheckOutWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        position = 50
        self.suttonKiosk = suttonKiosk
        mainLayout = QGridLayout()
        questionLabel = QLabel("Are you sure that you want to purchase " + product.name + " for: " + str(product.price) + " Sutton Bucks?")

        mainLayout.addWidget(questionLabel)
        yesButton = QPushButton("Yes", self)
        yesButton.move(50, position)
        confirmingPurchaseWindow = ConfirmingPurchaseWindow(student, product, suttonKiosk, previousIndex)
        yesButton.clicked.connect(confirmingPurchaseWindow.setAsCurrentIndex)
        position = position + 50
        mainLayout.addWidget(yesButton)

        noButton = QPushButton("No", self)
        noButton.move(50, position)
        noButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(previousIndex)) 
        position = position + 50
        mainLayout.addWidget(noButton)
        
        self.setLayout(mainLayout)

    
    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)

class PurchasingWindow (QWidget):
    def __init__(self,student, suttonKiosk, previousIndex, parent=None):
        super(PurchasingWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50
        self.suttonKiosk = suttonKiosk
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(previousIndex))
        mainLayout = QGridLayout()
        nameLabel = QLabel(student.name)
        currentBalanceLabel = QLabel("Current Balance: " + str(student.balance))

        mainLayout.addWidget(nameLabel)
        mainLayout.addWidget(currentBalanceLabel)
        mainLayout.addWidget(backButton)
        
        for product in variableListOfProducts:

            button = QPushButton(product.name + ":" + str(product.price), self)
            button.move(50, position)
            checkOutWindow = CheckOutWindow(student, product, suttonKiosk, self.stackIndex)
            button.clicked.connect(checkOutWindow.setAsCurrentIndex)  
            position = position + 50
            mainLayout.addWidget(button)
        
        self.setLayout(mainLayout)

    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)

class StudentsWindow(QWidget):
    def __init__(self,suttonKiosk, students, parent=None):
        super(StudentsWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50

        self.suttonKiosk = suttonKiosk
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(0))

        mainLayout = QGridLayout()
        mainLayout.addWidget(backButton)
        for student in students:
            button = QPushButton(student.name, self)
            button.move(50, position)
            purchasingWindow = PurchasingWindow(student, suttonKiosk, self.stackIndex)
            button.clicked.connect(purchasingWindow.setAsCurrentIndex)
            position = position + 50
            mainLayout.addWidget(button)
    
        self.setLayout(mainLayout)

    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)

class ClassesWidgetWindow (QWidget):
    def __init__(self, suttonKiosk, parent=None):
        super(ClassesWidgetWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)

        position = 50
        mainLayout = QGridLayout()

        for myClass in variableClassList:
            button = QPushButton(myClass.name, self)
            button.move(50, position)
            studentsWindow = StudentsWindow(suttonKiosk, myClass.students)
            button.clicked.connect(studentsWindow.setAsCurrentIndex)
            position = position + 50
            mainLayout.addWidget(button)
            
        self.setLayout(mainLayout)
        


class SuttonKiosk (QWidget):
    def __init__(self, parent=None):
        super(SuttonKiosk, self).__init__(parent)
        self.widgetStack = QStackedWidget(self)
        self.resize(320, 480)
        
        classesWidgetWindow = ClassesWidgetWindow(self)
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.widgetStack)
        self.setLayout(mainLayout)
        self.setWindowTitle("SuttonKiosk")

    def setStackIndex(self, index):
        
        self.widgetStack.setCurrentIndex(index)

if __name__ == '__main__':
    classesWindow = SuttonKiosk()
    classesWindow.show()
    sys.exit(app.exec_())
