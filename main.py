import time
import sys
import math
from dronekit import connect
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication , QPushButton , QLabel ,QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QPropertyAnimation , QTimer

from pyqtlet import L, MapWidget
from folium.features import CustomIcon
from PyQt5.QtGui import QPixmap, QImage, QFont


class MapWindow(QWidget):
    def __init__(self):
        # Setting up the widgets and layout
        super().__init__()
        yukseklik = 30.28
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.resize(1024, 600)

        self.mapWidget = MapWidget()
        self.layout = QVBoxLayout()
        self.layout.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.mapWidget)
        self.setLayout(self.layout)
        token = "pk.eyJ1IjoiaGFsaXM1MyIsImEiOiJjbGZ6MmhobWMwaDFwM29tczdoMzdnNnhpIn0.ZG4ao0g2QBDINMQKw3UjAg"
        # Working with the maps with pyqtlet
        self.map = L.map(self.mapWidget)
        self.map.setView([37.176234977, 33.25319639], 19)
        L.tileLayer('https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)).addTo(self.map)
        self.marker = L.marker([37.176234977, 33.25319639])
        self.marker.bindPopup('Maps are a treasure.')
        self.map.addLayer(self.marker)


        self.timer = QTimer()
        self.timer.setInterval(4000)
        self.timer.timeout.connect(self.check_connection)
        self.timer.start()
        self.timerVeri = QTimer()
        self.timerVeri.setInterval(100)
        self.timerVeri.timeout.connect(self.guncelle)
        self.timerKararti = QTimer()
        self.timerKararti.setInterval(3600)
        self.timerKararti.timeout.connect(self.kararti)
        self.timerKararti.start()

        self.LabelBos = QLabel(self)
        self.LabelBos1 = QLabel(self)
        self.LabelYukseklik = QLabel(self)
        self.LabelBatarya = QLabel(self)
        self.LabelDistance = QLabel(self)
        self.LabelHiz = QLabel(self)
        self.LabelUydu = QLabel(self)
        self.LabelUcusSuresi = QLabel(self)
        self.LabelKalanSure = QLabel(self)
        self.LabelArm = QLabel(self)
        self.LabelMode = QLabel(self)

        self.buton = QPushButton(self)
        self.buton.setText("görev")
        self.buton.setGeometry(0, 510, 80, 40)
        self.buton.clicked.connect(self.gorev)
        self.buton.hide()

        self.butonBitir = QPushButton(self)
        self.butonBitir.setText("bitir")
        self.butonBitir.setGeometry(90,510,80,40)
        self.butonBitir.clicked.connect(self.bitir)
        self.butonBitir.hide()

        self.uyduPng = QPixmap('png/uydu.png')
        self.pil1Png = QPixmap('png/pil1.png')
        self.pil2Png = QPixmap('png/pil2.png')
        self.pil3Png = QPixmap('png/pil3.png')
        self.pil4Png = QPixmap('png/pil4.png')
        self.pil5Png = QPixmap('png/pil5.png')
        self.pilDoluPng = QPixmap('png/pildolu.png')
        self.KumSaatPng = QPixmap('png/kumSaati.png')
        self.HizPng = QPixmap('png/hız.png')
        self.yukseklikPng = QPixmap('png/yukseklik.png')
        self.evPng = QPixmap('png/uzaklık.png')
        self.saatPng = QPixmap('png/saat.png')
        self.kapatPng = QPixmap('png/kapat.png')
        self.logoPng = QPixmap('png/flyshark.png')

        self.pilResim = QLabel(self)
        self.pilResim.setPixmap(self.pil5Png)
        self.pilResim.setGeometry(850, 10, 70, 32)
        self.uydu = QLabel(self)
        self.uydu.setPixmap(self.uyduPng)
        self.uydu.setGeometry(795, 10, 40, 32)
        self.KumSaat = QLabel(self)
        self.KumSaat.setPixmap(self.KumSaatPng)
        self.KumSaat.setGeometry(535, 0, 50, 50)
        self.HizIcon = QLabel(self)
        self.HizIcon.setPixmap(self.HizPng)
        self.HizIcon.setGeometry(10, 550, 45, 45)
        self.YukseklikIcon = QLabel(self)
        self.YukseklikIcon.setPixmap(self.yukseklikPng)
        self.YukseklikIcon.setGeometry(190, 555, 45, 45)
        self.EvIcon = QLabel(self)
        self.EvIcon.setPixmap(self.evPng)
        self.EvIcon.setGeometry(350, 555, 300, 45)
        self.SaatIcon = QLabel(self)
        self.SaatIcon.setPixmap(self.saatPng)
        self.SaatIcon.setGeometry(590, 552, 45, 45)
        self.KapatIcon = QLabel(self)
        self.KapatIcon.mousePressEvent = self.kapat
        self.KapatIcon.setPixmap(self.kapatPng)
        self.KapatIcon.setGeometry(965, 2, 45, 45)

        self.flyshark = QLabel(self)
        self.flyshark.setPixmap(self.logoPng)
        self.flyshark.setGeometry(15, 5, 260, 45)

        self.LabelYukseklik.setText("m")
        self.LabelBatarya.setText("%35")
        self.LabelDistance.setText(str(yukseklik) + "m")
        self.LabelHiz.setText(str(yukseklik) + "m/s")
        self.LabelUydu.setText(str(int(yukseklik)))
        self.LabelUcusSuresi.setText(str(yukseklik) + " dk")
        self.LabelKalanSure.setText(str(yukseklik) + "dk")
        self.LabelArm.setText("BAĞLANTI YOK")
        self.LabelMode.setText("GUIDED")

        self.LabelBos2 = QLabel(self)
        self.LabelBekle = QLabel(self)
        self.LabelBekle.setText("BAĞLANIYOR...")
        self.LabelBekle.setGeometry(375, 285, 200, 30)
        self.LabelBekle.setStyleSheet("color: White")
        self.LabelBekle.hide()

        self.LabelBos.setGeometry(0, 0, 1024, 50)
        self.LabelBos1.setGeometry(0, 550, 760, 50)
        self.LabelBos2.setGeometry(0, 0, 1024, 600)
        self.LabelBos2.hide()

        self.LabelBatarya.setGeometry(905, 10, 60, 30)
        self.LabelUydu.setGeometry(830, 0, 20, 20)
        self.LabelKalanSure.setGeometry(585, 10, 100, 30)
        self.LabelArm.setGeometry(335, 10, 170, 30)
        self.LabelMode.setGeometry(695, 10, 100, 30)

        self.LabelHiz.setGeometry(60, 560, 120, 30)
        self.LabelYukseklik.setGeometry(240, 560, 230, 30)
        self.LabelDistance.setGeometry(413, 550, 100, 30)
        self.LabelUcusSuresi.setGeometry(640, 560, 290, 30)

        self.LabelBos.setStyleSheet("background-color: rgba(0, 0, 0, 100)")
        self.LabelBos1.setStyleSheet("background-color: rgba(0, 0, 0, 100)")
        self.LabelBos2.setStyleSheet("background-color: rgba(0, 0, 0, 200)")
        self.LabelYukseklik.setStyleSheet(" color: white")
        self.LabelBatarya.setStyleSheet("color: white")
        self.LabelDistance.setStyleSheet("color: white")
        self.LabelHiz.setStyleSheet(" color: white")
        self.LabelUydu.setStyleSheet(" color: white")
        self.LabelUcusSuresi.setStyleSheet(" color: white")
        self.LabelKalanSure.setStyleSheet(" color: white")
        self.LabelArm.setStyleSheet(" color:  red")
        self.LabelMode.setStyleSheet(" color: rgb(255, 215, 0)")
        self.LabelYukseklik.setFont(self.font)
        self.LabelBatarya.setFont(self.font)
        self.LabelDistance.setFont(self.font)
        self.LabelHiz.setFont(self.font)
        # self.LabelUydu.setFont(self.font)
        self.LabelUcusSuresi.setFont(self.font)
        self.LabelKalanSure.setFont(self.font)
        self.LabelArm.setFont(self.font)
        self.LabelMode.setFont(self.font)
        self.LabelBekle.setFont(self.font)
        self.sayac = 0
        self.saniye = 0
        self.dakika = 0

        self.show()


    def kararti(self):
        self.LabelBos2.show()
        self.LabelBekle.show()



    def connect_drone(self):
        try:

            self.iha = connect('com6', baud=115200, wait_ready=True)
            # Bağlantı başarılıysa burada gerekli işlemleri yapabilirsiniz
            print("Drone bağlantısı başarıyla sağlandı.")
            self.homeLat = self.iha.location.global_relative_frame.lat
            self.homeLng = self.iha.location.global_relative_frame.lon


            self.timerVeri.start()
            self.LabelBos2.hide()
            self.LabelBekle.hide()
            self.buton.show()
            return True
        except Exception as e:
            print("Drone bağlantısı başarısız.")
            # Bağlantı hatası durumunda buraya düşer
            time.sleep(3)

            return False

    def check_connection(self):
        self.timer.stop()
        self.timerKararti.stop()


        connected = False
        while not connected:

            connected = self.connect_drone()
            if not connected:
                time.sleep(3)


    def kapat(self):
        self.close()
    def guncelle(self):
        self.LabelYukseklik.setText(str(self.iha.location.global_relative_frame.alt) + "m")
        #self.LabelBatarya.setText("%35")
        mesafe = self.Mesafe(self.homeLat,self.homeLng,self.iha.location.global_relative_frame.lat,self.iha.location.global_relative_frame.lon)
        self.LabelDistance.setText("{:04d}".format(int(mesafe)) + "m")
        self.LabelHiz.setText(str(self.iha.groundspeed) + "m/s")
        self.LabelUydu.setText(str(int(self.iha.gps_0.satellites_visible)))
        #self.LabelKalanSure.setText(str(yukseklik) + "dk")
        self.LabelMode.setText(self.iha.mode.name)
        if int(self.sayac) == 60:
            self.dakika += 1
            self.sayac = 0


        self.LabelUcusSuresi.setText(str(self.dakika) + "." + "{:02d}".format(int(self.sayac)) + " dk")


        if self.iha.armed:
            self.LabelArm.setText("UÇUŞA HAZIR")
            self.LabelArm.setStyleSheet("color : rgb(0, 255, 0)")
            self.sayac += 0.1

        else:
            self.LabelArm.setText("HAZIR DEĞİL")
            self.LabelArm.setStyleSheet("color : red")
            if self.sayac !=0:
                self.sayac = 0


    def Mesafe(self,lat1,lon1,lat2,lon2):
        dlon = lon1 - lon2
        dlat = lat1 - lat2
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        metre = (int(c*r*1000))
        return metre

    def gorev(self):
        self.map.clicked.connect(self.koordinat)
        self.butonBitir.show()

    def koordinat(self, point):
        self.lat = str(round(point['latlng']['lat'], 7))
        self.lon = str(round(point['latlng']['lng'], 7))
        self.koor = L.marker([self.lat, self.lon])
        self.map.addLayer(self.koor)

    def bitir(self):
        self.map.clicked.disconnect(self.koordinat)
        self.butonBitir.hide()








if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())