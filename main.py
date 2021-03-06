from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import threading
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.window import Window
import socket
from os.path import exists


class MainPage(Screen):

    def start_tcp(self, *args):
        y = threading.Thread(target=self.tcp, daemon=True)  # Setup thread
        y.start()  # Starts thread

    def tcp(self):
        try:
            global s
            host = self.tcpip.text
            port = int(self.port.text)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                while True:
                    data = s.recv(1024)
                    datastr = data.decode("utf-8")
                    self.location_infotxt.text = self.location_infotxt.text + "\n" + datastr
        except Exception as e:
            Clock.schedule_once(self.start_tcp, 0.01)
            print("Reconnecting", e)


class ExercisePage(Screen):
    pass


class ExercisePopUp(Screen):
    img_ico = StringProperty("./img/testico1.png")

    def exercise_name(self):
        text = open("exercise_name.txt", "r", encoding="utf-8").read().split('&')
        if text[int(self.var//100) - 1][0] == "\n":
            exercise_name = text[int(self.var // 100) - 1].replace(text[int(self.var//100) - 1][0], "")
        else:
            exercise_name = text[int(self.var//100) - 1]
        if '\\n' in exercise_name:
            exercise_name = exercise_name.split('\\n')
            exercise_name = "\n".join(exercise_name)
        self.location_info.text = exercise_name

    def testico(self):
        self.var += 1
        if self.var % 2 == 1:
            self.my_ico1.source = './img/testico2.png'

        else:
            self.my_ico1.source = './img/testico1.png'

    def send_data(self):
        global s
        try:
            data_container = ["q", "Q", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "p", "P", "a", "A", "s", "S",
                              "d", "D", "f", "F", "g", "G", "h"]
            s.sendall(bytes(data_container[int(self.var / 100) - 1 - 2], 'ascii'))
            # if self.var == 100:
            #     s.sendall(b'w')
        except Exception as e:
            print("Not Connected.")

    def stopbutton(self):
        global stopflag, s
        try:
            s.sendall(b'z')
        except Exception as e:
            print("Not Connected.")

        pass

    pass


class CircuitPage(Screen):
    img_src = StringProperty("./img/100.png")

    def on_enter(self, *args):
        self.my_image1.source = f'./img/{self.var}.png'


class CircuitPage2(Screen):
    img2_src = StringProperty("./img/100.png")
    file_exists = BooleanProperty(True)

    def on_enter(self, *args):
        self.image_source()

    def check_file(self):
        photos = [101, 201, 301, 401, 402, 403, 501, 502, 503, 504, 505, 601, 602, 603, 701, 702, 703, 704, 705,
                  801, 802, 803, 804, 805, 806, 901, 902, 903, 1001, 1002, 1003, 1004, 1101, 1102, 1103, 1104, 1201,
                  1202, 1203, 1204, 1205, 1301, 1302, 1303, 1304, 1305, 1306, 1401, 1402, 1403, 1404, 1405, 1501,
                  1502, 1503, 1504, 1505, 1506, 1507, 1601, 1602, 1603, 1604, 1701, 1702, 1703, 1704, 1801, 1901,
                  1902, 1903, 1904, 1905, 2001, 2002, 2003, 2004, 2005, 2101, 2102, 2103, 2104, 2105, 2106, 2107,
                  2201, 2202, 2203, 2204, 2205, 2206, 2207, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309,
                  2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409, 2410, 2501, 2502, 2503, 2504, 2505, 2601,
                  2602, 2603, 2604, 2605, 2606, 2607, 2608, 2701, 2702, 2703, 2704, 2705, 2706, 2707]
        if exists(f"./img/{self.var}.png"):
            if self.var % 100 != 0 and self.var in photos:
                text = open("aciklama.txt", "r", encoding="utf-8").read().split('&')  # Read .txt file
                if '\\n' in text[photos.index(self.var)]:
                    text = text[photos.index(self.var)].split('\\n')
                    text = "\n".join(text)
                else:
                    text = text[photos.index(self.var)]

                self.txt_input.text = text
            self.file_exists = True
        elif not exists(f"./img/{self.var}.png"):
            self.file_exists = False

    def image_source(self):
        self.check_file()
        if self.file_exists is True:
            self.my_image2.source = f'./img/{self.var}.png'
        elif self.file_exists is False:
            pass

    pass


class Player(Screen):

    def on_enter(self, *args):
        self.my_video.source = f'./img/{self.var}.mp4'
        pass

    pass


class PlcPage(Screen):
    file_exists = BooleanProperty(True)

    def on_enter(self, *args):
        self.image_source()

    def check_file(self):
        if exists(f"./img/{self.var}.png"):
            self.file_exists = True
        elif not exists(f"./img/{self.var}.png"):
            self.file_exists = False

    def image_source(self):
        self.check_file()
        if self.file_exists is True:
            self.my_image3.source = f'./img/{self.var}.png'
        elif self.file_exists is False:
            pass

    pass


class MyApp(App):
    Window.size = (1280, 720)
    pass


if __name__ == '__main__':
    MyApp().run()