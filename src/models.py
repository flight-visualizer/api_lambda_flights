from typing import List, Optional
from pydantic import BaseModel

# -----------------INTERNAL-----------------
class DepartureModel(BaseModel):
    airport: str
    timezone: str
    iata: str
    icao: str
    terminal: str
    gate: str
    delay: int
    scheduled: str
    estimated: str
    actual: str
    estimated_runway: str
    actual_runway: str

# -----------------INTERNAL-----------------
class ArrivalModel(BaseModel):
    airport: str
    timezone: str
    iata: str
    icao: str
    terminal: str
    gate: str
    baggage: Optional[str]
    delay: Optional[int]
    scheduled: str
    estimated: str
    actual: str
    estimated_runway: str
    actual_runway: str

# ------------------------------------------

class InputModel(BaseModel):
    airline_iata: str
    flight_number: int

class ResponseModel(BaseModel):
    class PaginationModel(BaseModel):
        offset: int
        limit: int
        count: int
        total: int
    pagination: PaginationModel
    
    class FlightsInfoModel(BaseModel):
        flight_date: str
        flight_status: str

        departure: DepartureModel
        arrival: ArrivalModel
            
        class AirlineModel(BaseModel):
            name: str
            iata: str
            icao: str
        airline: AirlineModel
        
        class FlightModel(BaseModel):
            number: str
            iata: str
            icao: str
        flight: FlightModel
        
        class AircraftModel(BaseModel):
            registration: str
            iata: str
            icao: str
            icao24: str
        aircraft: Optional[AircraftModel]

        class LiveModel(BaseModel):     
            updated: str
            latitude: float
            longitude: float
            altitude: float
            direction: float
            speed_horizontal: float
            speed_vertical: float
            is_ground: bool
            icao: str
            icao24: str
        live: Optional[LiveModel]
        
    data: List[FlightsInfoModel]

class FlightsCacheModel(BaseModel):
    airline_iata: str
    flight_number: int
    flight_date: str
    flight_status: str
    departure: DepartureModel
    arrival: ArrivalModel

class ApiResponse(BaseModel):
    status_code: int
    message: str
    payload: Optional[FlightsCacheModel]