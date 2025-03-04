from queue import PriorityQueue
import folium
from folium.plugins import Draw
import math


class knoten:
    def __init__(self, num, lat, lon):
        self.num = num
        self.lat = lat
        self.lon = lon


class kante:
    def __init__(self, knt1, knt2, distWeg):
        self.knt1 = knt1
        self.knt2 = knt2
        self.distWeg = distWeg

    def add_distZeit(self, distZeit):
        self.distZeit = distZeit

    def get_anderen_knoten(self, knt):
        if (self.knt1==knt):
            return self.knt2
        else:
            return self.knt1

class graph:
    # adj = [[knt1, k1, k2, k3...], [knt2, k1, k2, k3...]] (ind=knt.num)
    def __init__(self, adj):
        self.adj = adj
    
    def get_laenge(self):
        return len(self.adj)

    def add_knoten(self, knoten):
        self.adj.append([knoten])
    
    def add_kante(self, kante):
        self.adj[kante.knt1].append(kante)
        #self.adj[kante.knt2].append(kante) # nur bei ungerichtetem Graphen


    def dijkstra_weg(self, start, end):
        n = self.get_laenge()
        dist = [10000000]*n
        vorg = [0]*n
        pq = PriorityQueue()
        pq.put((0, start, start))
        
        while pq.qsize()>0:
            akt = pq.get()
            d = akt[0]
            knt = akt[1]
            vor = akt[2]
            if dist[knt] <= d: continue
            dist[knt] = d
            vorg[knt] = vor
            if knt==end: break
            for i in range(1, len(self.adj[knt])):
                kante = self.adj[knt][i]
                pq.put((d+kante.distWeg, kante.get_anderen_knoten(knt), knt))
        
        return dist, vorg
    
    def dijkstra_zeit(self, start, end):
        n = self.get_laenge()
        dist = [10000000]*n
        vorg = [0]*n
        pq = PriorityQueue()
        pq.put((0, start, start))
        
        while pq.qsize()>0:
            akt = pq.get()
            d = akt[0]
            knt = akt[1]
            vor = akt[2]
            if dist[knt] <= d: continue
            dist[knt] = d
            vorg[knt] = vor
            if knt==end: break
            for i in range(1, len(self.adj[knt])):
                kante = self.adj[knt][i]
                pq.put((d+kante.distZeit, kante.get_anderen_knoten(knt), knt))
        
        return dist, vorg


def get_weg(vorg, start, end):
    weg=[]
    akt=end
    while akt!=start:
        weg.append(akt)
        akt=vorg[akt]
    weg.append(start)
    return weg[::-1]

def datei_arbeit():
    fileKoord = open("USA-road-d.NY.co","r")
    fileKoord.readline()

    for i in fileKoord:
        tmp = i.split()[1:]
        tmp[1]=float(tmp[1][:3]+"."+tmp[1][3:])
        tmp[2]=float(tmp[2][:2]+"."+tmp[2][2:])
        tmp = knoten(tmp[0], tmp[2], tmp[1])
        g.add_knoten(tmp)

    fileKantenWeg = open("USA-road-d.NY.gr","r")
    fileKantenWeg.readline()

    for i in fileKantenWeg:
        tmp = i.split()[1:]
        tmp[0] = int(tmp[0])
        tmp[1] = int(tmp[1])
        tmp[2] = int(tmp[2])
        tmp = kante(tmp[0], tmp[1], tmp[2])
        g.add_kante(tmp)


    fileKantenZeit = open("USA-road-t.NY.gr","r")
    fileKantenZeit.readline()

    for i in fileKantenZeit:
        tmp = i.split()[1:]
        tmp[0] = int(tmp[0])
        tmp[1] = int(tmp[1])
        tmp[2] = int(tmp[2])
        for j in g.adj[tmp[0]][1:]:
            if j.knt1==tmp[1] or j.knt2==tmp[1]:
                j.add_distZeit(tmp[2])


# Kopie von https://gist.github.com/rochacbruno/2883505
# Haversine formula
# Author: Wayne Dyck        
def getDistanceBetweenPoints(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d



def naechsten_knoten_finden(lat, lon):
    mini = [10000000, 0]
    for i in range(1, g.get_laenge()):
        tmp = getDistanceBetweenPoints((lat, lon), (g.adj[i][0].lat, g.adj[i][0].lon))
        #print(tmp, i)
        if tmp < mini[0]:
            mini=[tmp, i]
    return mini[1]

def main(startk, endk):

    startk = startk[::-1]
    endk = endk[::-1]

    # naechste Knoten zu geg. Koord. finden
    start = naechsten_knoten_finden(startk[0], startk[1])
    end = naechsten_knoten_finden(endk[0], endk[1])

    # kuerzester Weg mit Dijkstra
    tmp = g.dijkstra_weg(start, end)
    distanz_weg = tmp[0][end]
    weg = get_weg(tmp[1], start, end)
    #print("Weg berechnet")

    # Koordinaten des Weges
    koor=[]
    for i in weg:
        koor.append([g.adj[i][0].lat, g.adj[i][0].lon])

    # Karte erstellen
    m = folium.Map()
    Draw(export=True, draw_options={'polyline': False, 'circlemarker': False, 'polygon': False, 'circle': False, 'rectangle': False}).add_to(m)

    # Start und Ziel Marker hinzufuegen
    folium.Marker(startk, tooltip="gewählter Start").add_to(m)
    folium.Marker(endk, tooltip="gewähltes Ziel").add_to(m)

    kw = {"prefix": "fa", "color": "blue", "icon": "arrow-down"}
    icon = folium.Icon(angle=0, **kw)
    folium.Marker(koor[0], icon=icon, tooltip="Start").add_to(m)
    kw = {"prefix": "fa", "color": "blue", "icon": "flag"}
    icon = folium.Icon(angle=0, **kw)
    folium.Marker(koor[-1], icon=icon, tooltip="Ziel").add_to(m)

    # naechsten Knoten mit gewaehltem Verbinden
    folium.PolyLine([startk, koor[0]], color="black", dash_array="10").add_to(m)
    folium.PolyLine([endk, koor[-1]], color="black", dash_array="10").add_to(m)

    # Weg als Linie hinzufuegen
    folium.PolyLine(locations=koor, color="red", weight=3, tooltip="kürzester Weg").add_to(m)

    # geringste Zeit mit Dijkstra
    tmp = g.dijkstra_zeit(start, end)
    distanz_zeit = tmp[0][end]
    weg = get_weg(tmp[1], start, end)
    #print("Zeit berechnet")

    # Koordinaten des Weges, Weg hinzufuegen
    koor=[]
    for i in weg:
        koor.append([g.adj[i][0].lat, g.adj[i][0].lon])
    
    folium.PolyLine(locations=koor, color="green", weight=3, tooltip="geringste Zeit").add_to(m)

    # Gauss
    folium.Marker((52.34371, 14.51508), tooltip="Carl-Friedrich-Gauß-Gymnasium").add_to(m)


    return m, distanz_weg, distanz_zeit



g = graph([[]])
datei_arbeit()

#print("fertig")




# Beispiel für Testungen

# a = knoten(0, 76.4345434, 56.634545)
# b = knoten(1, 76.4345434, 56.634545)
# print(b.num)

# k1 = kante(a, b, 5)
# k1.distanz()


#g.add_knoten(a)
#print(g.adj[1].num)


#print(naechsten_knoten_finden(41.093796, -73.524567))

#main(5, 645)