import os
import time
import random
import math
import requests
import osmnx as ox
from shapely.geometry import Polygon, LineString
from dotenv import load_dotenv

load_dotenv()

API_KEY       = os.getenv('API_KEY')
REQUEST_DELAY = 0.1     
N_IMAGES      = 20 
MIN_YEAR      = 2024
SAVE_DIR      = "streetview_images_taguatinga"          

# polígono da UnB (x=lng, y=lat)
polygon_unb = [
    (-47.87164081758313, -15.775414438601896 ),  # lng, lat
    (-47.87688531806301, -15.754227788558826 ),
    (-47.87337525671921, -15.751673950845614 ),
    (-47.84880856258651, -15.770879616652774 ),
]

# Polígono: Centro de Taguatinga (Praça do Relógio e arredores)
polygon_taguatinga = [
    (-48.0594, -15.8340),  
    (-48.0507, -15.8317),  
    (-48.0531, -15.8260),  
    (-48.0618, -15.8284)   
]

# Polígono: Centro de Águas Claras (próximo à estação Arniqueiras)
polygon_aguas_claras = [
    (-48.0215, -15.8432),  
    (-48.0142, -15.8415),  
    (-48.0168, -15.8351),  
    (-48.0241, -15.8368)   
]

# Poligono: Rodoviária
polygon_rodoviaria = [
    (-47.8829, -15.7984),  
    (-47.8727, -15.7953),  
    (-47.8757, -15.7883),  
    (-47.8861, -15.7912)   
]

def random_point_on_roads(edges_list):
    line: LineString = random.choice(edges_list)
    return line, random.random()

def compute_heading_at(line: LineString, t: float, delta: float = 1e-4):
    length = line.length
    d0 = t * length
    if d0 + delta <= length:
        p1 = line.interpolate(d0)
        p2 = line.interpolate(d0 + delta)
    else:
        p1 = line.interpolate(d0)
        p2 = line.interpolate(d0 - delta)
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    angle_rad = math.atan2(dx, dy)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return angle_deg

def get_perpendicular_headings(heading: float):
    return [ (heading + 90) % 360, (heading - 90) % 360 ]

def get_streetview_metadata(lat: float, lng: float):
    url = "https://maps.googleapis.com/maps/api/streetview/metadata"
    params = { "location": f"{lat},{lng}", "key": API_KEY }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO METADATA] Falha na requisição: {e}")
        return None

def fetch_streetview(lat: float, lng: float, heading: int,
                     size: str = "640x640", fov: int = 90, pitch: int = 0):
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "location": f"{lat},{lng}",
        "heading":  heading,
        "fov":      fov,
        "pitch":    pitch,
        "size":     size,
        "key":      API_KEY
    }
    resp = requests.get(url, params=params, stream=True)
    fname = f"{lat:.6f}_{lng:.6f}_h{int(heading)}.jpg"
    if resp.status_code == 200:
        path = os.path.join(SAVE_DIR, fname)
        with open(path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        print(f"[OK]   {fname}")
    else:
        print(f"[ERRO] {fname} → HTTP {resp.status_code}")


if __name__ == "__main__":

    if API_KEY is None:
        raise ValueError("API_KEY not found")
    
    area_polygon = Polygon(polygon_taguatinga)
    os.makedirs(SAVE_DIR, exist_ok=True)

    #ox utiliza dados do open street map
    G = ox.graph_from_polygon(area_polygon, network_type="drive", simplify=True) #retorna um grafo contendo todas as ruas dentro do poligono
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)["geometry"].tolist() #grafo -> geoDataFrame -> lista (somente com arestas)
    
    images_found = 0
    attempts = 0
    while images_found < N_IMAGES:
        attempts += 1
        #Escolhe uma rua e um ponto aleatório nela
        line, t = random_point_on_roads(edges)
        pt = line.interpolate(t * line.length)
        lat, lng = pt.y, pt.x

        #Pede os metadados para verificar a data
        metadata = get_streetview_metadata(lat, lng)
        time.sleep(REQUEST_DELAY)

        if not metadata or metadata.get("status") != "OK":
            print(f"[SKIP] Tentativa {attempts}: Sem panorama em {lat:.6f},{lng:.6f}")
            continue

        #Verifica a data da imagem a partir dos metadados
        capture_date = metadata.get("date") # Formato "YYYY-MM"
        try:
            image_year = int(capture_date.split('-')[0])
            if image_year < MIN_YEAR:
                print(f"[SKIP] Tentativa {attempts}: Imagem muito antiga ({capture_date}) em {lat:.6f},{lng:.6f}")
                continue
        except (ValueError, TypeError, IndexError):
            print(f"[SKIP] Tentativa {attempts}: Não foi possível determinar a data em {lat:.6f},{lng:.6f}")
            continue

        #Se a data for aceitável, calcula os rumos
        street_h = compute_heading_at(line, t)
        perp_headings = get_perpendicular_headings(street_h)
        print(f"\n[FETCH] Local Válido {images_found + 1}/{N_IMAGES} encontrado em {lat:.6f},{lng:.6f} (Data: {capture_date})")
        #print(f"        Rumo da via ≈ {street_h:.1f}°, perpendiculares → {perp_headings}")

        #Baixa as duas imagens perpendiculares
        for h in perp_headings:
            fetch_streetview(lat, lng, heading=h)
            time.sleep(REQUEST_DELAY)
        
        images_found += 1

    print(f"\nFinalizado com {images_found} locais válidos")