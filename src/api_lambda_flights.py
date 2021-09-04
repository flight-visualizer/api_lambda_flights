import os
import requests
from typing import List
from models import InputModel, ResponseModel, FlightsCacheModel
from services.DynamoService import DynamoService
# from services.


API_KEY = os.getenv('API_KEY')

flights = DynamoService(
    table_name = 'cache_dynamo_flights', 
    model = FlightsCacheModel
)

# requestService = 

def get_realtime_flight_info(parameters: InputModel) -> dict:
    """
    """

    try:
        print(f'Attempting to retrieve flight data with parameters {parameters} ...')
        response = requests.get(
            'http://api.aviationstack.com/v1/flights', 
            params={
                'airline_iata': parameters.iata,
                'flight_number': parameters.flight_number,
                'access_key': API_KEY
            }
        )
        print(f'Response received... status: {response.status_code}')

        response = ResponseModel(**response.json())

    except:
        print('Error querying aviation stack...')
        raise

    
    db_records: List[FlightsCacheModel] = []
    for record in response.data:
        db_records.append(
            AirlineCacheModel(
                iata=record.iata_code,
                airline=record.airline_name
            )
        )
    return db_records

    #TODO: Marshel response into data model for validation

    response = r.json()
    print(response["pagination"])
    print(response["data"][0])

if __name__ == '__main__':
    handler({'iata': 'AA'}, {})


# GET /flights/{iata}/{flight_number}
def lambda_handler(event: dict, context) -> dict:
    
    try:
        parameters = InputModel(**event)
        print(f'Input Parameters: {parameters}')
    except:
        raise Exception(f'Incorrect input, event: {event} should be of type {InputModel}')

    get_realtime_flight_info(parameters)

    
    # flight_number = event['flight_number'] #'5677'
    # airline_search_string = event['airline_search_string']

    # iata = get_airline_iata(airline_search_string)
    

    # return response['data']
    
