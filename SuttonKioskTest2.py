from PyQt5.QtCore import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget)

from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget
import sys

from PyQt5.QtWidgets import QApplication
print ("Constructing an app")
app = QApplication(sys.argv)

class BackButton (QToolButton):
    def __init__(self,goBack, parent=None):
        super(BackButton, self).__init__(parent)
        self.goBack = goBack
        self.setText("Go Back")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    
    def sizeHint(self):
        size = super(BackButton, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

    def mousePressEvent(self, event):
        self.goBack()

class SchoolClass (QToolButton):
    def __init__(self, name, students, parent=None):
        super(SchoolClass, self).__init__(parent)
        self.name = name
        self.students = students
        self.setText(name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    
    def sizeHint(self):
        size = super(SchoolClass, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

    def mousePressEvent(self, event):
        self.studentListWindow = StudentListWindow()
        self.studentListWindow.start(self.students, lambda: getSKInstance().startClassListWindow())
        getSKInstance().setCentralWidget(self.studentListWindow)

class Student (QToolButton):
    def __init__(self, name, parent=None):
        super(Student, self).__init__(parent)
        self.name = name
        self.setText(name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def sizeHint(self):
        size = super(Student, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

    def mousePressEvent(self, event):
        pass

seanStudent = Student("Sean")
danaStudent = Student("Dana")
willStudent = Student("Will")
brookeStudent = Student("Brooke")

calcClass = SchoolClass("APCalc", [seanStudent, danaStudent])
statsClass = SchoolClass("APStats", [willStudent, brookeStudent])
variableClassList = [calcClass, statsClass]

class ClassListWindow(QWidget):
    def __init__(self, parent=None):
        super(ClassListWindow, self).__init__(parent)
        self.verticalPosition = 50
        
    def start(self, listOfClasses):
        mainLayout = QGridLayout()
        for myClass in listOfClasses:
            print myClass.name
            mainLayout.addWidget(myClass, 50, self.verticalPosition)
            self.verticalPosition = self.verticalPosition + 50
        self.setLayout(mainLayout)
        self.setWindowTitle("ClassListWindow")


class StudentListWindow(QWidget):
    def __init__(self, parent=None):
        super(StudentListWindow, self).__init__(parent)
        self.verticalPosition = 50

    def start(self, listOfStudents, goBack):
        mainLayout = QGridLayout()
        self.backButton = BackButton(goBack)
        mainLayout.addWidget(self.backButton, 50, self.verticalPosition)
        self.verticalPosition = self.verticalPosition + 50
        for student in listOfStudents:
            mainLayout.addWidget(student, 50, self.verticalPosition)
            self.verticalPosition = self.verticalPosition + 50
        self.setLayout(mainLayout)
        self.setWindowTitle("StudentListWindow")

class SuttonKioskMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(SuttonKioskMainWindow, self).__init__(parent)
        print ("IN Sutton Kiosk test constructor")
        self.setGeometry(0, 0, 320, 480)
        self.setFixedSize(320, 480)
        self.classList = variableClassList
        self.startClassListWindow()

    def startClassListWindow(self):
        self.classListWindow = ClassListWindow(self)
        self.setWindowTitle("ClassList")
        self.classListWindow.start(self.classList)
        self.setCentralWidget(self.classListWindow)
        self.show()

    """def startStudentListWindow(self, schoolClass):
        self.StudentListWindow = StudentListWindow(self)
        print "IN startStudentListWindow"
        for student in schoolClass.students:
            print student.name
        print
        self.StudentListWindow.addStudents(schoolClass.students)
        self.setWindowTitle("StudentList")
        self.setCentralWidget(self.StudentListWindow)
        self.StudentListWindow.backButton.clicked.connect(lambda: self.startClassListWindow(self.classList))
        self.show()

    def startClassListWindow(self, classList):
        print "Starting Class LIst WIndow"
        self.classListWindow = ClassListWindow(self)
        self.setWindowTitle("ClassList")
        self.setCentralWidget(self.classListWindow)
        self.addClasses(classList)
        self.show()

    def addClasses(self, classList):
        for myClass in classList:
            button = self.classListWindow.makeClassButton(myClass)
            #print myClass.name
            print "In addClasses"
            for student in myClass.students:
                print student.name
            print
            button.clicked.connect(lambda: self.startStudentListWindow(myClass))"""

instance = SuttonKioskMainWindow()
def getSKInstance():
    print "in get Instance"
    return instance

if __name__ == '__main__':
    suttonKioskMainWindow = getSKInstance()
    suttonKioskMainWindow.show()

    sys.exit(app.exec_())

