import sys
from dronekit import connect
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QMainWindow,  QDesktopWidget, QPushButton
from pyqtlet import L, MapWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage, QFont


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        yukseklik = 30.28
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.setWindowTitle("Map Window")
        self.resize(1024, 600)
        self.mapWidget = MapWidget()
        self.setCentralWidget(self.mapWidget)
        self.layout = QVBoxLayout(self)
        self.video_widget = QLabel(self)
        self.layout.addWidget(self.video_widget)
        self.layout.setGeometry(QtCore.QRect(760,400,240,180))



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
        self.pilResim.setGeometry(850,10,70,32)
        self.uydu = QLabel(self)
        self.uydu.setPixmap(self.uyduPng)
        self.uydu.setGeometry(795,10,40,32)
        self.KumSaat = QLabel(self)
        self.KumSaat.setPixmap(self.KumSaatPng)
        self.KumSaat.setGeometry(535,0,50,50)
        self.HizIcon = QLabel(self)
        self.HizIcon.setPixmap(self.HizPng)
        self.HizIcon.setGeometry(10,550,45,45)
        self.YukseklikIcon = QLabel(self)
        self.YukseklikIcon.setPixmap(self.yukseklikPng)
        self.YukseklikIcon.setGeometry(190,555,45,45)
        self.EvIcon = QLabel(self)
        self.EvIcon.setPixmap(self.evPng)
        self.EvIcon.setGeometry(350,555,300,45)
        self.SaatIcon = QLabel(self)
        self.SaatIcon.setPixmap(self.saatPng)
        self.SaatIcon.setGeometry(590,552,45,45)
        self.KapatIcon = QLabel(self)
        self.KapatIcon.mousePressEvent = self.kapat
        self.KapatIcon.setPixmap(self.kapatPng)
        self.KapatIcon.setGeometry(965, 2, 45, 45)

        self.flyshark = QLabel(self)
        self.flyshark.setPixmap(self.logoPng)
        self.flyshark.setGeometry(15,5,260,45)


        self.LabelYukseklik.setText(str(yukseklik) + "m")
        self.LabelBatarya.setText("%35")
        self.LabelDistance.setText(str(yukseklik) + "m")
        self.LabelHiz.setText(str(yukseklik)+ "m/s")
        self.LabelUydu.setText(str(int(yukseklik)))
        self.LabelUcusSuresi.setText(str(yukseklik)+ " dk")
        self.LabelKalanSure.setText(str(yukseklik) + "dk")
        self.LabelArm.setText("UÇUŞA HAZIR")
        self.LabelMode.setText("GUIDED")


        self.LabelBos.setGeometry(0,0,1024,50)
        self.LabelBos1.setGeometry(0,550,760,50)

        self.LabelBatarya.setGeometry(905,10,60,30)
        self.LabelUydu.setGeometry(830,0,20,20)
        self.LabelKalanSure.setGeometry(585,10,100,30)
        self.LabelArm.setGeometry(335,10,160,30)
        self.LabelMode.setGeometry(695,10,100,30)

        self.LabelHiz.setGeometry(60, 560, 120, 30)
        self.LabelYukseklik.setGeometry(240, 560, 230, 30)
        self.LabelDistance.setGeometry(407, 550, 100, 30)
        self.LabelUcusSuresi.setGeometry(640,560,290,30)




        self.LabelBos.setStyleSheet("background-color: rgba(0, 0, 0, 100)")
        self.LabelBos1.setStyleSheet("background-color: rgba(0, 0, 0, 100)")
        self.LabelYukseklik.setStyleSheet(" color: white")
        self.LabelBatarya.setStyleSheet("color: white")
        self.LabelDistance.setStyleSheet("color: white")
        self.LabelHiz.setStyleSheet(" color: white")
        self.LabelUydu.setStyleSheet(" color: white")
        self.LabelUcusSuresi.setStyleSheet(" color: white")
        self.LabelKalanSure.setStyleSheet(" color: white")
        self.LabelArm.setStyleSheet(" color:  rgb(0, 255, 0)")
        self.LabelMode.setStyleSheet(" color: rgb(255, 215, 0)")
        self.LabelYukseklik.setFont(self.font)
        self.LabelBatarya.setFont(self.font)
        self.LabelDistance.setFont(self.font)
        self.LabelHiz.setFont(self.font)
        #self.LabelUydu.setFont(self.font)
        self.LabelUcusSuresi.setFont(self.font)
        self.LabelKalanSure.setFont(self.font)
        self.LabelArm.setFont(self.font)
        self.LabelMode.setFont(self.font)




        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        token = "pk.eyJ1IjoiaGFsaXM1MyIsImEiOiJjbGZ6MmhobWMwaDFwM29tczdoMzdnNnhpIn0.ZG4ao0g2QBDINMQKw3UjAg"
        self.map = L.map(self.mapWidget)
        self.map.setView([37.176234977, 33.25319639], 19)
        L.tileLayer('https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)).addTo(self.map)
        #self.marker = L.marker([37.176234977, 33.25319639])
        #self.map.addLayer(self.marker)
        js_code = '''
        var greenIcon = L.icon({
            iconUrl: 'C://Users//halis gürbüz//PycharmProjects//hedef_2024//png//ahmet.jpg',
            iconSize: [75, 90]
        });
        var marker = L.marker([37.176234977, 33.25319639], { icon: greenIcon });
        marker.addTo(map);
        
        '''
        self.map.runJavaScript(js_code)








    def kapat(self):
        self.close()




    def kameraBuyu(self, event):
        print("deneme")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #iha = connect('com6', baud=115200, wait_ready=True)
    window = MapWindow()
    window.video_widget.mousePressEvent = window.kameraBuyu # video_widget'a mousePressEvent ekleyin
    window.show()
    sys.exit(app.exec_())
