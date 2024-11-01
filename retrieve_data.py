import pandas as pd
import requests

# Define your Upstox API credentials
UPSTOX_API_KEY = '{YOUR API KEY}'
UPSTOX_API_SECRET = '{SECRET KEY}'
ACCESS_TOKEN = '{YOUR TOKEN}'  

def get_option_chain_data(instrument_key:str, expiry_date:str) -> pd.DataFrame:
    print("Starting function execution")
    
    #Calling of the api so that all the data should be fetch from the python program
    api_url = f"https://api.upstox.com/v2/option/chain"
    url = f"https://api.upstox.com/v2/option/contract"
    
    params={
        'instrument_key': f'{instrument_key}',
        'expiry_date': f'{expiry_date}'
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    #check wheter the url is correct or not
    try:
        response = requests.get(api_url,params=params ,headers=headers)
        response1 = requests.get(url,params=params ,headers=headers)
        response.raise_for_status()
        response1.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return pd.DataFrame(columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
    
    #Fetching all the data from the url to the variable in json format
    data = response.json()
    data1= response.json()['data']

    data_contract = response1.json()
    data1_contract= response1.json()['data']
    if 'data' not in data or not data['data']:
        print("Data is empty or not found in response.")
        return pd.DataFrame(columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
    

    #Creating the list so that data should be converted into dataframe 
    results = []
    for i in range(len(response.json()['data'])):
        strike_price = data1[i].get('strike_price')
    
    #Checking conditions for getting required output
        if data1_contract[i].get('instrument_type') == "PE":
            bid_ask_value = data1[i].get('put_options').get('market_data').get('bid_price')
            results.append((data1_contract[i].get('name'), strike_price, data1_contract[i].get('instrument_type'), bid_ask_value))
            
        elif data1_contract[i].get('instrument_type') == "CE":
            bid_ask_value = data1[i].get('call_options').get('market_data').get('ask_price')
            results.append((data1_contract[i].get('name'), strike_price, data1_contract[i].get('instrument_type'), bid_ask_value))
            
    #Creating the list into the dataframe 
    df = pd.DataFrame(results, columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
    return df


instrument_key=str(input("Enter the instrument_key of the stock: "))
expiry_date=str(input("Enter the expiry date of the stock: "))
df = get_option_chain_data(instrument_key, expiry_date)
print(df)
