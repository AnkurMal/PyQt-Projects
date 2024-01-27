from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout, QFileDialog, QDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from PyQt6.QtCore import QUrl, Qt, QSize, QDate
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QFont, QFontDatabase
import darkdetect, sys

class MainWindow(QMainWindow):
	def __init__(self):
			super().__init__()
			self.setWindowTitle("Music Player")
			self.setWindowIcon(QIcon('images/media_player.png'))
			self.setMinimumSize(800, 450)

			height = 4
			slider_style = f'''
			QSlider {{
					margin-top: {height+1}px;
					margin-bottom: {height+1}px;
					}}

			QSlider::groove:horizontal {{
					border: red;
					height: {height}px;
					background: red;
					margin: {height // 4}px 0;
					}}

			QSlider::handle:horizontal {{
					background: white;
					border: {height} solid red;
					width: {height * 3};
					margin: {height * 2 * -1} 0;
					border-radius: {height * 2 + height // 2}px;
					}}

			QSlider::add-page:horizontal {{
					background: grey;
					height: {height}px;
					margin: {height // 4}px 0;
					}}'''
			
			self.check = 0
			self.pause_time = 0
			self.play_or_pause = 0

			self.play_pause_light = QPushButton()
			self.play_pause_light.setIcon(QIcon(f'images/play_{theme}.png'))
			self.play_pause_light.setFixedSize(65, 65)
			self.play_pause_light.setIconSize(QSize(65, 65))
			self.play_pause_light.setStyleSheet('border-radius: 1px')
			self.play_pause_light.setDisabled(True)

			self.progress = QSlider(orientation=Qt.Orientation.Horizontal)
			self.progress.setStyleSheet(slider_style)
			self.progress.setDisabled(True)
			self.progress.sliderPressed.connect(self.pause)
			self.progress.sliderReleased.connect(self.play)

			self.media_name_label = QLabel()
			self.media_name_label.setStyleSheet('font-size: 80px; color: red; text-decoration: underline')
			self.media_name_label.setFixedHeight(50)

			self.media_properties_label = QLabel()
			self.media_properties_label.setStyleSheet('font-size: 35px; color: violet')

			self.left_time_label = QLabel("0:00")
			self.right_time_label = QLabel("X:XX")

			v_layout = QVBoxLayout()
			h1_layout = QHBoxLayout()
			h2_layout = QHBoxLayout()
			container = QWidget()

			self.play_pause_light.pressed.connect(self.media_player)

			v_layout.addWidget(self.media_name_label)
			v_layout.addWidget(self.media_properties_label)
			h1_layout.addWidget(self.left_time_label)
			h1_layout.addWidget(self.progress)
			h1_layout.addWidget(self.right_time_label)
			h1_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
			v_layout.addLayout(h1_layout)
			h2_layout.addWidget(self.play_pause_light)
			v_layout.addLayout(h2_layout)
			container.setLayout(v_layout)

			self.setCentralWidget(container)

			open_action = QAction('Open', self)
			open_action.setShortcut(QKeySequence('Ctrl+o'))
			open_action.triggered.connect(self.open_file)

			exit_action = QAction('Exit', self)
			exit_action.setShortcut(QKeySequence('Ctrl+q'))
			exit_action.triggered.connect(app.exit)

			about_action = QAction("About", self)
			about_action.triggered.connect(self.about)

			menu = self.menuBar()
			menu.setStyleSheet('font-size: 25px')

			file_menu = menu.addMenu('File')
			file_menu.addAction(open_action)
			file_menu.addAction(exit_action)

			help_menu = menu.addMenu("Help")
			help_menu.addAction(about_action)

			self.media = QMediaPlayer()
			self.audio = QAudioOutput()

			self.media.setAudioOutput(self.audio)
			self.media.positionChanged.connect(self.progress_bar)
			self.progress.valueChanged.connect(self.manually_changed)

	def pause(self, x = ''):
			if x!='No':
					self.check = 1
			self.media.pause()
			self.pause_time = int(self.left_time_label.text()[-2:])

	def play(self):
			self.check = 0
			if self.play_or_pause == 1:
					self.media.play()

	def media_player(self):
			if self.play_or_pause==0:
					self.media.play()
					self.play_or_pause = 1
					self.play_pause_light.setIcon(QIcon(f'images/pause_{theme}.png'))
			else:
					self.pause('No')
					self.play_or_pause = 0
					self.play_pause_light.setIcon(QIcon(f'images/play_{theme}.png'))

	def progress_bar(self):
			minute = (self.media.position()//1000)//60
			second = (self.media.position()//1000)%60
			if second<10:
					self.left_time_label.setText(f"{minute}:0{second}")
			else:
					self.left_time_label.setText(f"{minute}:{second}")
			self.progress.setValue(self.media.position())
			if self.progress.value()==self.media.duration():
					self.media_player()
	
	def manually_changed(self, pos):
			if self.check==1:
					self.media.setPosition(pos)
					self.progress_bar()

	def open_file(self):
			self.filename, adress = QFileDialog.getOpenFileName(self, filter='*.mp3 *.pcm *.wav *.aiff *.acc *.m4a *.amv *.ogg *.wma *.flac *.alac')
			if self.filename:
					metadata_dict = {}
					self.play_or_pause = 0
					self.media.setSource(QUrl.fromLocalFile(self.filename))
					if self.media.duration()==0:
							return
					minute = (self.media.duration()//1000)//60
					second = (self.media.duration()//1000)%60
					if second<10:
							self.right_time_label.setText(f"{minute}:0{second}")
					else:
							self.right_time_label.setText(f"{minute}:{second}")

					metadata = QMediaMetaData(self.media.metaData())
					metadata_dict["album"] = metadata.value(QMediaMetaData.Key.Title)
					metadata_dict["artist"] =  metadata.value(QMediaMetaData.Key.AlbumArtist)
					metadata_dict["genre"] = metadata.value(QMediaMetaData.Key.Genre)

					for i in metadata_dict:
							if metadata_dict[i] is None:
									metadata_dict[i] = "Unknown"

					text = f'Artist name - {metadata_dict["artist"]}\nGenre - {metadata_dict["genre"]}'
					self.media_name_label.setText(metadata_dict['album'])
					self.media_properties_label.setText(text)

					self.play_pause_light.setIcon(QIcon(f'images/play_{theme}.png'))
					self.play_pause_light.setDisabled(False)
					self.progress.setDisabled(False)
					self.progress.setMinimum(0)
					self.progress.setMaximum(self.media.duration())
					self.filename = ''

	def about(self):
		color = "cyan" if theme=="light" else "red"
		current_date = QDate.currentDate()
		dialog = QDialog(self)
		dialog.setFixedSize(350, 170)
		about_label = QLabel("About Music Player", dialog)
		about_label.setGeometry(18, 30, len(about_label.text())*20, about_label.height())
		about_label.setStyleSheet(f"font-size: 35px; color: {color}; text-decoration: underline")
		QLabel(f"\n\n\n\n  Copyright © {current_date.year()} Ankur Mallick.", dialog)
		QLabel("\n\n\n\n\n  All rights reserved.", dialog)
		dialog.exec()

if __name__ == "__main__":
	theme = "dark"
	app = QApplication(sys.argv)
	if(darkdetect.isDark()):
		app.setStyle('Fusion')
		theme = "light"
	id = QFontDatabase.addApplicationFont("font/edge.ttf")
	families = QFontDatabase.applicationFontFamilies(id)
	app.setFont(QFont(families[0], 20))

	window = MainWindow()
	window.show()
	app.exec()
