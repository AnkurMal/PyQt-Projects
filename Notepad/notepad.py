from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QMessageBox
from PyQt6.QtGui import QAction, QKeySequence, QCloseEvent, QIcon
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter

class MainWindow(QMainWindow):
        def __init__(self):
                super().__init__()
                self.filename = self.copy_name = self.f_name = self.data = ''

                self.setWindowTitle("Notepad")
                self.setStyleSheet('font-size: 14px')
                self.setWindowIcon(QIcon("Notepad.png"))
                self.setMinimumSize(1000, 550)

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
                exit_action.triggered.connect(self.closeEvent)

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

                print_action = QAction('Print', self)
                print_action.setShortcut(QKeySequence('Ctrl+p'))
                print_action.triggered.connect(self.print_out)

                menu = self.menuBar()

                file_menu = menu.addMenu('File')
                file_menu.addAction(open_action)
                file_menu.addAction(save_action)
                file_menu.addAction(save_as_action)
                file_menu.addAction(print_action)
                file_menu.addSeparator()
                file_menu.addAction(exit_action)
                
                edit_menu = menu.addMenu('Edit')
                edit_menu.addAction(self.cut_action)
                edit_menu.addAction(self.copy_action)
                edit_menu.addAction(paste_action)
                edit_menu.addSeparator()
                edit_menu.addAction(select_all_action)

        def open_file(self):
                self.filename, adress = QFileDialog.getOpenFileName(self)
                self.f_name = self.filename.split('/')[-1]
                if self.filename:
                        try:
                                with open(self.filename, 'r') as f:
                                        self.data = f.read()
                                self.edit.setText(self.data)
                                self.f_name = self.filename.split('/')[-1]
                                self.setWindowTitle(f'Notepad ({self.f_name})')
                                self.copy_name = self.filename
                        except UnicodeDecodeError:
                                file_extension = self.f_name.split('.')[-1].upper()
                                QMessageBox.warning(self, 'Invalid file format', f'Cannot open a {file_extension} file.')
                                self.f_name = self.filename = ''
                                return

        def save_file(self, para=''):
                if self.filename=='' or para=='save_as':
                        self.filename, adress = QFileDialog.getSaveFileName(self)
                if self.filename:
                        self.f_name = self.filename.split('/')[-1]
                        self.setWindowTitle(f'Notepad ({self.f_name})')
                        self.data = self.edit.toPlainText()
                        with open(self.filename, 'w') as f:
                                f.write(self.data)
                else:
                        self.filename = self.copy_name

        def print_out(self):
                printer = QPrinter()
                dialog = QPrintDialog(printer, self)
                dialog.accepted.connect(lambda: self.edit.print(printer))
                dialog.exec()

        def closeEvent(self, event: QCloseEvent):
                if self.data!=self.edit.toPlainText() and self.filename:
                        button = QMessageBox.question(self, 'Save changes', f'Do you want to save changes to {self.f_name}?', 
                                                     buttons= QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
                elif self.filename=='' and self.edit.toPlainText():
                        button = QMessageBox.question(self, 'Save changes', 'Do you want to save changes?', 
                                                     buttons= QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
                else:
                        QCoreApplication.exit()
                        return
                if button==QMessageBox.StandardButton.Save:
                        self.save_file()
                elif button==QMessageBox.StandardButton.Discard:
                        QCoreApplication.exit()
                event.ignore()

if __name__=='__main__':    
        app = QApplication([])
        app.setStyle('Fusion')
        window = MainWindow()
        window.show()
        app.exec()
