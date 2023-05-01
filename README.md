# Automatic Plant Watering and Prediction System

#### Authors: Jamie Bossenbroek and Aditya Vadlamani

## Hardware Requirements

The following components are needed:

<li> Arduino Uno
<li> HiLetgo Soil Moisture Sensor and Module
<li> Mini Water Pump, PVC tubing, and Water Tank

## Software Requirements

All of the necessary software packages can be installed via the `requirements.txt` file using the following command:

```
pip install -r requirements.txt
```

## Running Plant Watering System

The following are steps in order to run the source code

1. If there is no `plant_types_and_water.xlsx` file, then execute the web scraper by running

```
python PlantaScraper.py
```

2. Connec the Arduino Uno to the computer running the program
3. Run the following to initialize the system

```
python plant_watering.py
```

Once the application is up and running, you can specify the water available in the water tank as well as add your plant information. Once both are done, the program can be started.

## Running the Plant Watering Predictor

To run the Proof of Concept for the Plant Watering Predictor, execute

```
python WateringPrediction.py
```
