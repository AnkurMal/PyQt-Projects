from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QFont

class MainWindow(QMainWindow):
        def __init__(self):
                super().__init__()
                self.setWindowTitle("Music Player")
                self.setWindowIcon(QIcon('media_player.png'))
                self.setMinimumSize(1000, 550)

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

                self.play_pause_button = QPushButton()
                self.play_pause_button.setIcon(QIcon('play_button.png'))
                self.play_pause_button.setFixedSize(65, 65)
                self.play_pause_button.setIconSize(QSize(65, 65))
                self.play_pause_button.setStyleSheet('border-radius: 1px')
                self.play_pause_button.setDisabled(True)

                self.progress = QSlider(orientation=Qt.Orientation.Horizontal)
                self.progress.setStyleSheet(slider_style)
                self.progress.setDisabled(True)
                self.progress.sliderPressed.connect(self.pause)
                self.progress.sliderReleased.connect(self.play)

                self.media_name_label = QLabel()
                self.media_name_label.setStyleSheet('font-size: 40px; font-weight: bold')
                self.media_name_label.setFixedHeight(50)
                f = QFont()
                f.setUnderline(True)
                self.media_name_label.setFont(f)

                self.media_properties_label = QLabel()
                self.media_properties_label.setStyleSheet('font-size: 20px; font-weight: bold')

                self.left_time_label = QLabel("0:00")
                self.right_time_label = QLabel("X:XX")

                v_layout = QVBoxLayout()
                h1_layout = QHBoxLayout()
                h2_layout = QHBoxLayout()
                container = QWidget()

                self.play_pause_button.pressed.connect(self.media_player)

                v_layout.addWidget(self.media_name_label)
                v_layout.addWidget(self.media_properties_label)
                h1_layout.addWidget(self.left_time_label)
                h1_layout.addWidget(self.progress)
                h1_layout.addWidget(self.right_time_label)
                h1_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
                v_layout.addLayout(h1_layout)
                h2_layout.addWidget(self.play_pause_button)
                v_layout.addLayout(h2_layout)
                container.setLayout(v_layout)

                self.setCentralWidget(container)

                open_action = QAction('Open', self)
                open_action.setShortcut(QKeySequence('Ctrl+o'))
                open_action.triggered.connect(self.open_file)

                exit_action = QAction('Exit', self)
                exit_action.setShortcut(QKeySequence('Ctrl+q'))
                exit_action.triggered.connect(app.exit)

                menu = self.menuBar()
                menu.setStyleSheet('font-size: 14px')
                file_menu = menu.addMenu('File')
                file_menu.addAction(open_action)
                file_menu.addAction(exit_action)

                self.media = QMediaPlayer()
                self.audio = QAudioOutput()

                self.audio.setVolume(10)
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
                        self.play_pause_button.setIcon(QIcon('pause_button.png'))
                else:
                        self.pause('No')
                        self.play_or_pause = 0
                        self.play_pause_button.setIcon(QIcon('play_button.png'))

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
                        album_name = metadata.value(QMediaMetaData.Key.Title)
                        artist_name =  metadata.value(QMediaMetaData.Key.AlbumArtist)
                        genre = metadata.value(QMediaMetaData.Key.Genre)

                        if album_name is None:
                                album_name = 'Unknown'
                        if artist_name is None:
                                artist_name = 'Unknown'
                        if genre is None:
                                genre = 'Unknown'

                        text = f'Artist name - {artist_name}\nGenre - {genre}'
                        self.media_name_label.setText(album_name)
                        self.media_properties_label.setText(text)

                        self.play_pause_button.setIcon(QIcon('play_button.png'))
                        self.play_pause_button.setDisabled(False)
                        self.progress.setDisabled(False)
                        self.progress.setMinimum(0)
                        self.progress.setMaximum(self.media.duration())
                        self.filename = ''
                       
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
