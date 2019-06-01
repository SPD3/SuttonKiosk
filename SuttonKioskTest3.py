from PyQt5.QtCore import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget, QStackedWidget)

from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget
import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

class SchoolClass (QWidget):
    def __init__(self, name, students, parent=None):
        super(SchoolClass, self).__init__(parent)
        self.name = name
        self.students = students

class Student (QWidget):
    def __init__(self, name, balance, parent=None):
        super(Student, self).__init__(parent)
        self.name = name
        self.balance = balance

class Product (QWidget):
    def __init__(self, name, price, parent=None):
        super(Product, self).__init__(parent)
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

variableListOfProducts = [product1,product2,product3,product4]

class PurchasingWindow (QWidget):
    def __init__(self,student, suttonKiosk, stackIndex, previousIndex, parent=None):
        super(PurchasingWindow, self).__init__(parent)
        self.stackIndex = stackIndex
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
            position = position + 50
            mainLayout.addWidget(button)
        
        self.setLayout(mainLayout)

    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)

class StudentsWindow(QWidget):
    def __init__(self,suttonKiosk, students, stackIndex, parent=None):
        super(StudentsWindow, self).__init__(parent)
        self.stackIndex = stackIndex
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
            currentStackCount = suttonKiosk.widgetStack.count()
            purchasingWindow = PurchasingWindow(student, suttonKiosk, currentStackCount, self.stackIndex)
            button.clicked.connect(purchasingWindow.setAsCurrentIndex)
            position = position + 50
            mainLayout.addWidget(button)
    
        self.setLayout(mainLayout)

    def setAsCurrentIndex(self):
        print "Calling setAsCurrentIndex for the studentWindow!" 
        self.suttonKiosk.setStackIndex(self.stackIndex)

class ClassesWidgetWindow (QWidget):
    def __init__(self, suttonKiosk, parent=None):
        super(ClassesWidgetWindow, self).__init__(parent)
        print suttonKiosk.widgetStack.count()
        self.stackIndex = suttonKiosk.widgetStack.count()
        suttonKiosk.widgetStack.addWidget(self)

        position = 50
        mainLayout = QGridLayout()

        print "Entrering For Loop!"
        for myClass in variableClassList:
            button = QPushButton(myClass.name, self)
            button.move(50, position)
            currentStackCount = suttonKiosk.widgetStack.count()
            studentsWindow = StudentsWindow(suttonKiosk, myClass.students, currentStackCount)
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
        print ("setting the stack to index: " , index)
        self.widgetStack.setCurrentIndex(index)

if __name__ == '__main__':
    classesWindow = SuttonKiosk()
    classesWindow.show()
    sys.exit(app.exec_())
