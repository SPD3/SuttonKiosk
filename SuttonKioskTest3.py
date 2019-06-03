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
    def __init__(self, name, balance, password=[]):
        self.name = name
        self.balance = balance
        if (len(password) > 6 ):
            self.password = []
        else:
            self.password = password

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

student1 = Student("Student1", 10,[1,2,3,4])
student2 = Student("Student2", 20,[5,6,7,8])
student3 = Student("Student3", 30)
student4 = Student("Student4", 40)
student5 = Student("Student5", 55)
student6 = Student("Student6", 70)
student7 = Student("Student7", 300)

calcClass = SchoolClass("APCalc", [student1, student2])
statsClass = SchoolClass("APStats", [student3, student4, student5])
IM3Class = SchoolClass("IM3", [student6, student7])
preCalcClass = SchoolClass("PreCalc", [])
for x in range(8,25):
    student = Student("Student" + str(x), x)
    preCalcClass.students.append(student)

variableClassList = [calcClass, statsClass, IM3Class, preCalcClass]


p1 = Product("Product1", 5)
p2 = Product("Product2", 15)
p3 = Product("Product3", 35)
p4 = Product("Product4", 50)
p5 = Product("Product5", 100)


variableListOfProducts = [p1,p2,p3,p4,p5]

class MyWidget (QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent) 
        self.setGeometry(0,0,320,480)
        self.mainLayout = QGridLayout()
        #self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

def subtractSuttonBucks(student, price):
    student.balance = student.balance - price

class ConfirmingPurchaseWindow (MyWidget):
    def __init__(self,student, product, suttonKiosk, purchasingWindowIndex, parent=None):
        super(ConfirmingPurchaseWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50
        self.suttonKiosk = suttonKiosk
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(purchasingWindowIndex))
        self.purchasedConfirmedLayout = QGridLayout()
        purchasedConfirmedLabel = QLabel("You have just purchased:\n" + product.name)
        
        self.purchasedDeniedLayout = QGridLayout()
        purchasedDeniedLabel = QLabel("You do not have enough\nSutton Bucks to buy:\n" + product.name)

        self.purchasedConfirmedLayout.addWidget(purchasedConfirmedLabel)
        self.purchasedDeniedLayout.addWidget(purchasedDeniedLabel)
        
        self.purchasedConfirmedLayout.addWidget(backButton)
        self.purchasedDeniedLayout.addWidget(backButton)
        
        self.student = student
        self.product = product
        self.purchasingWindowIndex = purchasingWindowIndex

    def setAsCurrentIndex(self):
        if (self.product.price > self.student.balance):
            self.setLayout(self.purchasedDeniedLayout)
        else:
            self.setLayout(self.purchasedConfirmedLayout)
            subtractSuttonBucks(self.student, self.product.price)
            self.suttonKiosk.widgetStack.widget(self.purchasingWindowIndex).currentBalanceLabel.setText("Current Balance: " + str(self.student.balance))

        self.suttonKiosk.setStackIndex(self.stackIndex)


class CheckOutWindow (MyWidget):
    def __init__(self,student, product, suttonKiosk, previousIndex, parent=None):
        super(CheckOutWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        position = 50
        self.suttonKiosk = suttonKiosk
        questionLabel1 = QLabel("Are you sure that you want to purchase\n" + product.name + "\nfor: " + str(product.price) + " Sutton Bucks")

        self.mainLayout.addWidget(questionLabel1)
        yesButton = QPushButton("Yes", self)
        yesButton.move(50, position)
        confirmingPurchaseWindow = ConfirmingPurchaseWindow(student, product, suttonKiosk, previousIndex)
        yesButton.clicked.connect(confirmingPurchaseWindow.setAsCurrentIndex)
        position = position + 50
        self.mainLayout.addWidget(yesButton)

        noButton = QPushButton("No", self)
        noButton.move(50, position)
        noButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(previousIndex)) 
        position = position + 50
        self.mainLayout.addWidget(noButton)
        
        self.setLayout(self.mainLayout)

    
    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)

class PurchasingWindow (MyWidget):
    def __init__(self, student, suttonKiosk, previousIndex, parent=None):
        super(PurchasingWindow, self).__init__(parent)
        
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        
        self.suttonKiosk = suttonKiosk
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50
        
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(previousIndex))
        nameLabel = QLabel(student.name)
        self.currentBalanceLabel = QLineEdit("Current Balance: " + str(student.balance))
        self.currentBalanceLabel.setReadOnly(True)

        self.mainLayout.addWidget(nameLabel)
        self.mainLayout.addWidget(self.currentBalanceLabel)
        self.mainLayout.addWidget(backButton)
        
        for product in variableListOfProducts:

            button = QPushButton(product.name + "\nPrice: " + str(product.price) + " Sutton Bucks", self)
            button.move(50, position)
            checkOutWindow = CheckOutWindow(student, product, suttonKiosk, self.stackIndex)
            button.clicked.connect(checkOutWindow.setAsCurrentIndex) 
            position = position + 50
            self.mainLayout.addWidget(button)
        
        self.setLayout(self.mainLayout)

    def setAsCurrentIndex(self):
        self.resize(self.sizeHint())
        self.suttonKiosk.setStackIndex(self.stackIndex)

class PasswordWindow(MyWidget):
    def __init__(self, student, suttonKiosk, previousIndex, parent=None):
        super(PasswordWindow, self).__init__(parent)
        self.currentPasswordGuess = []
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)
        self.position = 50
        self.promptLabel = QLineEdit("Please enter your password")
        self.promptLabelSet = True
        self.promptLabel.setReadOnly(True)
        backButton = QPushButton("BackButton", self)
        backButton.move(50, self.position)
        self.position = self.position + 50

        self.suttonKiosk = suttonKiosk
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(previousIndex))

        self.mainLayout.addWidget(self.promptLabel)
        self.mainLayout.addWidget(backButton)

        button0 = self.makeDigitButton(0)
        button1 = self.makeDigitButton(1)
        button2 = self.makeDigitButton(2)
        button3 = self.makeDigitButton(3)
        button4 = self.makeDigitButton(4)
        button5 = self.makeDigitButton(5)
        button6 = self.makeDigitButton(6)
        button7 = self.makeDigitButton(7)
        button8 = self.makeDigitButton(8)
        button9 = self.makeDigitButton(9)

        self.mainLayout.addWidget(button0)
        self.mainLayout.addWidget(button1)
        self.mainLayout.addWidget(button2)
        self.mainLayout.addWidget(button3)
        self.mainLayout.addWidget(button4)
        self.mainLayout.addWidget(button5)
        self.mainLayout.addWidget(button6)
        self.mainLayout.addWidget(button7)
        self.mainLayout.addWidget(button8)
        self.mainLayout.addWidget(button9)

        self.setLayout(self.mainLayout)
        self.student = student
        self.previousIndex = previousIndex

    def setAsCurrentIndex(self):
        if(self.student.password != []):
            self.currentPasswordGuess = []
            self.suttonKiosk.setStackIndex(self.stackIndex)
            self.promptLabel.setText("Please enter your password")
        else:
            purchasingWindow = PurchasingWindow(self.student, self.suttonKiosk, self.previousIndex)
            purchasingWindow.setAsCurrentIndex();
    
    def addDigitToCurrentPasswordGuessAndCheckGuess(self, digit):
        self.currentPasswordGuess.append(digit)
        if(not self.promptLabelSet):
            self.promptLabel.setText("Please enter your password")
        if(self.currentPasswordGuess == self.student.password):
            purchasingWindow = PurchasingWindow(self.student, self.suttonKiosk, self.previousIndex)
            purchasingWindow.setAsCurrentIndex();
        if(len(self.currentPasswordGuess) >= len(self.student.password)):
            self.currentPasswordGuess = []
            self.promptLabel.setText("Wrong password, Try again!")
            self.promptLabelSet = False

    
    def makeDigitButton(self, digit):
        button = QPushButton(str(digit), self)
        button.move(50, self.position)
        button.clicked.connect(lambda: self.addDigitToCurrentPasswordGuessAndCheckGuess(digit))
        self.position = self.position + 50
        return button


class StudentsWindow(MyWidget):
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

        self.mainLayout.addWidget(backButton)
        for student in students:
            button = QPushButton(student.name, self)
            button.move(50, position)
            passwordWindow = PasswordWindow(student, suttonKiosk, self.stackIndex)
            button.clicked.connect(passwordWindow.setAsCurrentIndex)
            position = position + 50
            self.mainLayout.addWidget(button)
    
        self.setLayout(self.mainLayout)

    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)


class ClassesWidgetWindow (MyWidget):
    def __init__(self, suttonKiosk, parent=None):
        super(ClassesWidgetWindow, self).__init__(parent)
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)

        position = 50

        for myClass in variableClassList:
            button = QPushButton(myClass.name, self)
            button.move(50, position)
            studentsWindow = StudentsWindow(suttonKiosk, myClass.students)
            button.clicked.connect(studentsWindow.setAsCurrentIndex)
            position = position + 50
            self.mainLayout.addWidget(button)
            
        self.setLayout(self.mainLayout)
        


class SuttonKiosk (MyWidget):
    def __init__(self, parent=None):
        super(SuttonKiosk, self).__init__(parent)
        self.widgetStack = QStackedWidget(self)
        self.resize(320, 480)
        
        classesWidgetWindow = ClassesWidgetWindow(self)
        
        self.mainLayout.addWidget(self.widgetStack)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("SuttonKiosk")

    def setStackIndex(self, index):
        self.widgetStack.setCurrentIndex(index)
        

if __name__ == '__main__':
    classesWindow = SuttonKiosk()
    classesWindow.show()
    sys.exit(app.exec_())