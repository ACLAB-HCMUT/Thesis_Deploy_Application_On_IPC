import requests
import pandas as pd
from constant import *

# Get historical data from adafruit
def connect_to_adafruit(AIO_FEED_ID):  
    AIO_USERNAME = ADAFRUIT_AIO_USERNAME # Username
    AIO_KEY = ADAFRUIT_AIO_KEY# Key

    response = requests.get(f'https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{AIO_FEED_ID}/data?limit=1',
                        auth=(AIO_USERNAME, AIO_KEY))
    print(response)
    
    return response

# Analyst data from adafruit
def get_data_from_adafruit(AIO_FEED_ID):
    # Get data from sensor
    response_connect_adafruit = connect_to_adafruit(AIO_FEED_ID)

    if response_connect_adafruit.status_code == 200:
        data = response_connect_adafruit.json()

        result_data = pd.DataFrame(data)[["value", "created_at"]]

        return result_data
    
    else:
        return "Error"
    
print(get_data_from_adafruit("sensors"))
        