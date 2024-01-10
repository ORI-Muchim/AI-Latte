import os
import time
import random
import sys
import re

from gpt import start_chat_gpt, send_message, get_latest_response
import undetected_chromedriver as uc

from inference import voice_gen
from get_model import download_model_if_not_exists

from get_emotion import get_emotion_from_response

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

url = 'https://github.com/ORI-Muchim/AI-Latte/releases/download/v1.0/G_107000.pth'

local_path = './models/latte/G_107000.pth'

result = download_model_if_not_exists(url, local_path)
print(result)

driver = uc.Chrome(enable_cdp_events=True)
start_chat_gpt(driver)

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
        if "섹스" in self.message and random.random() < 0.5:
            responses = ["뭐? 섹스? 야! 섹스? 너 방금 섹스라고 했냐?", "섹스? 야, 섹스? 너 방금 섹스라고 했냐?"]
            response = random.choice(responses)
        else:
            send_message(driver, self.message)
            response = get_latest_response(driver)
        
        self.responseSignal.emit(response)
        print("응답:", response)


class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMediaPlayer()
        self.currentText = ""
        self.currentHtml = ""
        self.soundPlayer = QMediaPlayer()
        self.currentCharacterImagePath = './resource/clothes/black.png'
        self.faceImagePath = './resource/face/normal.png'
        self.selectedCharacterImagePath = './resource/clothes/black.png'
        self.currentEmotion = "normal"
        self.foregroundPixmap = QPixmap(self.currentCharacterImagePath)
        self.updateFaceImage(self.currentEmotion)
        self.selectedImageHistory = []
        self.displayRandomImage()


    def initMediaPlayer(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("./resource/bgm.wav")))
        self.player.setVolume(7)
        
        self.player.mediaStatusChanged.connect(self.repeatMusic)
        self.player.play()


    def repeatMusic(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()
            
    def invert_icon_colors(self, icon_path):
        image = QImage(icon_path)
        image.invertPixels(QImage.InvertRgb)
        return QPixmap.fromImage(image)


    def initUI(self):
        self.setWindowTitle('AI-Latte')
        self.pixmap = QPixmap('./resource/background/sea.png')
        self.setWindowIcon(QIcon('./resource/icon.png'))
        
        mainLayout = QVBoxLayout(self)

        fontInfo = QFontInfo(self.font())
        print("Current font:", fontInfo.family(), "Size:", fontInfo.pointSize())

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
        self.selectImageButton = QPushButton(self)

        inverted_icon = self.invert_icon_colors('./resource/select.png')
        self.selectImageButton.setIcon(QIcon(inverted_icon))
        self.selectImageButton.setIconSize(QSize(75, 75))

        self.selectImageButton.setStyleSheet("background-color: rgba(0, 0, 0, 127); border: none;")

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
        self.setAppBackground('./resource/background/sea.png')
        characterFolder = './resource/clothes'
        
        try:
            images = [os.path.join(characterFolder, f) for f in os.listdir(characterFolder) if os.path.isfile(os.path.join(characterFolder, f))]
            
            if images:
                randomCharacter = random.choice(images)
                self.setCharacterImage(randomCharacter)
                self.selectedCharacterImagePath = randomCharacter
                
        except Exception as e:
            print(f"Error loading random character image: {e}")


    def setCharacterImage(self, characterImagePath):
        self.selectedCharacterImagePath = characterImagePath
        self.applyFaceToCharacter()


    def applyFaceToCharacter(self):
        characterImage = QImage(self.selectedCharacterImagePath)
        if characterImage.isNull():
            # print(f"Error loading character image from {self.selectedCharacterImagePath}")
            return
        characterPixmap = QPixmap.fromImage(characterImage)

        faceImage = QImage(self.faceImagePath)
        if faceImage.isNull():
            # print(f"Error loading face image from {self.faceImagePath}")
            return

        facePixmap = QPixmap.fromImage(faceImage)
        x_position = 17
        y_position = -120

        painter = QPainter(characterPixmap)
        painter.drawPixmap(x_position, y_position, facePixmap)
        painter.end()

        self.foregroundPixmap = characterPixmap
        print("Image loaded and applied successfully.")
        self.update()


    def selectImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "./resource/clothes", "All Files (*);;Image Files (*.png;*.jpg)", options=options)
        if fileName:
            self.setAppForeground(fileName)
            self.selectedCharacterImagePath = fileName
            self.selectedImageHistory.append(fileName)
            # print("Selected Image History:", self.selectedImageHistory)
    

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
        painter.drawPixmap(17, -120, facePixmap)
        painter.end()

        self.foregroundPixmap = characterPixmap
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)

        if self.backgroundPixmap:
            scaledBackground = self.backgroundPixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(self.rect(), scaledBackground)

        if self.foregroundPixmap:
            fgWidth = self.foregroundPixmap.width()
            fgHeight = self.foregroundPixmap.height()
            windowWidth = self.size().width()
            windowHeight = self.size().height()
            fgX = (windowWidth - fgWidth) // 2
            fgY = (windowHeight - fgHeight) // 2

            painter.drawPixmap(fgX, fgY, self.foregroundPixmap)

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


    def updateFaceImage(self, emotion):
        faceImageMap = {
            "laugh": "./resource/face/laugh.png",
            "laugh2": "./resource/face/laugh2.png",
            "cry": "./resource/face/cry.png",
            "hate": "./resource/face/hate.png",
            "hate2": "./resource/face/hate2.png",
            "hate3": "./resource/face/hate3.png",
            "normal": "./resource/face/normal.png",
            "littleshame": "./resource/face/littleshame.png",
            "shame": "./resource/face/shame.png",
            "supershame": "./resource/face/supershame.png",
            "worry": "./resource/face/worry.png",
            "disappointed": "./resource/face/disappointed.png",
            "hmm": "./resource/face/hmm.png"
        }
        default_emotion = "normal"
        self.faceImagePath = faceImageMap.get(emotion, faceImageMap[default_emotion])
        self.currentEmotion = emotion
        self.applyFaceToCharacter()


    def remove_bracketed_text(self, text):
        pattern = r'\[.*?\]'
        return re.sub(pattern, '', text)


    def displayResponse(self, response):
        cleaned_response = self.remove_bracketed_text(response)

        self.animateText("<span style='color: peachpuff;'>" + "권라떼: " + cleaned_response + "</span>", "peachpuff")
        self.voiceThread = VoiceGenThread(cleaned_response)
        self.voiceThread.finished.connect(self.playVoiceAfterDelay)
        self.voiceThread.start()

        emotion = get_emotion_from_response(response)
        QTimer.singleShot(1000, lambda: self.updateFaceImage(emotion))


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
