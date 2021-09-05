import os
from typing import Optional
from models import InputModel, ResponseModel, FlightsCacheModel, ApiResponse
from services.DynamoService import DynamoService
from services.HttpClient import HttpClient

flights_db = DynamoService(
    table_name = 'cache_dynamo_flights', 
    model = FlightsCacheModel,
    ttl = 600
)

http_client = HttpClient(
    endpoint = 'http://api.aviationstack.com/v1/flights',
    api_key = os.getenv('API_KEY'),
    responseModel = ResponseModel
)

def get_realtime_flight_info(parameters: InputModel) -> Optional[FlightsCacheModel]:
    """
    """
    response = http_client.query(
        payload = parameters.dict()
    )

    if response.data:
        response = response.data[0]
        data = FlightsCacheModel(
            airline_iata = parameters.airline_iata,
            flight_number = parameters.flight_number,
            flight_date = response.flight_date,
            flight_status = response.flight_status,
            departure = response.departure,
            arrival = response.arrival
        )

        print(f'Successfully obtained flight data: {data}')
        return data
    else:
        print(f'Did not find any data with following parameters: {parameters}')
        return None

# GET /flights/{iata}/{flight_number}
def lambda_handler(event: dict, context) -> ApiResponse:
    """
    # Query DynamoDB cache to check for the iata, flight #
    # If present, return data
    # If NOT present, query aviation stack directly
    # Update cache with results
    # Return Results
    """
    try:
        parameters = InputModel(**event)
        print(f'Input Parameters: {parameters}')
    except:
        raise Exception(f'Incorrect input, event: {event} should be of type {InputModel}')

    cache_result = flights_db.get(parameters.dict())

    if cache_result:
        return ApiResponse(
            status_code = 200,
            message = 'Flight data retrieved from cache',
            payload = cache_result
        ).dict()
        
    else:
        data = get_realtime_flight_info(parameters)
        if data:
            flights_db.put(data)
            return ApiResponse(
                status_code = 200,
                message = 'Flight data retrieved from HTTP Query, written to cache',
                payload = data
            ).dict()
        else:
            return ApiResponse(
                status_code = 400,
                message = 'Flight data not found in cache or HTTP Query',
                payload = None
            ).dict()

# if __name__ == '__main__':
#     handler({'iata': 'AA'}, {})
