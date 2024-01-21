import tkinter as tk # for GUI
import customtkinter
import numpy as np 
import Dec_Tree as DT
import Prediction
import Scatter
from tkinter import ttk


#GUI - Login page
class MainApplication: 
    def __init__(self, root):
        self.root = root
        self.root.title("Students Performance")
        self.root.geometry("350x200")
        self.current_frame = None
        self.show_login_page()

    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Login_Page(self.root, self)

    def show_main_window(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Main_Window(self.root, self)

    def show_predictor(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Predictor(self.root, self)

    def show_decision_tree(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Decision_Tree(self.root, self)

    def show_scattergraph(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Scattergraph(self.root, self)


class Controller:
    def show_main_window(self):
        print("Logged in successfully")

class Login_Page(tk.Frame): 
    def __init__(self, master, controller):
        super().__init__(master)
        self.title=("Login Page")
        self.controller = controller
        self.grid()
        self.username_var = tk.StringVar() 
        self.password_var = tk.StringVar()

#using labels with grid positioning method
        tk.Label(self, text="Username: ").grid(row=0)
        username_entry = tk.Entry(self, textvariable=self.username_var)
        username_entry.grid(row=0, column=1)

        tk.Label(self, text="Password: ").grid(row=1)
        password_entry = tk.Entry(self, textvariable=self.password_var, show="*")
        password_entry.grid(row=1, column=1)

        tk.Button(self, text = "Log In", command = self.login).grid(row=2, column=1)       
        self.keep_signed_in_var = tk.BooleanVar()
        tk.Checkbutton(self,text = "Keep Me Signed In", variable=self.keep_signed_in_var).grid(column=2)

    def login(self):
        # Check the username and password
        username = self.username_var.get()
        password = self.password_var.get()

        expected_username = "admin"
        expected_password = "admin"

        if username == expected_username and password == expected_password:
            self.controller.show_main_window()
        else:
            # Show an error message if the login fails
            error_label = tk.Label(self, text="Invalid username or password")
            error_label.grid(row=3, columnspan=2)

# ADD PASSWORD PROTECTION
# buttons for decision tree, pie chart, scatter graph, line chart
#creation of main window
class Main_Window(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.grid()
 
        def Dec_Tree_Call():
            DecTree = DT
            DecTree.classifier.preprocess_data()
            DecTree.classifier.train_classifer()
            DecTree.classifier.plot_decision_tree()
        
        def Scatter_Call():
            Scatter_Plot = Scatter
            Scatter_Plot.classifier.preprocess_data()
            Scatter_Plot.classifier.train_classifer()
            Scatter_Plot.classifier.show_scatter()


# creation of button
        tk.Label(self, text = "Home Page").grid(row=0, column=0)
        tk.Button(self, text="Decision Tree", command=Dec_Tree_Call).grid(row=1, column=0) #create decision tree argument
        tk.Button(self, text="Predictor", command=controller.show_predictor).grid(row=2, column=0)
        tk.Button(self,text="Scatter Graph", command=Scatter_Call).grid(row=3, column=0)
        tk.Button(self, text="Log out", command=controller.show_login_page).grid(row=4, column=0,) 

#creation of predictor entries
class Predictor(tk.Frame): # add a back button
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.grid()
        self.title=("Predictor")

        gender = tk.IntVar()
        ethnicity = tk.IntVar()
        peducation = tk.IntVar()
        lunch = tk.IntVar()
        math = tk.IntVar()
        reading = tk.IntVar()
        writing = tk.IntVar()
        output = tk.StringVar()

        #add constraints to the entries
        tk.Label(self, text="Gender:").grid(row=0)
        ttk.Combobox(self, textvariable=gender, values=[0, 1]).grid(row=0, column=1)

        tk.Label(self, text="Race/ethnicity:").grid(row=1)
        ttk.Combobox(self, textvariable=ethnicity, values=[0, 1, 2, 3, 4]).grid(row=1, column=1)

        tk.Label(self, text="Parent Level of Education:").grid(row=2)
        ttk.Combobox(self, textvariable=peducation, values=[0, 1, 2, 3, 4, 5]).grid(row=2, column=1)

        tk.Label(self, text="Lunch:").grid(row=3)
        ttk.Combobox(self, textvariable=lunch, values=[0, 1]).grid(row=3, column=1)

        tk.Label(self, text="Math Score (0-100):").grid(row=4)
        tk.Entry(self, textvariable=math).grid(row=4, column=1)

        tk.Label(self, text="Reading Score (0-100):").grid(row=5)
        tk.Entry(self, textvariable=reading).grid(row=5, column=1)

        tk.Label(self, text="Writing Score (0-100):").grid(row=6)
        tk.Entry(self, textvariable=writing).grid(row=6, column=1)

        tk.Label(self, textvariable=output).grid(row=7, column=1)

        def Prediction_Call():
            Prediction.classifier.preprocess_data()
            model = Prediction.classifier.train_classifier()

            data = np.array([ [gender.get(), ethnicity.get(), peducation.get(), lunch.get(), math.get(), reading.get(), writing.get()] ])
            result= model.predict(data)
            if result == 0:
                output.set("The student has taken the test prep course")
            elif result == 1:
                output.set("The student didnt take the test prep course")
            else:
                output.set("ERROR")
            
        tk.Button(self, text = "Prediction: ", command= Prediction_Call).grid(row=7)
        tk.Label(self, text= "Accuracy: 68%").grid(row=9, columnspan=2)
        tk.Button(self, text="Back", command=controller.show_main_window).grid(row=10, columnspan=2) 
        tk.Label(self, text= "Key: Gender(Female/Male = 0/1) - Lunch(free/standard = 0/1)").grid(row=11, columnspan=2)
        tk.Label(self, text= "Race: Group A: Asian, Group B: Black, Group C: Mixed, Group D: White, Group E: Other").grid(row=12, columnspan=2)

class Decision_Tree(tk.Frame): 
    def __init__(self, master, controller):
        super().__init__(master)            
        self.title=("Decision Tree")
        self.controller = controller
        self.grid()

class Scattergraph(tk.Frame): 
    def __init__(self, master, controller):
        super().__init__(master)            
        self.title=("Scatter graph")
        self.controller = controller
        self.grid()

if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller()
    app = MainApplication(root)
    root.mainloop()