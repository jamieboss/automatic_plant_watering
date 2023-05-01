import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

PLANT_DATA = pd.read_excel('plant_types_and_water.xlsx')
PLANT_DATA = PLANT_DATA.fillna('None')

water_levels = ['Minimum demand', 'Low demand', 'Medium demand', 'High demand', 'Very high demand', 'None']
THRESHOLD = [0.55, 0.4, 0.35, 0.3, 0.25, 0.35]

PLANT_DATA = PLANT_DATA.replace({ water_levels[i] : THRESHOLD[i] for i in range(len(water_levels))} | { "Cacti & Succulents": 0, "Flowering Plants": 1, "Foliage Plants": 2, "Herbs": 3})

PLANT_DATA = PLANT_DATA[["Plant Type", "Water Level"]]
PLANT_DATA["Last Watering"] = np.random.randint(1, 7, PLANT_DATA.shape[0]) * np.random.rand(PLANT_DATA.shape[0])

kmeans = KMeans(2, random_state=0, n_init="auto").fit(PLANT_DATA.values)
labels = kmeans.labels_

PLANT_DATA["Labels"] = labels

label1 = PLANT_DATA[PLANT_DATA["Labels"] == 1]
label0 = PLANT_DATA[PLANT_DATA["Labels"] == 0]

ax = plt.axes(projection='3d')

ax.scatter(label1["Plant Type"], label1["Water Level"], label1["Last Watering"], c="blue", label="Needs water")
ax.scatter(label0["Plant Type"], label0["Water Level"], label0["Last Watering"], c="red", label = "Has enough water")
ax.set_xlabel("Plant Type")
ax.set_ylabel("Desired Moisture Level")
ax.set_zlabel("Last Watering (Days)")
ax.legend()
plt.show()
