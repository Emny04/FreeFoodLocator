import requests
import pandas as pd  # For creating and handling tables
import creds

# Set the API key directly in the code
api_key = creds.Api_Key # Replace with your actual API key
base_url = "https://api.perplexity.ai/chat/completions"  # API endpoint URL

# Set up the HTTP request headers with authorization and content type
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Read the content from content.txt
with open('content.txt', 'r') as file:
    food_type = file.read().strip()  # Read and strip any extra whitespace

# Append the search query for events that provide the specified type of food
query = f"Find events that provide food:"

# The request body containing the model and messages to send
data = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {"role": "user", "content": query}
    ]
}

# Send the POST request to the API and get the response
response = requests.post(base_url, headers=headers, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    response_data = response.json()
    
    # Extract the content from the response
    event_info = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    # Process the event_info to extract events (assuming it is in a text format that can be parsed)
    events = event_info.split('\n')  # Split events by newline, adjust if needed

    # Create a DataFrame to organize events into a table
    df = pd.DataFrame(events, columns=['Event Description'])

    # Save the table to a CSV file
    df.to_csv('events_with_food.csv', index=False)

    print("Table of events providing the specified type of food has been written to 'events_with_food.csv'.")
else:
    print(f"Error: {response.status_code} - {response.text}")
