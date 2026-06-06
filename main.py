import sys
import csv
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, QCompleter)
from PyQt6.QtCore import Qt, QStringListModel



class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Application")

        self.MainWidget = QWidget()
        self.setCentralWidget(self.MainWidget)

        self.vbox = QVBoxLayout(self.MainWidget)

        self.initUI()

    def initUI(self):
        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)

        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("", self)

        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)


        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vbox.addWidget(self.city_label)
        self.vbox.addWidget(self.city_input)
        self.vbox.addWidget(self.get_weather_button)
        self.vbox.addWidget(self.temperature_label)
        self.vbox.addWidget(self.emoji_label)
        self.vbox.addWidget(self.description_label)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
           QLabel, QPushButton{
             font-family: Bahnschrift;
        }
           QLabel#city_label{
                font-size: 40px;
                font-weight: bold;
        }
        QLineEdit#city_input{
           font-size: 40px;
           font-style: italic;
        }
        QPushButton#get_weather_button{
           font-size: 30px;
           font-style: italic;
        }QLabel#temperature_label{
           font-size: 75px;
        }
        QLabel#emoji_label{
            font-size: 100px;
            font-family: Segoe UI emoji;
        }
        QLabel#description_label{
            font-size: 50px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

        self.city_input.returnPressed.connect(self.get_weather)




    def get_weather(self):

        self.temperature_label.clear()
        self.emoji_label.clear()
        self.description_label.clear()

        api_key = "c667ee61ba2b52084b720ef8f6c5027b"
        city=self.city_input.text()

        if not city:
            self.display_error("Please enter a city name")
            return

        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
          response=requests.get(url)
          response.raise_for_status()
          data=response.json()

          if data["cod"] == 200:
            self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal server error:\nplease try again later")
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP Error occurred:\n{http_error}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nYour request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects error:\nCheck the url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error: {req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet(("font-size: 30px;"))
        self.temperature_label.setText(message)

        self.emoji_label.clear()
        self.description_label.clear()



    def display_weather(self, data):
        self.temperature_label.setStyleSheet(("font-size: 75px;"))
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k-273.15
        print(temperature_c)
        weather_id=data["weather"][0]["id"]
        rounded_temperature=round(temperature_c)
        weather_description=data["weather"][0]["description"]

        self.temperature_label.setText(f"{rounded_temperature}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")

    @staticmethod
    def get_weather_emoji(weather_id):

        if weather_id >=200 and weather_id <=232:
            return "⛈️"
        elif 300 <=weather_id <=321:
            return "🌦️"
        elif 500<=weather_id <=531:
            return "🌧️"
        elif 600<=weather_id <=622:
            return "❄️ "
        elif 701 <=weather_id <=741:
            return "🌫️"
        elif weather_id ==762:
            return "🌋"
        elif weather_id ==771:
            return "💨"
        elif weather_id ==781:
            return "🌪️"
        elif weather_id ==800:
            return "☀️"
        elif 801 <=weather_id <=804:
            return "☁️"
        else:
            return "🌍"





if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
