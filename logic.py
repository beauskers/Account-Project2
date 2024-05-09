from PyQt6.QtWidgets import *
from gui import *
import csv
import re


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__balance = 0
        self.enterBtn.clicked.connect(lambda: self.enter())
        self.exitBtn.clicked.connect(lambda: self.exit())
        self.loginBtn.clicked.connect(lambda: self.login())
        self.toCreateBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.createBtn.clicked.connect(lambda: self.create())

        self.passwordEnter.setEchoMode(QLineEdit.EchoMode.Password)
        self.createPassEnter.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmEnter.setEchoMode(QLineEdit.EchoMode.Password)

        self.email = ''
        self.password = ''

    def login(self) -> None:
        """
        This function logs you into the program
        """
        self.email = self.usernameEnter.text()
        self.password = self.passwordEnter.text()
        with open('accounts.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if self.email == line[0] and self.password == line[1]:
                    with open('accountBalance.csv', 'r') as csvfile:
                        csv_reader = csv.reader(csvfile)
                        for line in csv_reader:
                            if line[0] == self.email:
                                self.__balance = float(line[1])
                                self.balLabel.setText(f'Your account balance is ${self.__balance:.2f}')
                    self.usernameEnter.clear()
                    self.passwordEnter.clear()
                    self.stackedWidget.setCurrentIndex(2)
                else:
                    self.loginStatus.setText('Incorrect email or password')
                    self.passwordEnter.clear()

    def enter(self) -> None:
        """
        This function submits the action you want to take on your account
        """
        try:
            amount = float(self.amountEdit.text())

            if self.withdrawRadio.isChecked():
                if amount <= 0:
                    self.amountStatus.setText('You can\'t withdraw a negative amount')
                elif amount <= self.__balance:
                    self.__balance -= amount
                    self.clear()
                    self.amountStatus.setText('Success!')
                    self.balLabel.setText(f'Your account balance is ${self.__balance:.2f}')
                elif amount >= self.__balance:
                    self.amountStatus.setText('You can\'t withdraw more than your balance')
            elif self.depositRadio.isChecked():
                if amount <= 0:
                    self.amountStatus.setText('You can\'t deposit a negative amount')
                else:
                    self.__balance += amount
                    self.clear()
                    self.amountStatus.setText('Success!')
                    self.balLabel.setText(f'Your account balance is ${self.__balance:.2f}')
            else:
                self.amountStatus.setText('Please select an option')
        except ValueError:
            self.amountStatus.setText('Invalid amount')

    def exit(self) -> None:
        """
        This function exits the main program and brings you back to the login page
        """
        with open('accountBalance.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            info = [self.email, self.__balance]
            csv_writer.writerow(info)
        self.stackedWidget.setCurrentIndex(0)
        self.clear()
        self.__balance = 0
        self.balLabel.setText(f'Your account balance is ${self.__balance:.2f}')
        self.amountStatus.setText('')

    def create(self) -> None:
        """
        this function creates an account
        """
        email_check = self.check_email()
        if email_check:
            self.password = self.createPassEnter.text()
            password_check = self.confirmEnter.text()
            if password_check == self.password:
                with open('accounts.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    account_info = [self.email, self.password]
                    csv_writer.writerow(account_info)
                self.createUserEnter.clear()
                self.createPassEnter.clear()
                self.confirmEnter.clear()
                self.createStatus.setText('')
                self.stackedWidget.setCurrentIndex(2)
            else:
                self.createStatus.setText('Passwords do not match')
                self.confirmEnter.clear()
        else:
            self.createStatus.setText('Email is invalid')


    def check_email(self) -> bool:
        """
        This function checks to see if email is valid 
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        self.email = self.createUserEnter.text()
        if re.fullmatch(regex, self.email):
            return True
        else:
            return False
    def clear(self) -> None:
        """
        This function is used to clear the radio buttons 
        """
        self.amountEdit.clear()
        if self.withdrawRadio.isChecked():
            self.withdrawRadio.setAutoExclusive(False)
            self.withdrawRadio.setChecked(False)
            self.withdrawRadio.setAutoExclusive(True)
        else:
            self.depositRadio.setAutoExclusive(False)
            self.depositRadio.setChecked(False)
            self.depositRadio.setAutoExclusive(True)
        self.loginStatus.setText('')