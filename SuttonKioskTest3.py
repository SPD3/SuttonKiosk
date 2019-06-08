from __future__ import print_function
from PyQt5.QtCore import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget, QStackedWidget)

from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget
import sys

from PyQt5.QtWidgets import QApplication

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = QApplication(sys.argv)

class SchoolClass:
    def __init__(self, name, students):
        self.name = name
        self.students = students

class Student:
    def __init__(self, name, balance,spreadSheetId,  password=[]):
        self.name = name
        self.balance = balance
        if (len(password) > 6 or (len(password) == 1 and password[0] == 0)):
            self.password = []
        else:
            self.password = password
        self.spreadSheetId = spreadSheetId

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

student1 = Student("Student1", 10,[1,2,3,4])

variableClassList = []

variableListOfProducts = []

class MyWidget (QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent) 
        self.setGeometry(0,0,320,480)
        self.mainLayout = QGridLayout()
        #self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

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
        self.purchasedConfirmedLabel = QLineEdit("You have just purchased:\n" + product.name)

        self.purchasedConfirmedLayout.addWidget(self.purchasedConfirmedLabel)
        
        
        self.purchasedConfirmedLayout.addWidget(backButton)
        self.setLayout(self.purchasedConfirmedLayout)
        self.student = student
        self.product = product
        self.purchasingWindowIndex = purchasingWindowIndex

    def setAsCurrentIndex(self):
        print ("Confirming purchase window: " + str(self.student.balance))
        if (self.product.price > self.student.balance):
            
            self.purchasedConfirmedLabel.setText("You do not have enough money to buy:\n" + self.product.name)
        else:
            self.purchasedConfirmedLabel.setText("You have just purchased:\n" + self.product.name)
            global googleSheetsStuff
            googleSheetsStuff.subtractSuttonBucks(self.student, self.product.price)
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
    


class GoogleSheetsStuff:
    
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        self.SUTTON_KIOSK_SPREADSHEET_ID = '1wSak9lNEvY8_GDOwfzmTdErEKJxNK3H2kuhXDh_633o'
        self.STUDENT_DATA_RANGE = 'A2:D'
        self.PRODUCT_DATA_RANGE = 'F2:G'
        self.currentClass = None
        self.setGSData()

    def setGSData(self):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token, protocol=2)

        service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        self.sheet = service.spreadsheets()
        studentResults = self.sheet.values().get(spreadsheetId=self.SUTTON_KIOSK_SPREADSHEET_ID,
                                    range=self.STUDENT_DATA_RANGE).execute()
        studentValues = studentResults.get('values', [])
        
        productResults = self.sheet.values().get(spreadsheetId=self.SUTTON_KIOSK_SPREADSHEET_ID,
                                    range=self.PRODUCT_DATA_RANGE).execute()
        productValues = productResults.get('values', [])
        counter = 2
        for row in studentValues:
            studentGoogleSheetID = 'B' + str(counter) + ':C'
            studentPassCodeString = str(row[3])
            studentPassCodeList = []
            for char in studentPassCodeString:
                studentPassCodeList.append(int(char))


            student = Student(row[1], int(row[2]), studentGoogleSheetID, studentPassCodeList)
            counter = counter + 1
            if(self.currentClass is not None and row[0] == self.currentClass.name):
                self.currentClass.students.append(student)
            else:
                schoolClass = SchoolClass(row[0], [])
                variableClassList.append(schoolClass)
                self.currentClass = schoolClass
                self.currentClass.students.append(student)

        for row in productValues:
            product = Product(row[0], int(row[1]))
            variableListOfProducts.append(product)


    def subtractSuttonBucks(self, student, price):
        newbalance = student.balance - price
        print ("Subtracting sutton bucks student balance" + str(student.balance))
        values = [
                [
                    student.name, newbalance, 
                ],
                # Additional rows ...
            ]
        body = {
            'values': values
        }
        range_name = student.spreadSheetId

        result = self.sheet.values().update(
            spreadsheetId=self.SUTTON_KIOSK_SPREADSHEET_ID, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        
        service = build('sheets', 'v4', credentials=self.creds)
        #self.sheet = service.spreadsheets()
        studentResults = self.sheet.values().get(spreadsheetId=self.SUTTON_KIOSK_SPREADSHEET_ID,
                                    range=student.spreadSheetId).execute()
        studentValues = studentResults.get('values', [])
        spreadSheetBalance = int(studentValues[0][1])
        #print ("Here is what the spreadsheet reads: " + str(spreadSheetBalance))
       
        student.balance = spreadSheetBalance

if __name__ == '__main__':
    googleSheetsStuff = GoogleSheetsStuff()
    classesWindow = SuttonKiosk()
    classesWindow.show()
    sys.exit(app.exec_())