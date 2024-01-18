from PyQt6.QtCore import QCoreApplication, QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QMessageBox, QLabel
from PyQt6.QtGui import QAction, QKeySequence, QCloseEvent, QIcon, QFont, QFontDatabase
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from qfluentwidgets import FluentIcon, Icon, Theme, setTheme
from qframelesswindow import FramelessDialog
import darkdetect

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
                save_action.setIcon(Icon(FluentIcon.SAVE))
                save_action.setShortcut(QKeySequence('Ctrl+s'))
                save_action.triggered.connect(self.save_file)

                save_as_action = QAction('Save as', self)
                save_as_action.setIcon(Icon(FluentIcon.SAVE_AS))
                save_as_action.setShortcut(QKeySequence('Ctrl+Shift+s'))
                save_as_action.triggered.connect(lambda: self.save_file(para='save_as'))

                exit_action = QAction('Exit', self)
                exit_action.setShortcut(QKeySequence('Ctrl+q'))
                exit_action.triggered.connect(self.closeEvent)

                self.cut_action = QAction('Cut', self)
                self.cut_action.setIcon(Icon(FluentIcon.CUT))
                self.cut_action.setShortcut(QKeySequence('Ctrl+x'))
                self.cut_action.triggered.connect(self.edit.cut)

                self.copy_action = QAction('Copy', self)
                self.copy_action.setIcon(Icon(FluentIcon.COPY))
                self.copy_action.setShortcut(QKeySequence('Ctrl+c'))
                self.copy_action.triggered.connect(self.edit.copy)

                paste_action = QAction('Paste', self)
                paste_action.setIcon(Icon(FluentIcon.PASTE))
                paste_action.setShortcut(QKeySequence('Ctrl+v'))
                paste_action.triggered.connect(self.edit.paste)

                select_all_action = QAction('Select all', self)
                select_all_action.setShortcut(QKeySequence('Ctrl+a'))
                select_all_action.triggered.connect(self.edit.selectAll)

                print_action = QAction('Print', self)
                print_action.setIcon(Icon(FluentIcon.PRINT))
                print_action.setShortcut(QKeySequence('Ctrl+p'))
                print_action.triggered.connect(self.print_out)

                about_action = QAction("About", self)
                about_action.triggered.connect(self.about)

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

                help_menu = menu.addMenu("Help")
                help_menu.addAction(about_action)

        def open_file(self):
                button = self.file_content_changed()
                if button==QMessageBox.StandardButton.Save:
                        return self.save_file()
                elif button==QMessageBox.StandardButton.Cancel:
                        return
                        
                filename, adress = QFileDialog.getOpenFileName(self)
                if filename:
                        self.filename = filename
                        self.f_name = self.filename.split('/')[-1]
                        try:
                                with open(self.filename, 'r') as f:
                                        self.data = f.read()
                                self.check = 0
                                self.edit.setText(self.data)
                                self.setWindowTitle(f'Notepad ({self.f_name})')
                                self.copy_name = self.filename
                        except UnicodeDecodeError:
                                file_extension = self.f_name.split('.')[-1].upper()
                                warning = f"a {file_extension}" if file_extension[0] not in 'AEIOU' else f"an {file_extension}"
                                QMessageBox.warning(self, 'Invalid file format', f'Cannot open {warning} file.')
                                self.filename = self.copy_name
                                self.f_name = self.filename.split('/')[-1]
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
                button = self.file_content_changed(True)
                
                if button==QMessageBox.StandardButton.Save:
                        return self.save_file()
                elif button==QMessageBox.StandardButton.Discard:
                        return QCoreApplication.exit()
                event.ignore()

        def file_content_changed(self, CloseEvent = False):
                if self.data!=self.edit.toPlainText() and self.filename:
                        return QMessageBox.question(self, 'Save changes', f'Do you want to save changes to {self.f_name}?', 
                                                     buttons= QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
                                                     | QMessageBox.StandardButton.Cancel)
                elif self.filename=='' and self.edit.toPlainText():
                        return QMessageBox.question(self, 'Save changes', 'Do you want to save changes?', 
                                                     buttons= QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
                                                     | QMessageBox.StandardButton.Cancel)
                elif CloseEvent:
                        return QCoreApplication.exit()
                
        def about(self):
            color = "cyan" if theme=="dark" else "red"
            current_date = QDate.currentDate()
            dialog = FramelessDialog(self)
            dialog.setFixedSize(350, 170)
            about_label = QLabel("About Notepad\n", dialog)
            about_label.setGeometry(18, 30, len(about_label.text())*20, about_label.height())
            about_label.setStyleSheet(f"font-size: 25px; color: {color}; text-decoration: underline")
            QLabel(f"\n\n\n\n     Copyright © {current_date.year()} AnkurMal.", dialog)
            QLabel("\n\n\n\n\n     All rights reserved.", dialog)
            dialog.exec()

if __name__=='__main__': 
    theme = "light"
    app = QApplication([])
    if(darkdetect.isDark()):
        app.setStyle('Fusion')
        setTheme(Theme.DARK)
        theme = "dark"      
    window = MainWindow()
    window.show()
    app.exec()
