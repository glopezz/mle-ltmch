from enum import Enum

class ValidOpera(str, Enum):
    AEROLINEAS = "Aerolineas Argentinas"
    LATAM = "Grupo LATAM"
    SKY = "Sky Airline"
    COPA = "Copa Air"
    LATIN_AMERICAN_WINGS = "Latin American Wings"
    JETSMART = "JetSmart SPA"
    AEROCARDAL = "Aerocardal"
    AMERICAN_AIRLINES = "American Airlines"
    IBERIA = "Iberia"
    AIR_CANADA = "Air Canada"
    AIR_FRANCE = "Air France"
    ALITALIA = "Alitalia"
    AVIANCA = "Avianca"
    BRITISH_AIRWAYS = "British Airways"
    DELTA_AIR = "Delta Air"
    GOL = "Gol Trans"
    KLM = "K.L.M."
    LACSA = "Lacsa"
    OCEANAIR_LINHAS = "Oceanair Linhas Aereas"
    PLUS_ULTRA_LINHAS = "Plus Ultra Lineas Aereas"
    QANTAS_AIRWAYS = "Qantas Airways"
    UNITED_AIRLINES = "United Airlines"
    AMASZONAS = "Amaszonas"


class ValidTipoVuelo(str, Enum):
    I = "I"
    N = "N"