from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit
from PyQt6.QtGui import QAction, QKeySequence

class MainWindow(QMainWindow):
        def __init__(self):
                super().__init__()
                self.filename, self.copy_name = '', ''
                self.setWindowTitle("Notepad")

                self.edit = QTextEdit()
                self.setCentralWidget(self.edit)

                open_action = QAction('Open', self)
                open_action.setShortcut(QKeySequence('Ctrl+o'))
                open_action.triggered.connect(self.open_file)

                save_action = QAction('Save', self)
                save_action.setShortcut(QKeySequence('Ctrl+s'))
                save_action.triggered.connect(self.save_file)

                save_as_action = QAction('Save as', self)
                save_as_action.setShortcut(QKeySequence('Ctrl+Shift+s'))
                save_as_action.triggered.connect(lambda: self.save_file(para='save_as'))

                exit_action = QAction('Exit', self)
                exit_action.setShortcut(QKeySequence('Ctrl+q'))
                exit_action.triggered.connect(QCoreApplication.exit)

                self.cut_action = QAction('Cut', self)
                self.cut_action.setShortcut(QKeySequence('Ctrl+x'))
                self.cut_action.triggered.connect(self.edit.cut)

                self.copy_action = QAction('Copy', self)
                self.copy_action.setShortcut(QKeySequence('Ctrl+c'))
                self.copy_action.triggered.connect(self.edit.copy)

                paste_action = QAction('Paste', self)
                paste_action.setShortcut(QKeySequence('Ctrl+v'))
                paste_action.triggered.connect(self.edit.paste)

                select_all_action = QAction('Select all', self)
                select_all_action.setShortcut(QKeySequence('Ctrl+a'))
                select_all_action.triggered.connect(self.edit.selectAll)

                menu = self.menuBar()

                file_menu = menu.addMenu('File')
                file_menu.addAction(open_action)
                file_menu.addAction(save_action)
                file_menu.addAction(save_as_action)
                file_menu.addSeparator()
                file_menu.addAction(exit_action)
                
                edit_menu = menu.addMenu('Edit')
                edit_menu.triggered.connect(lambda: self.decide())
                edit_menu.addAction(self.cut_action)
                edit_menu.addAction(self.copy_action)
                edit_menu.addAction(paste_action)
                edit_menu.addSeparator()
                edit_menu.addAction(select_all_action)


        def open_file(self):
                self.filename, adress = QFileDialog.getOpenFileName(self, filter="Text files (*.txt)")
                self.copy_name = self.filename
                if self.filename:
                        with open(self.filename, 'r') as f:
                                self.edit.setText(f.read())

        def save_file(self, para):
                if self.filename=='' or para=='save_as':
                        self.filename, adress = QFileDialog.getSaveFileName(self, filter="Text files (*.txt)")
                if self.filename:
                        with open(self.filename, 'w') as f:
                                f.write(self.edit.toPlainText())
                else:
                        self.filename = self.copy_name

        def action_state(self, d):
                self.cut_action.setDisabled(d)
                self.copy_action.setDisabled(d)

        def decide(self):
                if self.edit.toPlainText=='':
                        self.action_state(d=True)
                else:
                        self.action_state(d=False)

app = QApplication([])

window = MainWindow()
window.show()
app.exec()