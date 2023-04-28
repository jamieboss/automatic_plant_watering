import pyfirmata, time, tkinter as tk
from tkinter.font import Font, BOLD

# Connect to board
#board = pyfirmata.Arduino('/dev/cu.usbmodem14401')
#it = pyfirmata.util.Iterator(board)
#it.start()

#WATERPUMP = 3
#moisture_sensor = board.get_pin('a:0:i')
#threshold = 0.4
#WATERTIME = 2.0

# GUI class for inputing plant information
class GUI():
    def __init__(self, master):
        self.master = master
        master.title("Input Plant Information")
        
        # Save input data
        self.numPlants = 0
        self.saveNames = []
        self.saveTypes = []
        self.saveDiam = []
        
        # Set window size
        self.master.geometry("500x200")
        
        # Define fonts
        self.header = Font(self.master, size = 15, weight=BOLD)
        self.button = Font(self.master, underline = 1)
        
        # Display
        tk.Label(self.master, text="Input Plant Information", font = self.header).place(x=5, y=5)
        tk.Button(self.master, text="Add Plant", font = self.button, height = 2, width = 10, command = lambda: AddPlant(self, self.master)).place(x=5, y = 35)
        
    
# Popup window to add a new plant
class AddPlant(tk.Toplevel):
    def __init__(self, mainapp, master = None):
        super().__init__(master = master)
        self.mainapp = mainapp
        self.title("Add Plant")
        
        self.plant_category = tk.StringVar(self)
        self.plant_category.set("Select Category")
        
        # List of plant type options
        plant_category = ["Cacti & Succulents", "Flowering Plants", "Foliage", "Herbs"]
        
        # Input data
        tk.Label(self, text = "Name: ").grid(row = 0, column = 0)
        self.name = tk.Entry(self)
        self.name.grid(row = 0, column = 1)
        tk.Label(self, text = "Plant category: ").grid(row = 1, column = 0)
        tk.OptionMenu(self, self.plant_category, *plant_category).grid(row = 1, column = 1)
        tk.Label(self, text = "Pot diameter: ").grid(row = 2, column = 0)
        self.diam = tk.Entry(self)
        self.diam.grid(row = 2, column = 1)
        
        # Save plant info and close window
        tk.Button(self, text="Enter", height = 2, width = 10, command = lambda: self.closeandsend()).grid(row = 3, columnspan = 2)
        
    def closeandsend(self):
        # Save plant information
        self.mainapp.numPlants = self.mainapp.numPlants + 1
        self.mainapp.saveNames.append(self.name.get())
        self.mainapp.saveTypes.append(self.plant_category.get())
        self.mainapp.saveDiam.append(self.diam.get())
        
        # Display plant information
        yCord = (self.mainapp.numPlants * 30) + 50
        tk.Label(self.mainapp.master, text=self.name.get()).place(x=5, y=yCord)
        tk.Label(self.mainapp.master, text=self.plant_category.get()).place(x=100, y=yCord)
        tk.Label(self.mainapp.master, text=self.diam.get()).place(x=250, y=yCord)
        
        # Close window
        self.destroy()
            
            
        
# Launch GUI
root = tk.Tk()
window = GUI(root)
root.mainloop()

# FIX: While loop doesn't run until GUI closes
#CHANGE?: Input all plant information first, then start user display
while False:
    # Check moisture level
    moisture_level = moisture_sensor.read()
    print(moisture_level)
    # 0 (connected) - 0.66 (disconnected)
    
    # Water plant if moisture is too low
    # ADD: get threshold and water time from AI or something
    if moisture_level is not None and moisture_level > threshold:
        board.digital[WATERPUMP].write(1)
        time.sleep(WATERTIME)
        board.digital[WATERPUMP].write(0)
        
    # ADD: write moisture level and time since last watering to UI
    # ADD: check for hardware errors 
    # ADD: predict next watering time
    
    time.sleep(60.0) # Sleep for one minute