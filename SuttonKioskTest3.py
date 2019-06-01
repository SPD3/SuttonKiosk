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

calcClass = SchoolClass("APCalc", ["seanStudent", "danaStudent"])
statsClass = SchoolClass("APStats", ["willStudent", "brookeStudent"])
IM3Class = SchoolClass("IM3", ["Bob", "Joe"])

variableClassList = [calcClass, statsClass, IM3Class]

class StudentsWindow(QWidget):
    def __init__(self,suttonKiosk, students, stackIndex, parent=None):
        self.stackIndex = stackIndex
        super(StudentsWindow, self).__init__(parent)
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50
        self.suttonKiosk = suttonKiosk
        backButton.clicked.connect(lambda: self.suttonKiosk.setStackIndex(0))
        for studentName in students:
            button = QPushButton(studentName, self)
            button.move(50, position)
            position = position + 50

    def setAsCurrentIndex(self):
        self.suttonKiosk.setStackIndex(self.stackIndex)

class ClassesWidgetWindow (QWidget):
    def __init__(self, suttonKiosk, parent=None):
        super(ClassesWidgetWindow, self).__init__(parent)
        print suttonKiosk.stackOfStudentWindowWidgets.count()
        self.stackIndex = suttonKiosk.stackOfStudentWindowWidgets.count()
        suttonKiosk.stackOfStudentWindowWidgets.addWidget(self)

        position = 50
        mainLayout = QGridLayout()

        print "Entrering For Loop!"
        for myClass in variableClassList:
            button = QPushButton(myClass.name, self)
            button.move(50, position)
            currentStackCount = suttonKiosk.stackOfStudentWindowWidgets.count()
            print ("The class: " , myClass.name , " has the stack index: " , currentStackCount)
            studentsWindow = StudentsWindow(suttonKiosk, myClass.students, currentStackCount)
            button.clicked.connect(studentsWindow.setAsCurrentIndex)
            position = position + 50
            mainLayout.addWidget(button)
            
            suttonKiosk.stackOfStudentWindowWidgets.addWidget(studentsWindow)

        self.setLayout(mainLayout)
        


class SuttonKiosk (QWidget):
    def __init__(self, parent=None):
        super(SuttonKiosk, self).__init__(parent)
        self.stackOfStudentWindowWidgets = QStackedWidget(self)
        self.resize(300, 300)
        
        classesWidgetWindow = ClassesWidgetWindow(self)
        
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.stackOfStudentWindowWidgets)
        self.setLayout(mainLayout)
        self.setWindowTitle("ClassListWindow")
        

    def setStackIndex(self, index):
        print ("setting the stack to index: " , index)
        self.stackOfStudentWindowWidgets.setCurrentIndex(index)

if __name__ == '__main__':
    classesWindow = SuttonKiosk()
    classesWindow.show()
    sys.exit(app.exec_())
