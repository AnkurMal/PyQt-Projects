from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QMainWindow, QMessageBox
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QIcon

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.choice = 0
        self.counter = 0
        self.setWindowTitle('Tic-Tac-Toe')
        self.setWindowIcon(QIcon('tic_tac_toe.png'))
        self.setFixedSize(270, 270)
        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.button3 = QPushButton()
        self.button4 = QPushButton()
        self.button5 = QPushButton()
        self.button6 = QPushButton()
        self.button7 = QPushButton()
        self.button8 = QPushButton()
        self.button9 = QPushButton()

        self.button1.pressed.connect(lambda: self.x_or_y(button=self.button1))
        self.button2.pressed.connect(lambda: self.x_or_y(button=self.button2))
        self.button3.pressed.connect(lambda: self.x_or_y(button=self.button3))
        self.button4.pressed.connect(lambda: self.x_or_y(button=self.button4))
        self.button5.pressed.connect(lambda: self.x_or_y(button=self.button5))
        self.button6.pressed.connect(lambda: self.x_or_y(button=self.button6))
        self.button7.pressed.connect(lambda: self.x_or_y(button=self.button7))
        self.button8.pressed.connect(lambda: self.x_or_y(button=self.button8))
        self.button9.pressed.connect(lambda: self.x_or_y(button=self.button9))
        
        layout = QGridLayout()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 0, 2)
        layout.addWidget(self.button4, 1, 0)
        layout.addWidget(self.button5, 1, 1)
        layout.addWidget(self.button6, 1, 2)
        layout.addWidget(self.button7, 2, 0)
        layout.addWidget(self.button8, 2, 1)
        layout.addWidget(self.button9, 2, 2)

        self.button_list = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, 
                       self.button7, self.button8, self.button9]
        for i in self.button_list:
            i.setFixedSize(80, 80)
            i.setStyleSheet('font-size: 40px; font-weight: bold')

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def x_or_y(self, button):
            self.counter += 1
            button.setDisabled(True)
            if self.choice==0:
                button.setText('X')
                self.choice = 1
                self.check_match('X')
            else:
                button.setText('O')
                self.choice = 0
                self.check_match('O')

    def check_match(self, state):
            matched = False
            info = 0
            if (self.button1.text()==self.button2.text()==self.button3.text()==state or
                self.button4.text()==self.button5.text()==self.button6.text()==state or
                self.button7.text()==self.button8.text()==self.button9.text()==state or
                self.button1.text()==self.button4.text()==self.button7.text()==state or
                self.button2.text()==self.button5.text()==self.button8.text()==state or
                self.button3.text()==self.button6.text()==self.button9.text()==state or
                self.button1.text()==self.button5.text()==self.button9.text()==state or
                self.button3.text()==self.button5.text()==self.button7.text()==state
                ):
                    info = QMessageBox.information(self, 'Win', f"Player '{state}' wins! Do you want to play again?", buttons=\
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    matched = True
            if matched==False and self.counter==9:
                    info = QMessageBox.information(self, 'Draw', "It's a draw! Do you want to play again?", buttons=\
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) 
            if info==QMessageBox.StandardButton.No:
                QCoreApplication.exit()
            elif info==QMessageBox.StandardButton.Yes:
                    for i in self.button_list:
                        i.setEnabled(True)
                        i.setText('')
                    self.choice = 0
                    self.counter = 0
    
app = QApplication([])
window = Window()
window.show()
app.exec()