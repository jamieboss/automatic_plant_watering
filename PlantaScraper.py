import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Get main Planta page
url = 'https://getplanta.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize array
plant_info = []

plant_types = ['Cacti & Succulents', 'Herbs', 'Foliage Plants', 'Flowering Plants']
for plant_type in plant_types:
    # Get plant type page
    plant_type_page = soup.find(text = plant_type).parent.parent['href']
    response2 = requests.get(url+str(plant_type_page))
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    
    # Get water level for each plant
    plants = soup2.findAll('a', {'class': 'plant-listed-link'})
    for plant in plants:
        plant_page = requests.get(url+str(plant['href']))
        plant_soup = BeautifulSoup(plant_page.text, 'html.parser')
        plant_name = plant_soup.title.text
        plant_name = plant_name[:plant_name.find('|')].strip()
        water_level = plant_soup.find(text = 'Watering need')
        if water_level:
            water_level = water_level.parent.parent.text
            water_level = water_level[water_level.find(':')+1:].strip()
        else:
            print(plant_name)
            water_level = 'None'
        
        # Store info
        plant_info.append([plant_name, plant_type, water_level])
        
# Convert to dataframe
df = pd.DataFrame(np.array(plant_info), columns=['Name', 'Plant Type', 'Water Level'])

# Save as excel
df.to_excel('plant_types_and_water.xlsx')
        
    