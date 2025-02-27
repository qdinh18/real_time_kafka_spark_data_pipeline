"""
KAFKA DATA PRODUCER FOR RANDOM USER PROFILES

This script performs three main actions:
1. Fetches random user data from an API
2. Structures the raw data into specific format
3. Streams formatted data to Kafka topic continuously for 5 minutes
"""
import uuid
import requests
import json
from kafka.producer import KafkaProducer
import time
import logging

def get_data():
    """
    Fetches single random user record from randomuser.me API
    
    Returns:
        dict|None: Dictionary containing user data if successful, 
                   None if request fails
    """
    response = requests.get("https://randomuser.me/api/")
    if response.status_code == 200:
        output = response.json()
        output = output['results'][0]  # Extract first user from results
    else:
        logging.error('An error occured while fetching data')
        output = None
    return output

def format_data(output):
    """
    Transforms raw API response into structured dictionary format
    
    Parameters:
        output (dict): Raw user data from get_data()
        
    Returns:
        dict: Structured data with selected fields. Returns empty dict 
              if input is None or formatting fails
    
    Note: 
        - Contains hardcoded field structure
        - Overwrites input 'output' parameter by calling get_data() internally
        - Address field combines multiple location components
    """
    output = get_data()  # Redundant call overwrites input parameter
    data = {}
    if output:
        # Extract specific fields from nested structure
        data['id'] = str(uuid.uuid4())
        data['first_name'] = output['name']['first']
        data['last_name'] = output['name']['last']
        data['gender'] = output['gender']
        data['address'] = f"{str(output['location']['street']['number'])} {output['location']['street']['name']}, " \
                        f"{output['location']['city']}, {output['location']['state']}, {output['location']['country']}"
        data['email'] = output['email']
        data['username'] = output['login']['username']
        data['dob'] = output['dob']['date']
        data['registered_date'] = output['registered']['date']
        data['phone'] = output['phone']
        data['picture'] = output['picture']['medium']
    else:
        logging.error('No data found')

    return data

def data_to_kafka():
    """
    Continuous data streaming to Kafka for 300 seconds (5 minutes)
    
    Creates Kafka producer that:
    - Connects to broker at 'broker:29092'
    - Has 5 second max blocking time for sends
    - Sends JSON-encoded data to 'users_profile' topic
    
    Loop runs for 5 minutes with basic error catching
    """
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    current_time = time.time()
    end_time = current_time + 300  # 5 minute runtime

    while time.time() < end_time:
        try:
            output = get_data()
            data = format_data(output)  # Gets data again via format_data's internal call

            # Send JSON-encoded data to Kafka topic
            producer.send('users_profile', json.dumps(data).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue