import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
base_url = "https://www.malkelapagading.com/directory?order="

# List of letters (A to Z) to utilize the pagination
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# List to store extracted information
data = []

# the loop for scraping
for letter in letters:

    url = base_url + letter
    
    response = requests.get(url)

    html_content = response.content
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    containers = soup.find_all("div", class_="col-md-4")
    
    # Loop through each container and extract information
    for container in containers:
        logo_img_element = container.find("img")
        tenant_name_element = container.find("h5")
        tenant_id_element = container.find("p")
        floor_element = container.find("h6")
        view_more_link_element = container.find("a")
        
        if view_more_link_element:  
            logo_img = logo_img_element["src"] if logo_img_element else "No logo found"
            tenant_name = tenant_name_element.text if tenant_name_element else "No tenant name found"
            tenant_id = tenant_id_element.text if tenant_id_element else "No tenant ID found"
            floor = floor_element.text if floor_element else "No floor found"
            view_more_link = view_more_link_element["href"] if view_more_link_element else "No view more link found"
            
            # Append extracted information to the list
            data.append({
                "Logo": logo_img,
                "Tenant Name": tenant_name,
                "Tenant ID": tenant_id,
                "Floor": floor,
                "View More Link": view_more_link
            })

    print(f"Scraping for letter {letter} completed.")

# Create a DataFrame from the list of extracted data
df = pd.DataFrame(data)
df.to_csv("tenants_data.csv", index=False)

#due to the dynamic website on each letter page, this code couldn't completely extract all 412 tenants