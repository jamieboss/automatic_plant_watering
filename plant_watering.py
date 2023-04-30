import enum
import os
from re import A
import pyfirmata, time, datetime, tkinter as tk, pandas as pd
from tkinter.font import Font, BOLD
from tkinter import ttk

# Read in plant data
PLANT_DATA = pd.read_excel('plant_types_and_water.xlsx')
PLANT_DATA = PLANT_DATA.fillna('None')
CS = list(PLANT_DATA[PLANT_DATA['Plant Type'] == "Cacti & Succulents"]['Name'])
FP = list(PLANT_DATA[PLANT_DATA['Plant Type'] == "Flowering Plants"]['Name'])
F = list(PLANT_DATA[PLANT_DATA['Plant Type'] == "Foliage Plants"]['Name'])
H = list(PLANT_DATA[PLANT_DATA['Plant Type'] == "Herbs"]['Name'])

# Calculate threshold values for each plant
water_levels = ['Minimum demand', 'Low demand', 'Medium demand', 'High demand', 'Very high demand', 'None']
THRESHOLD = [0.55, 0.4, 0.35, 0.3, 0.25, 0.35]

# GUI class for inputing plant information
class GUI():
    def __init__(self, master):
        self.master = master
        master.title("Input Plant Information")
        self.input = False
        
        # Save input data
        self.numPlants = 0
        self.numPlantsVar = tk.IntVar(self.master, 0)
        self.saveNames = []
        self.saveTypes = []
        self.saveDiams = []
        self.saveCurrMoisture = []
        self.saveLastWatered = []
        self.waterTank = 0
        self.waterTankVar = tk.StringVar()
        
        # Trace variables to enable start button
        self.numPlantsVar.trace('w', self.enable_button)
        self.waterTankVar.trace('w', self.enable_button)

        # Load in plants from file if it exists
        if os.path.exists("my_plants.txt"):
            with open("my_plants.txt", "r") as f:
                for line in f.readlines():
                    parts = line.strip("\n").split(",")
                    self.saveNames.append(parts[0])
                    self.saveTypes.append(parts[1])
                    self.saveDiams.append(parts[2])
                    self.saveCurrMoisture.append(parts[3])
                    self.saveLastWatered.append(datetime.datetime.strptime(parts[4], "%Y-%m-%d %H:%M:%S.%f"))
                    self.numPlants += 1

        self.numPlantsVar.set(self.numPlants)
        # Set window size
        self.master.geometry("1000x200")
        
        # Define fonts
        self.title = Font(self.master, size = 20, weight=BOLD)
        self.header = Font(self.master, size = 15, weight=BOLD)
        self.button = Font(self.master, underline = 1)
        
        # Display
        tk.Label(self.master, text="Plant Health Tracker", font = self.title).place(x=5, y=5)
        tk.Button(self.master, text="Add Plant", font = self.button, height = 2, width = 10, command = lambda: AddPlant(self, self.master), justify="left").place(x=5, y = 35)
        self.start = tk.Button(self.master, text="Start", font = self.button, height = 2, width = 10, command = self.end)
        self.start.place(x = 110, y = 35)
        self.start["state"] = "disabled"
        tk.Label(self.master, text="Enter Water Tank Capacity (oz): ", font = self.header).place(x = 550, y = 5)
        tk.Entry(self.master, textvariable=self.waterTankVar).place(x = 800, y = 5)
        tk.Button(self.master, text='Refill Water', font = self.button, command = self.refill_water).place(x = 800, y = 35)
        
        # Headers
        tk.Label(self.master, text="Name", anchor = "w", font = self.header).place(x=5, y=85)
        tk.Label(self.master, text="Type", anchor = "w", font = self.header).place(x=175, y=85)
        tk.Label(self.master, text="Pot Diameter", anchor = "w", font = self.header).place(x=325, y=85)
        tk.Label(self.master, text="Current Moisture", anchor = "w", font = self.header).place(x=475, y=85)
        tk.Label(self.master, text="Last Watered", anchor = "w", font = self.header).place(x=700, y=85)

        update_display(self)
    def saveToFile(self):
        with open("my_plants.txt", "w") as f:
            for i in range(self.numPlants):
                f.write(f"{self.saveNames[i]},{self.saveTypes[i]},{self.saveDiams[i]},{self.saveCurrMoisture[i]},{self.saveLastWatered[i]}\n")

    def enable_button(self, var, index, mode):
        if self.numPlants > 0 and len(self.waterTankVar.get()) > 0:
            self.start["state"] = "normal"
            
    def refill_water(self, _event=None):
        self.waterTank = int(self.waterTankVar.get())
    
    def end(self, _event=None):
        self.waterTank = int(self.waterTankVar.get())
        self.input = True
    
# Popup window to add a new plant
class AddPlant(tk.Toplevel):
    def __init__(self, mainapp, master = None):
        super().__init__(master = master)
        self.mainapp = mainapp
        self.title("Add Plant")
        
        # List of plant type options
        plant_category = ["Cacti & Succulents", "Flowering Plants", "Foliage", "Herbs"]
        plant_type = [CS, FP, F, H]
        
        # Input data
        tk.Label(self, text = "Name: ").grid(row = 0, column = 0)
        self.name = tk.Entry(self)
        self.name.grid(row = 0, column = 1)
        
        tk.Label(self, text = "Plant category: ").grid(row = 1, column = 0)
        self.plantC = ttk.Combobox(self, value=(plant_category))
        self.plantC.grid(row = 1, column = 1)
        
        def callback(eventObject):
            index = plant_category.index(self.plantC.get())
            self.plantT.config(values=plant_type[index])
            
        tk.Label(self, text = "Plant type: ").grid(row = 2, column = 0)
        self.plantT = ttk.Combobox(self)
        self.plantT.grid(row = 2, column = 1)
        self.plantT.bind('<Button-1>', callback)
        
        tk.Label(self, text = "Pot diameter: ").grid(row = 3, column = 0)
        self.diam = tk.Entry(self)
        self.diam.grid(row = 3, column = 1)
        
        # Save plant info and close window
        tk.Button(self, text="Enter", height = 2, width = 10, command = lambda: self.closeandsend()).grid(row = 4, columnspan = 2)
        
    def closeandsend(self):
        # Save plant information
        self.mainapp.numPlants = self.mainapp.numPlants + 1
        self.mainapp.numPlantsVar.set(self.mainapp.numPlants)
        self.mainapp.saveNames.append(self.name.get())
        self.mainapp.saveTypes.append(self.plantT.get())
        self.mainapp.saveDiams.append(self.diam.get())
        self.mainapp.saveCurrMoisture.append("0")
        self.mainapp.saveLastWatered.append(datetime.datetime.now())

        update_display(self.mainapp)
        
        self.mainapp.saveToFile()
        # Close window
        self.destroy()

# Window listing hardware issues
class IssuesList(tk.Toplevel):
    def __init__(self, mainapp, master = None):
        super().__init__(master = master)
        self.mainapp = mainapp
        self.title("Active Issues")
        self.geometry("300x300")

        self.issues_list = []

        tk.Label(self, text="Issues:", font=Font(self.master, size=20, weight=BOLD)).grid(row = 0, column = 0)
        
        if self.issues_list:
            tk.Label(self, text="\n".join(self.issues_list), anchor="w", font=Font(self.master, size=14), fg="#f00", justify="left").grid(row=1, column=0)
        else:
            tk.Label(self, text="None", anchor="w", font=Font(self.master, size=14), fg="#0f0", justify="left").grid(row=1, column=0)


# Update GUI display
def update_display(app):
    for i in range(0, app.numPlants):
        yCord = (i * 50) + 115
        tk.Label(app.master, text=app.saveNames[i], anchor = "w", wraplength=100).place(x=5, y=yCord)
        tk.Label(app.master, text=app.saveTypes[i], anchor = "w", wraplength=100).place(x=150, y=yCord)
        tk.Label(app.master, text=app.saveDiams[i], anchor = "w", wraplength=100).place(x=375, y=yCord)
        tk.Label(app.master, text=app.saveCurrMoisture[i] + '%', anchor = "w", wraplength=100).place(x=525, y=yCord)
        time_dif = datetime.datetime.now() - app.saveLastWatered[i]
        t = int(time_dif.total_seconds())
        days = int(t / (24 * 3600))
        t = t % (24 * 3600)
        hours = int(t / 3600)
        t = t % 3600
        minutes = int(t / 60)
        tk.Label(app.master, text=str(days) + ' days ' + str(hours) + ' hours ' + str(minutes) + ' minutes ', anchor = "w", wraplength=200).place(x=700, y=yCord)

# Update Issues GUI
def update_issues(app):
    if app.issues_list:
        tk.Label(app, text="\n".join(app.issues_list), anchor="w", font=Font(app.master, size=14), fg="#f00").grid(row=1, column=0)
    else:
        tk.Label(app, text="None", anchor="w", font=Font(app.master, size=14), fg="#0f0", justify="left").grid(row=1, column=0)


def read_and_update(main_window, i, moisture, time, issues_window, issues_list):
    if moisture:
        main_window.saveCurrMoisture[i] = str(int((moisture / 65) * 100))
    if time:
        main_window.saveLastWatered[i] = datetime.datetime.now()
    issues_window.issues_list = issues_list
    update_display(main_window)
    update_issues(issues_window)
    main_window.saveToFile()
        
# Connect to board
board = pyfirmata.Arduino('/dev/cu.usbmodem14201')
it = pyfirmata.util.Iterator(board)
it.start()

# Define pins
WATERPUMP = 3
moisture_sensor = [board.get_pin('a:0:i')]

# Water pumped per second
OZPERSECOND = 10

# Launch GUI
root = tk.Tk()
window = GUI(root)
issues_window = IssuesList(root)

def sensor_readings():
    if window.input:
        i = 0
        # Check moisture level
        moisture_level = moisture_sensor[i].read()
        
        # Water plant if moisture is too low
        update_time = False
        threshold = THRESHOLD[water_levels.index(PLANT_DATA[PLANT_DATA['Name'] == window.saveTypes[i]]['Water Level'].astype('str').values[0])]
        if moisture_level is not None and moisture_level > threshold and window.waterTank > 0:
            board.digital[WATERPUMP].write(1)
            time.sleep(int(window.saveDiams[i]))
            board.digital[WATERPUMP].write(0)
            
            # Update time and water tank
            update_time = True
            window.waterTank = window.waterTank - (float(window.saveDiams[i]) * OZPERSECOND)

        issues_list = []
        # Check for hardware errors 
        if moisture_level is None:
            issues_list.append('CHECK MOISTURE SENSOR')
        if window.waterTank < 0:
            issues_list.append('REFILL WATER TANK')
    
        # Write moisture level and time since last watering to UI
        read_and_update(window, i, moisture_level, update_time, issues_window, issues_list)
            
        # ADD: predict next watering time
        
    # Sleep for one minute
    root.after(60000, sensor_readings)

def on_closing():
    window.saveToFile()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

sensor_readings()
root.mainloop()