from math import radians, sin, cos, sqrt, atan2
import logging

logger = logging.getLogger(__name__)


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    
    a = sin(delta_phi / 2) ** 2 + \
        cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distancia = R * c
    
    logger.debug(f"Distância calculada: {distancia:.2f}m entre ({lat1},{lon1}) e ({lat2},{lon2})")
    
    return distancia


def validar_coordenadas_brasilia(latitude, longitude):
    return (-16.0 <= latitude <= -15.5) and (-48.3 <= longitude <= -47.3)


def formatar_distancia(metros):
    if metros >= 1000:
        return f"{metros/1000:.1f} km"
    else:
        return f"{metros:.0f} m"


def calcular_area_bounding_box(lat_min, lon_min, lat_max, lon_max):
    lat_centro = (lat_min + lat_max) / 2
    dist_horizontal = calcular_distancia_haversine(lat_centro, lon_min, lat_centro, lon_max)
    
    lon_centro = (lon_min + lon_max) / 2
    dist_vertical = calcular_distancia_haversine(lat_min, lon_centro, lat_max, lon_centro)
    
    area_km2 = (dist_horizontal * dist_vertical) / 1_000_000
    
    return area_km2