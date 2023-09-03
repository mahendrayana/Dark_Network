import pandas as pd
import re
import urllib.parse

df = pd.read_csv('C:\\Users\\Putu Mahendrayana\\Documents\\Dark_Network\\Data\\RAW.csv')

# Function to extract character name from the link
def extract_character_name(link):
    match = re.search(r'/wiki/([^/]+)', link)
    if match:
        return match.group(1).replace('_', ' ')
    return None

# Apply the function to the 'link' column and create a new 'Character Name' column
df['Character Name'] = df['Wiki Link'].apply(extract_character_name)

# Assign NodeIDs to each character row
df['NodeID'] = range(1, len(df) + 1)

# Function to decode URL-encoded characters and replace underscores with spaces
def decode_and_clean_name(link):
    decoded_name = urllib.parse.unquote(link)
    cleaned_name = decoded_name.replace('_', ' ')
    return cleaned_name

# Apply the function to the 'Character Name' column
df['Character Name'] = df['Character Name'].apply(decode_and_clean_name)

# Function to modify the family relations text
def modify_family_relations(relations):
    if pd.isna(relations):
        return relations  # Return NA value as is
    
    modified_relations = []
    segments = re.split(r'\)(?=\S)', relations)
    
    for segment in segments:
        parts = segment.split('(')
        if len(parts) == 2:
            name = parts[0].strip().replace('†', '')  # Remove † symbol
            role = parts[1].strip()
            modified_relations.append(f"{name}_{role}")  # Remove the space after underscore
        else:
            modified_relations.append(segment.strip())
    return ','.join(modified_relations)
# Apply the function to the 'Family Relations' column
df['Modified Family Relations'] = df['Family Relations'].apply(modify_family_relations)

# Create an empty list to store rows
rows = []

# Iterate through each row
for index, row in df.iterrows():
    source = row['Character Name']
    modified_relations = row['Modified Family Relations']
    
    # Skip processing if modified_relations is NA
    if pd.isna(modified_relations):
        continue
    
    target_relations = modified_relations.split(',')
    
    # Iterate through each relation in the 'Modified Family Relations'
    for relation in target_relations:
        # Split the relation by underscore (_)
        relation_parts = relation.split('_')
        
        # Check if the relation is in the correct format
        if len(relation_parts) == 2:
            target, relation_type = relation_parts
            rows.append([source, target, relation_type])

# Create a new DataFrame with the extracted relationships
new_df = pd.DataFrame(rows, columns=['Source Node', 'Target Node', 'Relation'])


new_df['Relation'] = new_df['Relation'].str.replace(')', '')

# Split the 'Relation' column and create new rows
new_rows = []

for index, row in new_df.iterrows():
    source = row['Source Node']
    target = row['Target Node']
    relations = row['Relation'].split('/')
    
    for relation in relations:
        new_rows.append([source, target, relation.strip()])

# Create a new DataFrame with the split relations
df_final = pd.DataFrame(new_rows, columns=['Source Node', 'Target Node', 'Relation'])

df_final.to_csv('dark_output.csv', index=False)


