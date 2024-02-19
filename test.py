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
    def __init__(self, knt1, knt2, dist):
        self.knt1 = knt1
        self.knt2 = knt2
        self.dist = dist

    def distanz(self):
        print(self.dist)
    
    def get_alles(self):
        return self.knt1, self.knt2, self.dist

    def get_dist_knt(self, knt):
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


    def dijkstra(self, start):
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
            for i in range(1, len(self.adj[knt])):
                kante = self.adj[knt][i]
                pq.put((d+kante.dist, kante.get_dist_knt(knt), knt))
        
        return dist, vorg


def weg_ausgeben(vorg, start, end):
    weg=[]
    akt=end
    while akt!=start:
        weg.append(akt)
        akt=vorg[akt]
    weg.append(start)
    return weg[::-1]




a = knoten(0, 76.4345434, 56.634545)
b = knoten(1, 76.4345434, 56.634545)
print(b.num)

k1 = kante(a, b, 5)
k1.distanz()

g = graph([[]])
#g.add_knoten(a)
#print(g.adj[1].num)


n=264346

file1 = open("USA-road-d.NY.co/USA-road-d.NY.co","r")
print(file1.readline())

for i in range(n):
    tmp = file1.readline().split()[2:]
    tmp[0]=float(tmp[0][:3]+"."+tmp[0][3:])
    tmp[1]=float(tmp[1][:2]+"."+tmp[1][2:])
    tmp = knoten(i+1, tmp[0], tmp[1])
    g.add_knoten(tmp)

print(g.adj[10][0].get_alles())


file2 = open("USA-road-d.NY.gr/USA-road-d.NY.gr","r")
print(file2.readline())

for i in range(733844):
    tmp = file2.readline().split()[1:]
    tmp[0] = int(tmp[0])
    tmp[1] = int(tmp[1])
    tmp[2] = int(tmp[2])
    tmp = kante(tmp[0], tmp[1], tmp[2])
    g.add_kante(tmp)

print(g.adj[10][3].get_alles())




#print(g.dijkstra(1)[1][0:10])
x = g.dijkstra(38784)
z = weg_ausgeben(x[1], 38784, 243450)

print("berechnet")




m = folium.Map(location=(41, -73), zoom_start=10)
#fg = folium.FeatureGroup(name="Weg").add_to(m)


coor=[]
for i in z:
    #folium.Marker([g.adj[i][0].lon, g.adj[i][0].lat]).add_to(fg)
    coor.append([g.adj[i][0].lon, g.adj[i][0].lat])

folium.Marker(coor[0]).add_to(m)
folium.Marker(coor[-1]).add_to(m)

folium.PolyLine(
    locations=coor,
    color="#FF0000",
    weight=5,
    tooltip="From Boston to San Francisco",
).add_to(m)


folium.Marker([41, -73], popup='My Home').add_to(m)
#folium.LayerControl().add_to(m)

m.save("index.html")