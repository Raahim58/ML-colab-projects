import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Define the target URL
url = 'https://www.olx.com.pk/items/q-lenovo-laptop'

# Step 1: Fetch the main page content
response = requests.get(url)
print("Status Code:", response.status_code)

# Initialize a list to hold laptop details
laptop_details = []

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 2: Find all listings
    listings = soup.find_all('div', class_='IKo3_')  # Adjust this class based on the current HTML structure

    # Step 3: Loop through each listing to get the sub-link
    for listing in listings:
        link = listing.find('a')['href']
        full_link = 'https://www.olx.com.pk' + link if link.startswith('/') else link
        
        # Step 4: Fetch the sub-link content
        sub_response = requests.get(full_link)
        if sub_response.status_code == 200:
            sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
            
            # Step 5: Extract specific fields from the sub-link page using regex
            try:
                # Get the text content of the entire sub-page
                page_text = sub_soup.get_text()

                # Use regex to find the Brand, Name, and Price
                brand_match = re.search(r'Brand:\s*(.*)', page_text)
                name_match = re.search(r'Name:\s*(.*)', page_text)
                price_match = re.search(r'Price:\s*([0-9,]+)', page_text)

                # Extract the matched groups or set as 'N/A' if not found
                brand = brand_match.group(1).strip() if brand_match else 'N/A'
                name = name_match.group(1).strip() if name_match else 'N/A'
                price = price_match.group(1).strip() if price_match else 'N/A'
                
                # Append the extracted details to the list
                laptop_details.append([brand, name, price])
            except Exception as e:
                print("Error while extracting fields for:", full_link, "\nError:", e)
    
    # Step 6: Store the data in a DataFrame and save it to Excel
    df = pd.DataFrame(laptop_details, columns=['Brand', 'Name', 'Price'])
    
    df.to_excel('lenovo_laptops_olx_test.xlsx', index=False)
    print("Data saved to lenovo_laptops_olx_test.xlsx")
else:
    print("Failed to retrieve the main page.")

