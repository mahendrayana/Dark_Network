import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

base_url = "https://dark-netflix.fandom.com/wiki/Category:Characters"

response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

character_containers = soup.find_all("div", class_="category-page__member-left")

character_data = []

# Step 1: Extract Character Name, Wiki Link, and Image Source
for container in character_containers:
    anchor = container.find("a")
    
    if anchor:
        image_src = anchor.find("img")["data-src"]
        wiki_link = urljoin(base_url, anchor["href"])
        
        character_name = wiki_link.split("/")[-1]  # Extract the character name from the URL
        
        character_data.append({"Character Name": character_name, "Image Source": image_src, "Wiki Link": wiki_link})

# Step 2: Fill in Family Relations
for character in character_data:
    character_response = requests.get(character["Wiki Link"])
    character_soup = BeautifulSoup(character_response.content, "html.parser")
    
    family_section = character_soup.find("div", {"data-source": "Family"})
    
    if family_section:
        family_relations = []
        for item in family_section.find_all("p"):
            family_relations.append(item.get_text())
        
        family_relations = " ".join(family_relations)
        character["Family Relations"] = family_relations
    else:
        character["Family Relations"] = "N/A"

# Create DataFrame from the character data
df = pd.DataFrame(character_data)

df.info