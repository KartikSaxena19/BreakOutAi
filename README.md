# BreakOutAi
It is the Ai tool which constantly monitors stocks poised for significant upside moves, ensuring you don't miss out on lucrative opportunities.
For more detail check the official website of the [Breakoutai](https://breakoutai.tech/) .

## Table of Content
- [Libraries](#Libraries)
- [Retrieve Data](#Retrieve-Data)
- [Margin and Premium](#Margin-and-Premium)


## Libraries
### Run the following commands in the command promt or vs code 
- Install the request library to request the access of broker api.
```bash
pip install request
```
- Insall the pandas library so that the dataframe should be created by this.
```bash
pip install pandas
```
## Retrieve Data
- This function is used to retrieve the data from the stock market api.
    - for eg:- upstox, zerodha etc.
    
- By the help of this function we are able to extract the data in the form of dataframe and the output comes in the form of:-
    - Instrument_key, Strike_Price, Side, Bid/Ask
  
- This function check for PE and CE for each strike price and calculate the data accordingly.
    
    - IF `Instrument_key` == PE
        - Than the data calculated with respect to PE than it will select the highest bid price from the put function.
    - If `Instrument_key` == CE
        - Than the data calcualted with respect to CE than it will select the highest ask price from the call function.

## Margin and Premium
- This function is used to calculate the premium and find the margin of the stock.
  
- Premium should be calculated with the api.
    - `Premium` = `lot_size`*`bid/ask`     

- Can calulate margin for `SELL` or `BUY` as per you wish
