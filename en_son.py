import sys
from dronekit import connect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton, QSpinBox
from pyqtlet import L, MapWidget
from PyQt5.QtCore import QTimer
from flyshark import Tarama
from Ui import Labels
import time
import socket
import math


class MapWindow(QWidget):
    def __init__(self):
        # Setting up the widgets and layout
        super().__init__()
        self.ui = Labels()
        self.ui.show()

        self.ui.LabelYukseklik.setText("30m")
        self.ui.LabelBatarya.setText("%35")
        self.ui.LabelDistance.setText("250m")
        self.ui.LabelHiz.setText("25m/s")
        self.ui.LabelUydu.setText("16")
        self.ui.LabelUcusSuresi.setText(" 30dk")
        self.ui.LabelKalanSure.setText("35dk")
        self.ui.LabelArm.setText("BAĞLANTI YOK")
        self.ui.LabelMode.setText("GUIDED")

        token = "pk.eyJ1IjoiaGFsaXM1MyIsImEiOiJjbGZ6MmhobWMwaDFwM29tczdoMzdnNnhpIn0.ZG4ao0g2QBDINMQKw3UjAg"
        # Working with the maps with pyqtlet
        self.map = L.map(self.ui.mapWidget)
        self.map.setView([37.176234977, 33.25319639], 19)
        L.tileLayer('https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)).addTo(self.map)
        self.secilen_kose = []

        self.ui.butonBitti.clicked.connect(self.bitti)
        self.ui.butonSil.clicked.connect(self.sil)
        self.ui.butonGorev.clicked.connect(self.gorev)
        self.ui.butonYukle.clicked.connect(self.yukle)

        self.timerSpin = QTimer()
        self.timerSpin.setInterval(1000)
        self.timerSpin.timeout.connect(self.spinKontrol)

        self.saniye = 0
        self.dakika = 0
        self.sayac = 0
        self.koseSayac = 0
        self.line_ids = []
        self.marker = []
        self.timer = QTimer()
        self.timer.setInterval(4000)
        self.timer.timeout.connect(self.check_connection)
        # self.timer.start()
        self.timerVeri = QTimer()
        self.timerVeri.setInterval(100)
        self.timerVeri.timeout.connect(self.guncelle)
        self.timerKararti = QTimer()
        self.timerKararti.setInterval(3600)
        self.timerKararti.timeout.connect(self.kararti)
        # self.timerKararti.start()

    def kararti(self):
        self.ui.LabelBos2.show()
        self.ui.LabelBekle.show()

    def connect_drone(self):
        try:

            self.iha = connect('com6', baud=115200, wait_ready=True)
            # Bağlantı başarılıysa burada gerekli işlemleri yapabilirsiniz
            print("Drone bağlantısı başarıyla sağlandı.")
            self.homeLat = self.iha.location.global_relative_frame.lat
            self.homeLng = self.iha.location.global_relative_frame.lon

            self.timerVeri.start()
            self.ui.LabelBos2.hide()
            self.ui.LabelBekle.hide()
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
        lat = self.iha.location.global_relative_frame.lat
        lon = self.iha.location.global_relative_frame.lon
        self.ui.LabelYukseklik.setText(str(self.iha.location.global_relative_frame.alt) + "m")
        self.ui.LabelBatarya.setText("%35")
        mesafe = self.Mesafe(self.homeLat, self.homeLng, lat, lon)
        self.ui.LabelDistance.setText("{:04d}".format(int(mesafe)) + "m")

        self.ui.LabelHiz.setText(str(self.iha.groundspeed) + "m/s")
        self.ui.LabelUydu.setText(str(int(self.iha.gps_0.satellites_visible)))
        # self.LabelKalanSure.setText(str(yukseklik) + "dk")
        self.ui.LabelMode.setText(self.iha.mode.name)

        if int(self.saniye) == 60:
            self.dakika += 1
            self.saniye = 0

        self.ui.LabelUcusSuresi.setText(str(self.dakika) + "." + "{:02d}".format(int(self.saniye)) + " dk")

        if self.iha.armed:
            self.ui.LabelArm.setText("UÇUŞA HAZIR")
            self.ui.LabelArm.setStyleSheet("color : rgb(0, 255, 0)")

        else:
            self.ui.LabelArm.setText("HAZIR DEĞİL")
            self.ui.LabelArm.setStyleSheet("color : red")
            self.saniye += 0.1

    def secim(self, point):
        self.lat = str(point['latlng']['lat'])
        self.lon = str(point['latlng']['lng'])
        self.secilen_kose.append([self.lat, self.lon])
        self.koor = L.marker([self.lat, self.lon])
        self.marker.append(self.koor)
        self.map.addLayer(self.marker[self.sayac])
        self.sayac = self.sayac + 1

    def yukle(self):
        self.flyshark.txt_yazdir()
        self.ui.butonSil.hide()
        self.ui.butonBitti.hide()
        self.ui.spin.hide()
        self.ui.butonYukle.hide()
        for i in range(self.sayac):
            self.map.removeLayer(self.marker[i])
        self.txt_gonder()

    def gorev(self):
        self.map.clicked.connect(self.secim)
        self.ui.butonSil.show()
        self.ui.butonBitti.show()
        self.ui.spin.show()
        self.ui.butonYukle.show()

    def bitti(self):
        self.ciz()
        self.map.clicked.disconnect(self.secim)

    def ciz(self):
        self.aralik = self.ui.spin.value()
        self.flyshark = Tarama(self.map, self.secilen_kose, self.aralik)
        self.timerSpin.start()

    def sil(self):
        for i in range(self.sayac):
            self.map.removeLayer(self.marker[i])
        self.sayac = 0
        self.secilen_kose.clear()
        self.marker.clear()
        self.flyshark.remove_lines()
        self.flyshark.remove_polygon()
        self.map.clicked.connect(self.secim)
        self.timerSpin.stop()

    def spinKontrol(self):
        if self.ui.spin.value() != self.aralik:
            self.flyshark.remove_lines()
            self.flyshark.remove_polygon()
            self.ciz()

    def Mesafe(self, lat1, lon1, lat2, lon2):
        dlon = lon1 - lon2
        dlat = lat1 - lat2
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        metre = (int(c * r * 1000))
        return metre

    def txt_gonder(self):
        # Hedef IP adresi ve port numarasını belirtin
        hedef_IP = '192.168.137.206'  # Alıcı cihazın IP adresini buraya yazın
        port = 12345  # Kullanılacak port numarasını belirleyin

        # Göndermek istediğiniz dosyanın dosya yolunu belirtin
        dosya_yolu = 'dosya.txt'

        # Dosyanın baytlarını okuyun
        with open(dosya_yolu, 'rb') as dosya:
            dosya_icerik = dosya.read()

        # Soket oluşturun ve bağlantıyı kurun
        soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soket.connect((hedef_IP, port))

        # Dosyanın baytlarını gönderin
        soket.sendall(dosya_icerik)

        # Soketi kapatın
        soket.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())