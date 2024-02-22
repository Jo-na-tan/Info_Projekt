from queue import PriorityQueue
import folium


class knoten:
    def __init__(self, num, lat, lon):
        self.num = num
        self.lat = lat
        self.lon = lon

    def get_alles(self):
        return self.num, self.lat, self.lon

class kante:
    def __init__(self, knt1, knt2, distWeg):
        self.knt1 = knt1
        self.knt2 = knt2
        self.distWeg = distWeg

    def add_distZeit(self, distZeit):
        self.distZeit = distZeit
    
    def get_alles(self):
        return self.knt1, self.knt2, self.distWeg

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
        #self.adj[kante.knt2].append(kante)


    def dijkstra_weg(self, start, end):
        n = self.get_laenge()
        dist = [10000000]*n
        vorg = [0]*n
        pq = PriorityQueue()
        pq.put((0, start, start))
        
        while pq.qsize()>0:
            akt = pq.get()
            #print(akt)
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
            #print(akt)
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
    fileKoord = open("USA-road-d.FLA.co","r")
    fileKoord.readline()

    for i in fileKoord:
        tmp = i.split()[1:]
        tmp[1]=float(tmp[1][:3]+"."+tmp[1][3:])
        tmp[2]=float(tmp[2][:2]+"."+tmp[2][2:])
        tmp = knoten(tmp[0], tmp[2], tmp[1])
        g.add_knoten(tmp)

    #print(g.adj[10][0].get_alles())

    fileKantenWeg = open("USA-road-d.FLA.gr","r")
    fileKantenWeg.readline()

    for i in fileKantenWeg:
        tmp = i.split()[1:]
        tmp[0] = int(tmp[0])
        tmp[1] = int(tmp[1])
        tmp[2] = int(tmp[2])
        tmp = kante(tmp[0], tmp[1], tmp[2])
        g.add_kante(tmp)


    fileKantenZeit = open("USA-road-t.FLA.gr","r")
    fileKantenZeit.readline()

    for i in fileKantenZeit:
        tmp = i.split()[1:]
        tmp[0] = int(tmp[0])
        tmp[1] = int(tmp[1])
        tmp[2] = int(tmp[2])
        for j in g.adj[tmp[0]][1:]:
            if j.knt1==tmp[1] or j.knt2==tmp[1]:
                j.add_distZeit(tmp[2])

def main(start, end):
    tmp = g.dijkstra_weg(start, end)
    distanz_weg = tmp[0][end]
    tmp = get_weg(tmp[1], start, end)

    koor=[]
    for i in tmp:
        koor.append([g.adj[i][0].lat, g.adj[i][0].lon])

    m = folium.Map(location=(41, -73), zoom_start=8)

    folium.Marker(koor[0]).add_to(m)
    folium.Marker(koor[-1]).add_to(m)

    folium.PolyLine(locations=koor, color="red", weight=3, tooltip="kürzester Weg").add_to(m)



    tmp = g.dijkstra_zeit(start, end)
    distanz_zeit = tmp[0][end]
    tmp = get_weg(tmp[1], start, end)

    koor=[]
    for i in tmp:
        koor.append([g.adj[i][0].lat, g.adj[i][0].lon])
    
    folium.PolyLine(locations=koor, color="green", weight=3, tooltip="geringste Zeit").add_to(m)

    
    print("berechnet")
    print(g.adj[1][0].lat)

    return m, distanz_weg




g = graph([[]])

datei_arbeit()












# a = knoten(0, 76.4345434, 56.634545)
# b = knoten(1, 76.4345434, 56.634545)
# print(b.num)

# k1 = kante(a, b, 5)
# k1.distanz()


#g.add_knoten(a)
#print(g.adj[1].num)

# print(g.adj[10][3].get_alles())




#print(g.dijkstra(1)[1][0:10])
# x = g.dijkstra(38784)
# z = get_weg(x[1], 38784, 243450)

# print("berechnet")



    


# m = folium.Map(location=(41, -73), zoom_start=10)

#fg = folium.FeatureGroup(name="Weg").add_to(m)


# coor=[]
# for i in z:
#     #folium.Marker([g.adj[i][0].lon, g.adj[i][0].lat]).add_to(fg)
#     coor.append([g.adj[i][0].lon, g.adj[i][0].lat])

# folium.Marker(coor[0]).add_to(m)
# folium.Marker(coor[-1]).add_to(m)

# folium.PolyLine(
#     locations=coor,
#     color="#FF0000",
#     weight=5,
#     tooltip="From Boston to San Francisco",
# ).add_to(m)


# folium.Marker([41, -73], popup='My Home').add_to(m)
#folium.LayerControl().add_to(m)

#m.save("index.html")


# import streamlit as st
# from streamlit_folium import st_folium
# st_data = st_folium(m, width=725)