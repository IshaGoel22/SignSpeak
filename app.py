
#pip install pyttsx3
#pip install pyqt5-sip
#colourLoop constants
# pip install googletrans==3.1.0a0
# pip install googletrans==4.0.0-rc1

#Import Library
import sys
sys.stdout.reconfigure(encoding='utf-8-sig')
# sys.stdout.reconfigure(encoding='utf-8')
from PyQt5 import QtCore
from PyQt5 import QtWidgets 
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets  import QApplication
import numpy as np
import cv2
import time
import random
import pyttsx3 as pyttsx
import autocomplete
import winsound
import os.path
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5 import QtGui
import time
from cvzone.HandTrackingModule import HandDetector
import torch
import joblib
import torch.nn as nn
import numpy as np
import argparse
import torch.nn.functional as F
import time
import cnn_models
# from torchvision import models
from googletrans import Translator
# import enchant
import random
from PyQt5.QtGui import QFont
from gtts import gTTS
import pygame
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

engine = pyttsx.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 1)

voices = engine.getProperty('voices')
for voice in voices:
    engine.setProperty('voice',voices[1].id)
    break

NUM_ROWS_OF_LETTERS=5
letColCount=-1
letRowCount=-1
stopRow=False
currentSentence=""
wholeText=""
vidOpen=False
currentDT = 0
timer = 0
closed = False
FinalWord = ""

translator = Translator()

lb = joblib.load('outputs/lb.pkl')
model = cnn_models.CustomCNN()
model.load_state_dict(torch.load('outputs/model.pth'))

def hand_area(img):
    hand = img[100:324, 100:324]
    hand = cv2.resize(hand, (224,224))
    return hand

def text_to_speech(text, language='en', filename='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename,"mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.quit()
    
    os.remove('output.mp3')


# ui.textBrowser_3.setText(predWord)
cap = cv2.VideoCapture(0)
countVal = 0
string = " "
prev = " "
allLang = []

def tick():
    global allLang
    global string
    global countVal

    if (cap.isOpened() == False):
        print('Error while trying to open camera. Plese check again...')
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('outputs/asl.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width,frame_height))

    while(cap.isOpened()):
        # capture each frame of the video
        ret, frame = cap.read()
        
        cv2.rectangle(frame, (100, 100), (324, 324), (20,34,255), 2)
        # cv2.rectangle(frame, (50, 50), (200, 200), (20,34,255), 2)
        # cv2.rectangle(frame, (200, 200), (400, 400), (20,34,255), 2)
        hand = hand_area(frame)

        image = hand
        
        image = np.transpose(image, (2, 0, 1)).astype(np.float32)
        image = torch.tensor(image, dtype=torch.float)
        image = image.unsqueeze(0)
        
        outputs = model(image)
        _, preds = torch.max(outputs.data, 1)
        # print("outputs: ",outputs)
        # print()
        print("count Val: ",countVal)
        
        countVal += 1
        opString = lb.classes_[preds]
        # if(countVal == 200):
        #     countVal = 99
        #     prev= lb.classes_[preds] 
        #     if(len(outputs) >= 2):
        #         string += " "             
        #     else:
        #         string += prev
        
        print()
        print("output: ",lb.classes_[preds])

        if countVal == 100 and opString != "nothing":
            if opString=="space":
                string += " "
            elif opString=="del":
                string = string[:-1]
            else:
                string += opString
            ui.textBrowser_4.setText(string)
            countVal = 0
        elif opString == "nothing":
            countVal = 0


        cv2.putText(frame, opString+": "+str(countVal), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.imshow('American Sign Language', frame)
        out.write(frame)

        # press 'q' to exit
        if cv2.waitKey(27) & 0xFF == ord('q'):
            break

    # release VideoCapture()
    cap.release()

    # close all frames and video windows
    cv2.destroyAllWindows()


def close():
    cap.release()
    cv2.destroyAllWindows()
    return 0
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.addLnOnly=True
        MainWindow.setObjectName(_fromUtf8("SignToText Translator"))
        MainWindow.resize(800, 600)
        self.go=True
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(65, 20, 680, 380))
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 480, 180, 51))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.addSpace)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(65, 480, 520, 51))
        self.textBrowser_4.setObjectName(_fromUtf8("textBrowser_4"))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuStart_Stop_Sel = QtWidgets.QMenu(self.menuSettings)
        self.menuStart_Stop_Sel.setObjectName(_fromUtf8("menuStart_Stop_Sel"))
        self.menuFinger = QtWidgets.QMenu(self.menuSettings)
        self.menuFinger.setObjectName(_fromUtf8("menuFinger"))
        self.menuLetter_Sel = QtWidgets.QMenu(self.menuSettings)
        self.menuLetter_Sel.setObjectName(_fromUtf8("menuLetter_Sel"))
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionWord_Sel = QtWidgets.QAction(MainWindow)
        self.actionWord_Sel.setObjectName(_fromUtf8("actionWord_Sel"))
        self.actionBlink = QtWidgets.QAction(MainWindow)
        self.actionBlink.setObjectName(_fromUtf8("actionBlink"))
        self.actionLeft_Wink = QtWidgets.QAction(MainWindow)
        self.actionLeft_Wink.setObjectName(_fromUtf8("actionLeft_Wink"))
        self.actionRight_Wink = QtWidgets.QAction(MainWindow)
        self.actionRight_Wink.setObjectName(_fromUtf8("actionRight_Wink"))
        self.actionBlink_2 = QtWidgets.QAction(MainWindow)
        self.actionBlink_2.setObjectName(_fromUtf8("actionBlink_2"))
        self.actionLeft_Wink_2 = QtWidgets.QAction(MainWindow)
        self.actionLeft_Wink_2.setObjectName(_fromUtf8("actionLeft_Wink_2"))
        self.actionRight_Wink_2 = QtWidgets.QAction(MainWindow)
        self.actionRight_Wink_2.setObjectName(_fromUtf8("actionRight_Wink_2"))
        self.actionAbout_EyeTotText = QtWidgets.QAction(MainWindow)
        self.actionAbout_EyeTotText.setObjectName(_fromUtf8("actionAbout_EyeTotText"))
        self.actionContact_Developer = QtWidgets.QAction(MainWindow)
        self.actionContact_Developer.setObjectName(_fromUtf8("actionContact_Developer"))
        self.menuStart_Stop_Sel.addAction(self.actionBlink)
        self.menuStart_Stop_Sel.addAction(self.actionLeft_Wink)
        self.menuStart_Stop_Sel.addAction(self.actionRight_Wink)
        self.menuFinger.addAction(self.actionBlink)
        self.menuFinger.addAction(self.actionLeft_Wink)
        self.menuFinger.addAction(self.actionRight_Wink)
        self.menuLetter_Sel.addAction(self.actionBlink_2)
        self.menuLetter_Sel.addAction(self.actionLeft_Wink_2)
        self.menuLetter_Sel.addAction(self.actionRight_Wink_2)
        self.menuSettings.addAction(self.menuStart_Stop_Sel.menuAction())
        self.menuSettings.addAction(self.menuLetter_Sel.menuAction())
        self.menuSettings.addAction(self.menuFinger.menuAction())
        self.menuSettings.addSeparator()
        self.menuHelp.addAction(self.actionAbout_EyeTotText)
        self.menuHelp.addAction(self.actionContact_Developer)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.buts=[self.pushButton_2]
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.textBrowser_2.setText(_translate("MainWindow", "", None))
        self.textBrowser_2.setAlignment(QtCore.Qt.AlignLeft)
        self.textBrowser_2.setFont(QtGui.QFont("MS Shell Dlg 2", 14))
        self.textBrowser_4.setText(_translate("MainWindow", "...", None))
        self.textBrowser_4.setAlignment(QtCore.Qt.AlignCenter)
        self.textBrowser_4.setFont(QtGui.QFont("MS Shell Dlg 2", 18))
        self.pushButton_2.setText(_translate("MainWindow", "Transalte & Speak", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.menuStart_Stop_Sel.setTitle(_translate("MainWindow", "Left Wink", None))
        self.menuFinger.setTitle(_translate("MainWindow", "Finger", None))
        self.menuLetter_Sel.setTitle(_translate("MainWindow", "Right Wink", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionWord_Sel.setText(_translate("MainWindow", "Finger", None))
        self.actionBlink.setText(_translate("MainWindow", "Same as Blink", None))
        self.actionLeft_Wink.setText(_translate("MainWindow", "Space", None))
        self.actionRight_Wink.setText(_translate("MainWindow", "Recite", None))
        self.actionBlink_2.setText(_translate("MainWindow", "Same as Blink", None))
        self.actionLeft_Wink_2.setText(_translate("MainWindow", "Space", None))
        self.actionRight_Wink_2.setText(_translate("MainWindow", "Recite", None))
        self.actionAbout_EyeTotText.setText(_translate("MainWindow", "About EyeTotText", None))
        self.actionContact_Developer.setText(_translate("MainWindow", "Contact Developer", None))
    
    # def pushSentenceToBody(self):
    #     global FinalWord
    #     global wholeText
    #     print("FinalWord")
    #     print(FinalWord)
    #     if FinalWord!="":
    #         if FinalWord[-1]==" ":
    #             FinalWord=FinalWord[0:-1]
    #         wholeText+=FinalWord+"."+"<br> "
    #         FinalWord=""
    #     self.textBrowser_2.setText(wholeText)
    #     self.textBrowser_4.setText(FinalWord)
    # def delLet(self):
    #     global FinalWord
    #     FinalWord=FinalWord[0:-1]
    #     self.textBrowser_4.setText(FinalWord)
    def addSpace(self):
        global allLang
        global string
        print()
        print("Global String: ",string)
        print()
        if len(string)>=0:
            font = QFont("Arial", 10) 
            ui.textBrowser_2.setFont(font)

            allLang.append(string)

            hindiOp = translator.translate(str(string), dest='hi') #hindi    
            print("hindi version: ",hindiOp.text)
            # ui.textBrowser_2.setText(str(hindiOp.text))
            # ui.textBrowser_2.setPlainText(str(hindiOp.text))
            allLang.append(hindiOp.text)

            gujratiOp = translator.translate(str(string), dest='gu') #gujrati
            print("gujrati version: ",gujratiOp.text)

            # ui.textBrowser_2.setText(str(gujratiOp.text))
            allLang.append(gujratiOp.text)

            punjabiOp = translator.translate(str(string), dest='pa') #punjabi
            print("punjabi version: ",punjabiOp.text)
            # ui.textBrowser_2.setText(str(punjabiOp.text))
            allLang.append(punjabiOp.text)

            allText = "Hindi Translate: "+hindiOp.text+"\n"+"Gujrati Translate: "+gujratiOp.text+"\n"+"punjabi Translate"+punjabiOp.text+"\n"
            ui.textBrowser_2.setPlainText(str(allText))
            
            hindi_text = ["Hindi Translate: "+hindiOp.text,"Gujrati Translate: "+gujratiOp.text,"punjabi Translate"+punjabiOp.text]
            for i in hindi_text:
                text_to_speech(i, language='hi')
                time.sleep(2)
            
            allLang.clear()
            string = " "
        else:
            print("No Data Available....!!")

    def openCam(self):
        print("hi")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(close)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    row5={0:ui.addSpace}
    # row5={0:ui.pauseBut, 1:ui.addSpace, 2:ui.delLet, 3:ui.pushSentenceToBody, 4:ui.reciteBut}
    # row6={0:ui.getPredWord, 1:ui.nurseBut}
    MainWindow.show()
    timer = QTimer()
    
    # engine.say("Initializing camera")
    # engine.runAndWait()
    
    timer.timeout.connect(tick)
    timer.start(100)
    timerColour = QTimer()
    timerColour.start(1000)
    sys.exit(app.exec_())
