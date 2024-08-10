# Import required libraries
import pandas as pd

# Import data
client_details = pd.read_csv('data/client_details.csv')
subscription_records = pd.read_csv('data/subscription_records.csv', parse_dates = ['start_date','end_date'])
economic_indicators = pd.read_csv('data/economic_indicators.csv', parse_dates = ['start_date','end_date'])

##### Question 1 - How many total Fintech and Crypto clients does the company have?  ##### 
# Define a function that returns 1 if the input is either 'Fintech' or 'Crypto', otherwise returning 0
def is_fintech_or_crypto(x):
    if x in ['Fintech','Crypto']:
        return 1
    else:
        return 0
    
# Loop through the 'industry' column in client_details and increment the total_fintech_crypto_clients counter for every Fintech or Crpyto client
total_fintech_crypto_clients = 0
for industry in client_details['industry']:
    total_fintech_crypto_clients += is_fintech_or_crypto(industry)

# Alternate approach 1 - Apply the custom function directly to the 'industry' column to calculate the total number of Fintech and Crypto clients
# total_fintech_crypto_clients = client_details['industry'].apply(is_fintech_or_crypto).sum()
    
# Alternate approach 2 - Use a lambda function to calculate the total number of Fintech and Crypto clients
# total_fintech_crypto_clients = client_details['industry'].apply(lambda x: x in ['Fintech','Crypto']).sum()
    
  
##### Question 2 - Which industry has the highest renewal rate?   ##### 
# Merge client details with subscription records
subscriptions = pd.merge(subscription_records, client_details, on = 'client_id', how = 'left')

# Group by industry and calculate renewal rate
industry_renewal_rates = subscriptions.groupby('industry')['renewed'].mean()

# Find the industry with the highest renewal rate, save as variable 'top_industry'
top_industry = industry_renewal_rates.sort_values(ascending = False).index[0]


##### Question 3 -For clients that renewed their subscriptions, what was the average inflation rate when their subscriptions were renewed? #####
# Merge subscription records with economic indicators to get the inflation rate at the subscription end date (i.e., renewal time)
subscriptions_with_inflation = pd.merge_asof(subscription_records.sort_values(by='end_date'), 
                                             economic_indicators, 
                                             left_on='end_date', 
                                             right_on='start_date', 
                                             direction='backward')

# Calculate the average inflation rate for renewed subscriptions
average_inflation_for_renewals = subscriptions_with_inflation[subscriptions_with_inflation['renewed'] == True].inflation_rate.mean()
