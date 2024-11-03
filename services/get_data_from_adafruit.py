import requests
import pandas as pd
from utils.constant import *

# Get historical data from adafruit
def connect_to_adafruit(AIO_FEED_ID):  
    AIO_USERNAME = AIO_USERNAME_ADAFRUIT # Username
    AIO_KEY = AIO_KEY_ADAFRUIT# Key

    response = requests.get(f'https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{AIO_FEED_ID}/data',
                        auth=(AIO_USERNAME, AIO_KEY))
    
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
        return ""
        