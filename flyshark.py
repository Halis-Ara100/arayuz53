import math
from pyqtlet import L, MapWidget

class Tarama():
    def __init__(self, map, secilen_koseler, cizgi_arasi):
        super().__init__()
        self.latArray = []
        self.lonArray = []
        self.bolme1 = []
        self.bolme2 = []
        self.koseler = []
        self.kesen_nokta = 0
        self.bolme_sayisi = 0
        self.sira = []
        self.line_ids = []
        self.sayac = 0
        self.map = map
        self.secilenKoseler = secilen_koseler
        self.cizgi_arasi = cizgi_arasi

        # Kare köşe koordinatlarını oluşturun


        self.polygon_ekle()
        self.degerAl()
        self.kare()
        self.Bolme()
        self.sira_koordinat()
        self.siralama()
        self.line_ekle()



    def degerAl(self):
        for kose in self.secilenKoseler:
            self.latArray.append(float(kose[0]))
            self.lonArray.append(float(kose[1]))
            self.sayac+=1

    def remove_lines(self):
        for i in range(self.kesen_nokta):
            self.map.removeLayer(self.line_ids[i])
    def remove_polygon(self):
        self.map.removeLayer(self.polygon)
    def polygon_ekle(self):
        self.polygon = L.polygon(self.secilenKoseler, options = {"color": 'red'})
        self.map.addLayer(self.polygon)


    def kare(self):

        self.min_lat = float(min(self.latArray))
        self.max_lat = float(max(self.latArray))
        self.min_lng = float(min(self.lonArray))
        self.max_lng = float(max(self.lonArray))

        # Kare köşe koordinatlarını oluşturun

        self.koseler.append([self.min_lat, self.min_lng])
        self.koseler.append([self.max_lat, self.min_lng])
        self.koseler.append([self.max_lat, self.max_lng])
        self.koseler.append([self.min_lat, self.max_lng])



    def Mesafe(self,LatLon1, LatLon2):
        # Radyan cinsinden koordinatları hesapla
        lat1_rad = math.radians(LatLon1[0])
        lon1_rad = math.radians(LatLon1[1])
        lat2_rad = math.radians(LatLon2[0])
        lon2_rad = math.radians(LatLon2[1])

        # Deltas
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # Haversine formülü
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        r = 6371  # Yeryüzündeki ortalama yarıçap: 6371 km

        distance = c * r * 1000  # Mesafeyi metre cinsinden hesapla

        return distance
    def Bolme(self):
        mesafe = self.Mesafe(self.koseler[0], self.koseler[1])
        aralik = (self.koseler[1][0] - self.koseler[0][0]) / mesafe
        metre30 = aralik * self.cizgi_arasi

        for i in range(int(mesafe / self.cizgi_arasi)):
            self.bolme_sayisi += 1
            if i == 0:
                self.bolme1.append([self.min_lat, self.min_lng])
                self.bolme2.append([self.min_lat, self.max_lng])
            else:
                self.bolme1.append([self.bolme1[i - 1][0] + metre30, self.min_lng])
                self.bolme2.append([self.bolme2[i - 1][0] + metre30, self.max_lng])


    def sira_koordinat(self):
        for i in range(1,self.bolme_sayisi):
            p1 = self.bolme1[i]
            p2 = self.bolme2[i]
            for j in range(self.sayac):
                p3 = (self.latArray[j], self.lonArray[j])
                if j ==self.sayac-1:
                    p4 = (self.latArray[0], self.lonArray[0])
                else:
                    p4 = (self.latArray[j+1], self.lonArray[j+1])
                point = self.lineLineIntersection(p1, p2, p3, p4)
                if point != None:
                    control = self.kontrol(point, p3, p4)
                    if control == True:
                        self.sira.append(point)
                        self.kesen_nokta+= 1

    def siralama(self):

        for i in range(0, self.kesen_nokta-1, 2):
            if self.sira[i][1]> self.sira[i+1][1]:
                temp = self.sira[i]
                self.sira[i] =self.sira[i+1]
                self.sira[i+1] =temp

        for i in range(2,self.kesen_nokta-1,4):
            temp = self.sira[i]
            self.sira[i] = self.sira[i+1]
            self.sira[i+1] = temp

        self.sira.insert(0, self.koseler[0])

    def line_ekle(self):

        for i in range(self.kesen_nokta):
            line = L.polyline([self.sira[i], self.sira[i+1]], options = {"color": 'yellow'})
            self.line_ids.append(line)
            self.map.addLayer(line)


    def kontrol(self, marker, E , F):
        is_on_line = (min(E[0], F[0]) <= marker[0] <= max(E[0], F[0])) and (
                min(E[1], F[1]) <= marker[1] <= max(E[1], F[1]))
        if is_on_line == True:
            return True
        else:
            return None

    def lineLineIntersection(self, A, B, C, D):
        # Line AB represented as a1*lat + b1*lon = c1
        a1 = B[1] - A[1]
        b1 = A[0] - B[0]
        c1 = a1 * A[0] + b1 * A[1]
        # Line CD represented as a2*lat + b2*lon = c2
        a2 = D[1] - C[1]
        b2 = C[0] - D[0]
        c2 = a2 * C[0] + b2 * C[1]

        determinant = a1 * b2 - a2 * b1

        if determinant == 0:
            # The lines are parallel. Return a point with invalid coordinates
            return None
        else:
            lat = (b2 * c1 - b1 * c2) / determinant
            lon = (a1 * c2 - a2 * c1) / determinant
            return [lat, lon]




    def txt_yazdir(self):
        file = open("dosya.txt", "w")
        for i in self.sira:
            file.write(str(i[0]) + " "+ str(i[1]) + " 30" + "\n")
        file.close()