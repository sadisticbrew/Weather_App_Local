import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.submit_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(" ", self)
        self.emoji_label = QLabel(" ", self)
        self.description_label = QLabel(" ", self)

        self.initUI()
    def initUI(self):
        self.setGeometry(0,0,500, 500)
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.submit_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignHCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.submit_button.setObjectName("submit_button")

        self.setStyleSheet("""
            WeatherApp{
                background-color: #E4E4E4;
            }
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 25px;
            }
            QPushButton#submit_button{
                font-size: 20px;
                border: 2px solid;
                margin: 5px;
                padding: 5px;
                border-radius: 7px;
                background-color: #96BBBB;
            }
            QPushButton#submit_button:hover{
                background-color: #618985;
            }
            QLabel#temp_label{
                font-size: 40px;
            }
            QLabel#emoji_label{
                font-size: 75px;
                font-family: segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
                font-family: noto sans;
            }
            """)
        self.submit_button.clicked.connect(self.get_weather)
    def get_weather(self):
        api_key = "352cce2411a139ff24a929d55a3fe900"
        city_name = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("cod") == "404":
                self.description_label.setStyleSheet("font-size: 20px;""color: red")
                self.description_label.setText("City not found. Please try again.")
                self.temp_label.setText("")
                self.emoji_label.setText("❓")
                self.city_label.setText("")
                return
            elif data.get("cod") != 200:
                self.description_label.setStyleSheet("font-size: 20px;""color: red")
                self.description_label.setText(f"API Error: {data.get('message', 'Unknown error')}")
                self.temp_label.setText("")
                self.emoji_label.setText("❗")
                self.city_label.setText("")
                return
            else:
                self.display_weather(data)
        except requests.exceptions.HTTPError as e:
            self.description_label.setStyleSheet("font-size: 20px;""color: red")
            self.description_label.setText(f"HTTP Error: {e}")
            self.temp_label.setText(" ")
            self.emoji_label.setText("❗")
            self.city_label.setText(" ")
        except requests.exceptions.ConnectionError:
            self.description_label.setStyleSheet("font-size: 20px;""color: red")
            self.description_label.setText("Network error. Check your internet connection.")
            self.temp_label.setText("")
            self.emoji_label.setText("🔌")
            self.city_label.setText("")
        except Exception as e:
            self.description_label.setStyleSheet("font-size: 20px;""color: red")

            self.description_label.setText(f"An unexpected error occurred: {e}")
            self.temp_label.setText("")
            self.emoji_label.setText("❌")
            self.city_label.setText("")
    def display_weather(self, data):
        self.city_label.setText(f"{self.city_input.text()}")
        self.temp_label.setText(f"{data['main']['temp']} °C")
        id = str(data['weather'][0]['id'])
        if id[0] == 2:
            self.emoji_label.setText("⛈️")
        elif id[0] == 3:
            self.emoji_label.setText("🌦️")
        elif id[0] == 5:
            self.emoji_label.setText("🌧️")
        elif id[0] == 6:
            self.emoji_label.setText("🌨️")
        elif id[0] == 7:
            self.emoji_label.setText("⛅")
        elif id == 800:
            self.emoji_label.setText("☀️")
        else:
            self.emoji_label.setText("☁️")
        self.description_label.setText(f"{data['weather'][0]['description']}")
        self.city_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
