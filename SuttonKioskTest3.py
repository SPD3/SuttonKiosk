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
variableClassList = [calcClass, statsClass]

class StudentsWindow(QWidget):
    def __init__(self,classesMainWindowWindow, students, stackIndex, parent=None):
        self.stackIndex = stackIndex
        super(StudentsWindow, self).__init__(parent)
        position = 50
        backButton = QPushButton("BackButton", self)
        backButton.move(50, position)
        position = position + 50
        backButton.clicked.connect(lambda: classesMainWindowWindow.setStudentWindow(0))
        for studentName in students:
            button = QPushButton(studentName, self)
            button.move(50, position)
            position = position + 50

class ClassesWidgetWindow (QWidget):
    def __init__(self, classesMainWindowWindow, stackIndex, parent=None):
        super(ClassesWidgetWindow, self).__init__(parent)
        self.stackIndex = stackIndex
        position = 50
        mainLayout = QGridLayout()
        calcButton = QPushButton(variableClassList[0].name, self)
        calcButton.move(50, position)
        calcButton.clicked.connect(lambda: classesMainWindowWindow.setStudentWindow(1))
        position = position + 50
        mainLayout.addWidget(calcButton)
        
        statsButton = QPushButton(variableClassList[1].name, self)
        statsButton.move(50, position)
        statsButton.clicked.connect(lambda: classesMainWindowWindow.setStudentWindow(2))
        mainLayout.addWidget(statsButton)
        position = position + 50
        self.setLayout(mainLayout)
        


class SuttonKiosk (QWidget):
    def __init__(self, parent=None):
        super(SuttonKiosk, self).__init__(parent)
        self.stackOfStudentWindowWidgets = QStackedWidget(self)
        self.resize(300, 300)
        
        classesWidgetWindow = ClassesWidgetWindow(self, 0)
        self.stackOfStudentWindowWidgets.addWidget(classesWidgetWindow)
        calcStudentsWindow = StudentsWindow(self, variableClassList[0].students, 1)
        self.stackOfStudentWindowWidgets.addWidget(calcStudentsWindow)
        statsStudentsWindow = StudentsWindow(self, variableClassList[1].students,2)
        self.stackOfStudentWindowWidgets.addWidget(statsStudentsWindow)
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.stackOfStudentWindowWidgets)
        self.setLayout(mainLayout)
        self.setWindowTitle("ClassListWindow")
        

    def setStudentWindow(self, index):
        self.stackOfStudentWindowWidgets.setCurrentIndex(index)


if __name__ == '__main__':
    classesWindow = SuttonKiosk()
    classesWindow.show()
    sys.exit(app.exec_())
