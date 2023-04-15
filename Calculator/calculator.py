from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QWidget, QGridLayout
from PyQt6.QtGui import QIcon
import darkdetect as QDetectTheme

class MainWindow(QMainWindow):
        def __init__(self):
                super().__init__()
                self.num = ''
                self.op_list = []
                self.num1 = self.num2 = 0.0
                self.err_list = ['', 'Cannot divide by zero']
                self.check = 0

                self.setWindowTitle("Calculator")
                self.setFixedSize(320, 280)
                self.setWindowIcon(QIcon('calculator.ico'))

                self.entry = QLineEdit()
                self.entry.setFixedHeight(30)
                self.entry.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                self.entry.setReadOnly(True)

                #declaring buttons
                self.button_1 = QPushButton('1')
                self.button_2 = QPushButton('2')
                self.button_3 = QPushButton('3')
                self.button_4 = QPushButton('4')
                self.button_5 = QPushButton('5')
                self.button_6 = QPushButton('6')
                self.button_7 = QPushButton('7')
                self.button_8 = QPushButton('8')
                self.button_9 = QPushButton('9')
                self.button_C = QPushButton('C')
                self.button_0 = QPushButton('0')
                self.button_point = QPushButton('.')
                self.button_point.setStyleSheet('font: bold')
                self.button_pm = QPushButton('+/-')
                self.button_pm.setStyleSheet('font: bold')
                self.button_remove = QPushButton('⌫')
                self.button_remove.setStyleSheet('font: bold')
                self.button_div = QPushButton('÷')
                self.button_div.setStyleSheet('font: bold')
                self.button_multiply = QPushButton('×')
                self.button_multiply.setStyleSheet('font: bold')
                self.button_minus = QPushButton('–')
                self.button_minus.setStyleSheet('font: bold')
                self.button_plus = QPushButton('+')
                self.button_plus.setStyleSheet('font: bold')
                self.button_percentage = QPushButton('%')
                self.button_percentage.setStyleSheet('font: bold')
                self.button_equals = QPushButton('=')
                self.button_equals.setStyleSheet('font: bold')

                #setting button size
                self.button_1.setFixedSize(75,45)
                self.button_2.setFixedSize(75,45)
                self.button_3.setFixedSize(75,45)
                self.button_4.setFixedSize(75,45)
                self.button_5.setFixedSize(75,45)
                self.button_6.setFixedSize(75,45)
                self.button_7.setFixedSize(75,45)
                self.button_8.setFixedSize(75,45)
                self.button_9.setFixedSize(75,45)
                self.button_C.setFixedSize(75,45)
                self.button_0.setFixedSize(75,45)
                self.button_point.setFixedSize(75,45)
                self.button_pm.setFixedSize(75,45)
                self.button_remove.setFixedSize(75,45)
                self.button_div.setFixedSize(75,45)
                self.button_multiply.setFixedSize(75,45)
                self.button_minus.setFixedSize(75,45)
                self.button_plus.setFixedSize(75,45)
                self.button_percentage.setFixedSize(75,45)
                self.button_equals.setFixedSize(75,45)

                #adding widgets to layout
                layout = QGridLayout()
                layout.addWidget(self.entry, 0, 0, 1, 4, Qt.AlignmentFlag.AlignTop)
                layout.addWidget(self.button_pm, 5, 0)
                layout.addWidget(self.button_percentage, 5, 1)
                layout.addWidget(self.button_equals, 5, 2)
                layout.addWidget(self.button_plus, 5, 3)
                layout.addWidget(self.button_C, 4, 0)
                layout.addWidget(self.button_0, 4, 1)
                layout.addWidget(self.button_point, 4, 2)
                layout.addWidget(self.button_minus, 4, 3)
                layout.addWidget(self.button_1, 3, 0)
                layout.addWidget(self.button_2, 3, 1)
                layout.addWidget(self.button_3, 3, 2)
                layout.addWidget(self.button_multiply, 3, 3)
                layout.addWidget(self.button_4, 2, 0)
                layout.addWidget(self.button_5, 2, 1)
                layout.addWidget(self.button_6, 2, 2)
                layout.addWidget(self.button_div, 2, 3)
                layout.addWidget(self.button_7, 1, 0)
                layout.addWidget(self.button_8, 1, 1)
                layout.addWidget(self.button_9, 1, 2)
                layout.addWidget(self.button_remove, 1, 3)

                #what the button does!!
                self.button_0.clicked.connect(lambda: self.put_number(n = '0'))
                self.button_1.clicked.connect(lambda: self.put_number(n = '1'))
                self.button_2.clicked.connect(lambda: self.put_number(n = '2'))
                self.button_3.clicked.connect(lambda: self.put_number(n = '3'))
                self.button_4.clicked.connect(lambda: self.put_number(n = '4'))
                self.button_5.clicked.connect(lambda: self.put_number(n = '5'))
                self.button_6.clicked.connect(lambda: self.put_number(n = '6'))
                self.button_7.clicked.connect(lambda: self.put_number(n = '7'))
                self.button_8.clicked.connect(lambda: self.put_number(n = '8'))
                self.button_9.clicked.connect(lambda: self.put_number(n = '9'))
                self.button_point.clicked.connect(lambda: self.put_number(n = '.'))
                self.button_pm.clicked.connect(self.plus_minus)
                self.button_remove.clicked.connect(self.remove)
                self.button_div.clicked.connect(lambda: self.operators(op = '/'))
                self.button_multiply.clicked.connect(lambda: self.operators(op = 'x'))
                self.button_minus.clicked.connect(lambda: self.operators(op = '-'))
                self.button_plus.clicked.connect(lambda: self.operators(op = '+'))
                self.button_percentage.clicked.connect(self.percentage)
                self.button_equals.clicked.connect(self.equals)
                self.button_C.clicked.connect(self.clear)

                #adding layout to widget
                widget = QWidget()
                widget.setLayout(layout)
                self.setCentralWidget(widget)

        #When keys in keyboard or virtual keyboard is pressed
        def event_handle(self, key):
                if key==Qt.Key.Key_0:
                        self.button_0.animateClick()
                elif key==Qt.Key.Key_1:
                        self.button_1.animateClick()
                elif key==Qt.Key.Key_2:
                        self.button_2.animateClick()
                elif key==Qt.Key.Key_3:
                        self.button_3.animateClick()
                elif key==Qt.Key.Key_4:
                        self.button_4.animateClick()
                elif key==Qt.Key.Key_5:
                        self.button_5.animateClick()
                elif key==Qt.Key.Key_6:
                        self.button_6.animateClick()
                elif key==Qt.Key.Key_7:
                        self.button_7.animateClick()
                elif key==Qt.Key.Key_8:
                        self.button_8.animateClick()
                elif key==Qt.Key.Key_9:
                        self.button_9.animateClick()
                elif key==Qt.Key.Key_Period:
                        self.button_point.animateClick()
                elif key==Qt.Key.Key_Backspace and self.button_remove.isEnabled()==True:
                        self.button_remove.animateClick()
                elif key==Qt.Key.Key_Slash and self.button_div.isEnabled()==True:
                        self.button_div.animateClick()
                elif key==Qt.Key.Key_Asterisk and self.button_multiply.isEnabled()==True:
                        self.button_multiply.animateClick()
                elif key==45 and self.button_minus.isEnabled()==True:      #hex value for the minus symbol '-'
                        self.button_minus.animateClick()
                elif key==Qt.Key.Key_Plus and self.button_plus.isEnabled()==True:
                        self.button_plus.animateClick()
                elif key==Qt.Key.Key_Percent:
                        self.button_percentage.animateClick()
                elif key==Qt.Key.Key_Equal or key==Qt.Key.Key_Enter or key==Qt.Key.Key_Return:
                        self.button_equals.animateClick()
                elif key==Qt.Key.Key_Delete:
                        self.button_C.animateClick()

        def keyPressEvent(self, event):
                self.event_handle(key=event.key())

        def mousePressEvent(self, event):
                try:
                    self.event_handle(key=event.key())
                except AttributeError:
                        pass
        
        #Other functions
        def button_state(self, x):
                self.button_remove.setDisabled(x)
                self.button_div.setDisabled(x)
                self.button_multiply.setDisabled(x)
                self.button_minus.setDisabled(x)
                self.button_plus.setDisabled(x)

        def put_number(self, n):
                if self.button_div.isEnabled()==False:
                        self.button_state(x=False)
                self.num = self.entry.text()
                if self.num=='Cannot divide by zero' or self.check==1:
                        self.clear()
                        self.check = 0
                if self.num=='0' and n=='0':
                        return
                elif n=='.' and self.num.count('.')==1:
                        return
                elif n=='.' and self.num=='':
                        self.num = '0.'
                else:
                        self.num += n
                self.num2 = float(self.num)
                self.entry.setText(self.num)

        def remove(self):
                text = self.entry.text()
                if text in self.err_list:
                        return
                if 'e' in text:
                        return
                self.entry.setText(text[:-1])

        def plus_minus(self):
                x = self.entry.text()
                list = ['', 'Cannot divide by zero', '0', '0.0']
                if x in list:
                        return
                x = float(x)
                self.entry.setText(str(-x))

        def percentage(self):
                n = self.entry.text()
                self.op_list = []
                if n in self.err_list:
                        return
                n = float(n)
                self.entry.setText(str(n/100.0))

        def clear(self):
                if self.button_div.isEnabled()==False:
                        self.button_state(x=False)
                self.num = ''
                self.op_list = []
                self.entry.clear()

        def operators(self, op):
                self.check = 0
                self.num = ''
                self.op_list.append(op)
                if self.entry.text()=='':
                        return
                self.num1 = float(self.entry.text())
                self.entry.clear()

        def equals(self):
                self.check = 1
                result = 0.0
                if self.op_list==[]:
                        self.num = ''
                        return
                if self.entry.text()=='':
                        return
                operator = self.op_list[-1]
                if operator=='/':
                        if self.num2==0:
                                self.entry.setText("Cannot divide by zero")
                                self.button_state(x=True)
                                self.num = ''
                                return
                        result = self.num1 / self.num2
                elif operator=='x':
                        result = self.num1 * self.num2
                elif operator=='-':
                        result = self.num1 - self.num2
                elif operator=='+':
                        result = self.num1 + self.num2
                self.num1 = result
                self.entry.setText(str(result))

app = QApplication([])
if QDetectTheme.theme()=='Dark':
        app.setStyle('Fusion')          #Apply the theme of the OS in your widget       
window = MainWindow()
window.show()
app.exec()