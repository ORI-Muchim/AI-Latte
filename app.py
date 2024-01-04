import time
import sys
import winsound
import threading

from gpt import start_chat_gpt, send_message, get_latest_response
import undetected_chromedriver as uc

from inference import voice_gen

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QFont, QFontDatabase, QFontInfo, QTextCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer, QThread, pyqtSignal

driver = uc.Chrome(enable_cdp_events=True)
start_chat_gpt(driver)

class ApiThread(QThread):
    responseSignal = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        send_message(driver, self.message)
        response = get_latest_response(driver)
        self.responseSignal.emit(response)
        print("응답: ", response)

class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMediaPlayer()
        self.currentText = ""
        self.currentHtml = ""

    def initMediaPlayer(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("bgm.wav")))
        self.player.setVolume(5)
        
        self.player.mediaStatusChanged.connect(self.repeatMusic)
        self.player.play()

    def repeatMusic(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def initUI(self):
        self.setWindowTitle('AI-Latte Chat UI')
        self.pixmap = QPixmap('back.png')
        self.setWindowIcon(QIcon('icon.png'))
        
        fontInfo = QFontInfo(self.font())
        print("Current font:", fontInfo.family(), "Size:", fontInfo.pointSize())
        print("\n")
        
        white_text_style = "color: white;"
        transparent_style = "background-color: rgba(0, 0, 0, 127);"
        no_border_style = "border: none;"

        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setStyleSheet(transparent_style + white_text_style + no_border_style)

        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText("메시지를 입력하세요.")
        self.userInput.setFixedHeight(40)
        self.userInput.setStyleSheet(transparent_style + white_text_style + no_border_style)
        self.userInput.returnPressed.connect(self.sendMessage)
        QTimer.singleShot(100, self.userInput.setFocus)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.chatHistory, 1)
        layout.addWidget(self.userInput, 1)

        self.setLayout(layout)
        self.resize(1536, 864)
    
    def playSound(self):
        winsound.PlaySound(self.audioPath, winsound.SND_FILENAME)

    def sendMessage(self):
        message = self.userInput.text()
        if message:
            print("내가 보낸 메시지: ", message)
            self.chatHistory.clear()
            self.chatHistory.append("<span style='color: white;'>" + "현수: " + message + "</span>")
            self.userInput.clear()
            print("응답을 기다리는 중...")
            self.sendToApiAndReceiveResponse(message)

    def sendToApiAndReceiveResponse(self, message):
        self.apiThread = ApiThread(message)
        self.apiThread.responseSignal.connect(self.displayResponse)
        self.apiThread.start()

    def displayResponse(self, response):
        self.animateText("<span style='color: peachpuff;'>" + "권라떼: " + response + "</span>", "peachpuff", "./vitsoutput/latte/latte.wav")
        voice_gen(response)
        
    def animateText(self, text, color, audioPath):
        self.currentHtml = self.chatHistory.toHtml()
        self.fullText = "<span style='color: {};'>{}</span>".format(color, text)
        self.textIndex = 0
        self.audioPath = audioPath
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.addLetter)
        self.timer.start(18)

    def addLetter(self):
        if self.textIndex < len(self.fullText):
            self.currentHtml += self.fullText[self.textIndex]
            self.textIndex += 1
            self.chatHistory.setHtml(self.currentHtml)
        else:
            self.timer.stop()
            threading.Thread(target=self.playSound).start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_height = self.size().height() // 4 
        self.chatHistory.setMaximumHeight(new_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        super().paintEvent(event)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        font_id = QFontDatabase.addApplicationFont('./NEXON Lv2 Gothic Medium.ttf')
        if font_id == -1:
            print("폰트 설정 실패. 폰트 경로 확인.")
        else:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font = QFont(font_families[0], 25)
                app.setFont(font)

        ex = ChatBotUI()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit(1)
