from typing import List, Optional
from pydantic import BaseModel

class InputModel(BaseModel):
    iata: str
    flight_number: int

class ResponseModel(BaseModel):
    class PaginationModel(BaseModel):
        offset: int
        limit: int
        count: int
        total: int
    pagination: PaginationModel
    
    class AirlineInfoModel(BaseModel):
        id: str
        fleet_average_age: str
        airline_id: str
        callsign: str
        hub_code: Optional[str]
        iata_code: str
        icao_code: str
        country_iso2: str
        date_founded: Optional[str]
        iata_prefix_accounting: Optional[str]
        airline_name: str
        country_name: str
        fleet_size: str
        status: str
        type: Optional[str]
    data: List[AirlineInfoModel]

class AirlineCacheModel(BaseModel):
    iata: str
    airline: str
