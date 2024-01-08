import os
import time
import random
import sys

from gpt import start_chat_gpt, send_message, get_latest_response
import undetected_chromedriver as uc

from inference import voice_gen
from get_model import download_model_if_not_exists

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

url = 'https://github.com/ORI-Muchim/AI-Latte/releases/download/v1.0/G_107000.pth'

local_path = './models/latte/G_107000.pth'

result = download_model_if_not_exists(url, local_path)
print(result)

#driver = uc.Chrome(enable_cdp_events=True)
#start_chat_gpt(driver)

class VoiceGenThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, response):
        super().__init__()
        self.response = response

    def run(self):
        audioPath = voice_gen(self.response)
        self.finished.emit(audioPath)

class ApiThread(QThread):
    responseSignal = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        if "섹스" in self.message:
            responses = ["뭐? 섹스? 야! 섹스? 너 방금 섹스라고 했냐?", "섹스? 야, 섹스? 너 방금 섹스라고 했냐?"]
            response = random.choice(responses)
        else:
            #send_message(driver, self.message)
            #response = get_latest_response(driver)
            response = '야, 씹덕. 여기서 뭐하고 있어.'
        
        self.responseSignal.emit(response)
        print("응답:", response, end="")

class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMediaPlayer()
        self.currentText = ""
        self.currentHtml = ""
        self.soundPlayer = QMediaPlayer()
        self.foregroundPixmap = None
        self.faceImagePath = './resource/face/normal.png'
        self.displayRandomImage()

    def initMediaPlayer(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("./resource/bgm.wav")))
        self.player.setVolume(5)
        
        self.player.mediaStatusChanged.connect(self.repeatMusic)
        self.player.play()

    def repeatMusic(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def initUI(self):
        self.setWindowTitle('AI-Latte Chat UI')
        self.pixmap = QPixmap('./resource/back.png')
        self.setWindowIcon(QIcon('./resource/icon.png'))
        
        mainLayout = QVBoxLayout(self)

        fontInfo = QFontInfo(self.font())
        print("Current font:", fontInfo.family(), "Size:", fontInfo.pointSize())
        print("\n")

        text_style = "background-color: rgba(0, 0, 0, 127); color: white; border: none;"

        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setStyleSheet(text_style)
        mainLayout.addWidget(self.chatHistory, 1)

        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText("메시지를 입력하세요.")
        self.userInput.setStyleSheet(text_style)
        self.userInput.returnPressed.connect(self.sendMessage)
        mainLayout.addWidget(self.userInput, 1)

        topLayout = QHBoxLayout()
        self.selectImageButton = QPushButton("Select Image", self)
        self.selectImageButton.clicked.connect(self.selectImage)
        topLayout.addWidget(self.selectImageButton, 0, Qt.AlignRight | Qt.AlignTop)
        mainLayout.addLayout(topLayout)

        self.imageLabel = QLabel(self)
        mainLayout.addWidget(self.imageLabel)

        mainLayout.addWidget(self.chatHistory, 1)
        mainLayout.addWidget(self.userInput, 1)

        self.setLayout(mainLayout)
        self.resize(1536, 864)
        self.setFixedSize(self.size())
        
    def displayRandomImage(self):
        self.setAppBackground('./resource/back.png')
        characterFolder = './resource/clothes'
        faceImage = './resource/face/normal.png'

        try:
            images = [os.path.join(characterFolder, f) for f in os.listdir(characterFolder) if os.path.isfile(os.path.join(characterFolder, f))]
            
            if images:
                randomCharacter = random.choice(images)
                self.setCharacterImage(randomCharacter, faceImage)

        except Exception as e:
            print(f"Error loading random character image: {e}")

    def setCharacterImage(self, characterImagePath, faceImagePath):
        characterImage = QImage(characterImagePath)
        characterPixmap = QPixmap.fromImage(characterImage)

        faceImage = QImage(faceImagePath)
        facePixmap = QPixmap.fromImage(faceImage)

        painter = QPainter(characterPixmap)

        painter.drawPixmap(17, -120, facePixmap)
        painter.end()

        self.foregroundPixmap = characterPixmap
        self.update()
        
    def selectImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "./resource/clothes", "All Files (*);;Image Files (*.png;*.jpg)", options=options)
        if fileName:
            self.setAppForeground(fileName)
    
    def setAppBackground(self, imagePath):
        backgroundImage = QImage(imagePath)
        self.backgroundPixmap = QPixmap.fromImage(backgroundImage)
        self.update()

    def setAppForeground(self, imagePath):
        characterImage = QImage(imagePath)
        characterPixmap = QPixmap.fromImage(characterImage)

        faceImage = QImage(self.faceImagePath)
        facePixmap = QPixmap.fromImage(faceImage)

        painter = QPainter(characterPixmap)
        painter.drawPixmap(20, -120, facePixmap)
        painter.end()

        self.foregroundPixmap = characterPixmap
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.backgroundPixmap:
            painter.drawPixmap(self.rect(), self.backgroundPixmap)
        if self.foregroundPixmap:
            painter.drawPixmap(0, 0, self.foregroundPixmap)
        super().paintEvent(event)
    
    def playSound(self, audioPath):
        if os.path.exists(audioPath):
            url = QUrl.fromLocalFile(audioPath)
            self.soundPlayer.setMedia(QMediaContent(url))
            self.soundPlayer.stateChanged.connect(lambda: self.deleteAudioFile(audioPath))
            self.soundPlayer.play()
            
    def deleteAudioFile(self, audioPath):
        if self.soundPlayer.state() == QMediaPlayer.StoppedState:
            try:
                os.remove(audioPath)
                print(f"Deleted audio file: {audioPath}")
            except Exception as e:
                print("")

    def sendMessage(self):
        message = self.userInput.text()
        if message:
            print("내가 보낸 메시지:", message)
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
        self.animateText("<span style='color: peachpuff;'>" + "권라떼: " + response + "</span>", "peachpuff")
        self.voiceThread = VoiceGenThread(response)
        self.voiceThread.finished.connect(self.playVoiceAfterDelay)
        self.voiceThread.start()
        print()
        
    def playVoiceAfterDelay(self, audioPath):
        QTimer.singleShot(250, lambda: self.playSound(audioPath))
        
    def animateText(self, text, color):
        self.currentHtml = self.chatHistory.toHtml()
        self.fullText = "<span style='color: {};'>{}</span>".format(color, text)
        self.textIndex = 0
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_height = self.size().height() // 4 
        self.chatHistory.setMaximumHeight(new_height)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        font_id = QFontDatabase.addApplicationFont('./NEXON Lv2 Gothic Medium.ttf')
        if font_id == -1:
            print("폰트 설정 실패. 폰트 경로 확인.")
        else:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font = QFont(font_families[0], 27)
                app.setFont(font)

        ex = ChatBotUI()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit(1)
