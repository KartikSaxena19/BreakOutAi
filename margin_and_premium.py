import requests
import pandas as pd
from retrieve_data import get_option_chain_data     #-->Connecting the data from the other file to this file

ACCESS_TOKEN = '{YOUR ACCESS TOKEN}'

def get_margin_and_premium(df: pd.DataFrame,instrument_key:str, expiry_date:str, quantity:int, product:str) -> pd.DataFrame:
    premium_earned = []


    #Calling of the api's(contract, chain, margin)
    contract_url = f"https://api.upstox.com/v2/option/contract"
    param_contract = {
        'instrument_key': f'{instrument_key}',
        'expiry_date': f'{expiry_date}'
    }
    headers_contract = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    try:
        response_contract = requests.get(contract_url, params=param_contract, headers=headers_contract)
        response_contract.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching lot size for {instrument_key}: {e}")
        return 0
    
    data = response_contract.json()

    chain_url = f"https://api.upstox.com/v2/option/chain"
    param_chain = {
        'instrument_key': f'{instrument_key}',
        'expiry_date': f'{expiry_date}'
    }
    headers_chain = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    try:
        response_chain = requests.get(chain_url, params=param_chain, headers=headers_chain)
        response_chain.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching lot size for {instrument_key}: {e}")
        return 0  
    chain=response_chain.json()  
    chain_size=len(response_chain.json()['data'])


    for i in range(chain_size):
        #Premium = lot_size*bid/ask
        if data['data'][i].get('instrument_type') == "PE":
            premium_earned.append((data['data'][i].get('lot_size'))*(chain['data'][i].get('put_options').get('market_data').get('bid_price')))
        elif data['data'][i].get('instrument_type') == "CE":
            premium_earned.append((data['data'][i].get('lot_size'))*(chain['data'][i].get('call_options').get('market_data').get('ask_price')))

    #Creating extra column in the existing dataframe
    df['premium']=premium_earned


    #Data should be fetch from POST method
    margin_url = f"https://api.upstox.com/v2/charges/margin/"
    headers_margin = {
        "accept": "application/json",
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data_margin = {
        "instruments": [
        {
            "instrument_key": f'{instrument_key}',
            "quantity": f'{quantity}',
            "transaction_type": "SELL",
            "product": f'{product}'
        }
    ]
}

    try:
        margin_response = requests.post(margin_url, json=data_margin, headers=headers_margin)
        margin_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching margin data:", e)


    margin_data = margin_response.json()
    
    margins_list = margin_data.get('data', {}).get('margins', [])
    if margins_list and isinstance(margins_list, list):
        df['margin'] = margins_list[0].get('total_margin', 0)
    else:
        df['margin'] = 0
        
        

    return df

#Is is the way that how the file is connected by the __main__
if __name__ == "__main__":
    instrument_key = input("Enter the instrument_key of the stock: ")
    expiry_date = input("Enter the expiry date of the stock: ")
    df = get_option_chain_data(instrument_key, expiry_date)  
    quantity=int(input("Enter the quantity of the margin: "))
    product=str(input("Enter the product type: "))
    final_result = get_margin_and_premium(df,instrument_key,expiry_date,quantity,product)
    print(final_result)
