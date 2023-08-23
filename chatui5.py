import sys
import requests
import json
import poe
import logging
import emoji

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QPushButton, QScrollBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ChatbotThread(QThread):
    got_response = pyqtSignal(str)

    def __init__(self, token, parent=None):
        super().__init__(parent)
        self.poe_client = poe.Client(token)
        self.queue = []

    def run(self):
        while True:
            message = self.queue[0] if len(self.queue) > 0 else None
            
            if message is None:
                break
            del self.queue[0]
            self.log("Got message from queue: " + message)
            response = ""
            for chunk in self.poe_client.send_message("capybara", message, with_chat_break=False):
                response += chunk["text_new"]
            self.log("Got response: " + response)
            self.got_response.emit(response)

    def log(self, message):
        print(message)


class ChatbotGui(QWidget):
    def __init__(self, token):
        super().__init__()

        self.chat_history = QPlainTextEdit()
        self.chat_history.setReadOnly(True)

        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.setDefault(True)
        self.send_button.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_history)
        layout.addWidget(self.user_input)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.chatbot_thread = ChatbotThread(token)
        self.chatbot_thread.got_response.connect(self.display_response)
        # self.chatbot_thread.queue = []

    def send_message(self):
        message = self.user_input.text()
        if message:
            self.chat_history.appendPlainText(f"You: {message}")
            self.user_input.clear()
            self.chatbot_thread.queue.append(message)
            self.chatbot_thread.start()

    def display_response(self, response):
        response = emoji.emojize(response)
        self.chat_history.appendPlainText(f"Bot: {response}")

        # Scroll to the bottom of the chat history
        scroll_bar = self.chat_history.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


if __name__ == "__main__":
    with open("/home/kashan/poe_api/token.txt", "r") as f:
        token = f.read().strip()

    app = QApplication(sys.argv)
    chatbot_gui = ChatbotGui(token)
    chatbot_gui.show()
    sys.exit(app.exec_())