import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

import friday_cli as friday
import gui_resource_library


class SpeechRecognitionThread(QThread):
    newUserText = pyqtSignal(str)
    newComputerText = pyqtSignal(str)
    recognitionEnded = pyqtSignal(str)

    def __init__(self, parent, current_topic, listen=True, entered_user_text=None):
        super(SpeechRecognitionThread, self).__init__(parent)

        self.current_topic = current_topic
        self.listen = listen
        self.entered_user_text = entered_user_text

        self.start()

    def run(self):
        result = friday.listen_microphone(fallback=False) if self.listen else self.entered_user_text

        if result is not None:
            self.newUserText.emit(result)
        else:
            result = ""

        self.current_topic = friday.user_input_parser(result, self.current_topic, self.newComputerText)
        if self.current_topic is None:
            self.current_topic = ""

        self.recognitionEnded.emit(self.current_topic)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        self.browser = QWebEngineView(self)
        self.browser.setHtml(gui_resource_library.main_html)
        self.browser.loadFinished.connect(self.start_microphone)

        layout.addWidget(self.browser, 0, 0, 1, 0)

        self.line = QLineEdit()
        self.line.setPlaceholderText("Ask me anything…")
        self.line.returnPressed.connect(self.text_query)
        layout.addWidget(self.line, 1, 0)

        self.mic_button = QPushButton("")
        self.mic_button.clicked.connect(self.start_microphone)
        self.mic_button.setIcon(QIcon('mic_off.png'))
        self.mic_button.setEnabled(False)

        layout.addWidget(self.mic_button, 1, 1)

        self.currentTopic = "greet"
        self.speechRecognitionThread = None

    def start_microphone(self, entered_user_text=None):
        self.setWindowTitle("%s" % self.browser.page().title())

        if not isinstance(entered_user_text, str):
            entered_user_text = None

        self.speechRecognitionThread = SpeechRecognitionThread(self, self.currentTopic, False if self.currentTopic == "greet" or entered_user_text is not None else True, entered_user_text=entered_user_text)
        self.speechRecognitionThread.newUserText.connect(self.on_user_text)
        self.speechRecognitionThread.newComputerText.connect(self.on_pc_text)
        self.speechRecognitionThread.recognitionEnded.connect(self.ready_for_next_conversation)

    def ready_for_next_conversation(self, value):
        self.line.setEnabled(True)
        self.currentTopic = value
        self.start_microphone()

    def on_user_text(self, value):
        self.browser.page().runJavaScript(gui_resource_library.speech_bubble_right(value))

    def on_pc_text(self, value):
        self.line.setEnabled(False)  # when pc is speaking it would otherwise crash when enter enter gets pressed

        for i in value.split("\n"):
            self.browser.page().runJavaScript(gui_resource_library.speech_bubble_left(i))

    def terminate_speech_recognition_thread(self):
        if self.speechRecognitionThread is not None and self.speechRecognitionThread.isRunning():
            self.speechRecognitionThread.terminate()

    def text_query(self):
        if self.line.text().strip() != "":
            self.terminate_speech_recognition_thread()
            self.start_microphone(entered_user_text=self.line.text())
            self.line.clear()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.argv.append(" --enable-smooth-scrolling")
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setApplicationName("Friday - Personal Assistant")

    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 2 / 3)
    mainWin.show()
    sys.exit(app.exec_())
