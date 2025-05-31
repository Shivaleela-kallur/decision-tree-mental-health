from tkinter import *
from tkinter import messagebox                           
import os            
import webbrowser
import numpy as np
import pandas as pd
from tkcalendar import DateEntry
import json
import subprocess

class HyperlinkManager:
      
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return


training_dataset = pd.read_csv('train.csv')
test_dataset = pd.read_csv('test.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:9].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['diagnosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols     = training_dataset.columns
cols     = cols[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree

# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
        #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero() 
        #print(val)
        disease = labelencoder.inverse_transform(val[0])
        return disease
def recurse(node, depth):
            global val,ans
            global tree_,feature_name,symptoms_present,present_disease
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                yield name + " ?"
                
#                ans = input()
                ans = ans.lower()
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    yield from recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    yield from recurse(tree_.children_right[node], depth + 1)
            else:
                strData = ""
                present_disease = print_disease(tree_.value[node]) 
                
                print()
                strData="\nYou may have :" +  str(present_disease)
               
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                
                red_cols = dimensionality_reduction.columns 
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
                print("Symptoms present  " + str(list(symptoms_present)))
                print()
                
                strData="symptoms present:  " + str(list(symptoms_present))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                print()
                
                strData="symptoms given: "  +  str(list(symptoms_given))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
                print()

                strData="confidence level is: " + str(confidence_level)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                print()

                strData='The model suggests:'
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                row = doctors[doctors['disease'] == present_disease[0]]

                for index, row in record.iterrows():  # iterate over the filtered doctors record
                    # Create the string for the doctor's name to be inserted into the text widget
                    strData = 'Consult ' + str(row['name'])  # Extract the doctor's name from the row
                    
                    # Insert the consultation text into the widget
                    QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData + '\n') 

                    # Create a hyperlink for the doctor's link
                    hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
                    strData = 'Visit ' + str(row['link'])  # Extract the doctor's link
                    
                    # Define the click function to open the doctor's website
                    def click1():
                        webbrowser.open_new(str(row['link']))  # Open the link in a new browser tab
                    
                    # Insert the visit link with the hyperlink functionality
                    QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
                    
                    # Optionally add a new line for readability
                    QuestionDigonosis.objRef.txtDigonosis.insert(END, '\n')

                    # Yield the string data if needed for other purposes
                    yield sum
        
def tree_to_code(tree, feature_names):
        global tree_,feature_name,symptoms_present
        tree_ = tree.tree_
        #print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        #print("def tree({}):".format(", ".join(feature_names)))
        symptoms_present = []   
#        recurse(0, 1)
    

def execute_bot():
    tree_to_code(classifier,cols)



# This section of code to be run after scraping the data

doc_dataset = pd.read_csv('doctors_dataset.csv', names=['Name', 'Description'])

# Sample list of mental healthcare diseases (modify this as needed)
mental_health_diseases = ['Depression', 'Anxiety', 'Schizophrenia', 'Bipolar Disorder', 'PTSD']

# Simulating dimensionality reduction index with a list of diseases (for example purposes)
# In actual implementation, this should come from the 'dimensionality_reduction.index' or similar
diseases = pd.DataFrame({'diagnosis': mental_health_diseases})

# Creating an empty DataFrame for doctors
doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

# Assign the disease column to the doctors DataFrame (here, assuming we are mapping one disease per doctor)
doctors['disease'] = diseases['diagnosis']

# Assign doctor names and links from the CSV dataset
doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

# Now filter the doctors for a specific disease (e.g., 'Anxiety')
record = doctors[doctors['disease'] == 'PTSD']



# Execute the bot and see it in Action
#execute_bot()


class QuestionDigonosis(Frame):
    global coping_strategies
    objIter=None
    objRef=None
    def __init__(self,master=None):
        master.title("Question")
        master.geometry("1920x1080")
        QuestionDigonosis.objRef=self
        super().__init__(master=master)
        self.master.config(bg="dark gray")  # Set the background color of the entire window

        # Ensure the frame takes up the whole window space
        self.grid(row=0, column=0, sticky="nsew")  # This ensures the frame expands to fit the window
        self.master.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        self.master.grid_columnconfigure(0, weight=1)
        self.createWidget()
        self.iterObj=None

    def createWidget(self):


        
        self.lblHeadline = Label(self, 
                         text="Mental Healthcare Chatbot", 
                         font=("Arial", 16, "bold"), 
                         anchor="w", 
                         justify=LEFT)
        self.lblHeadline.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        self.lblQuestion = Label(self, 
                         text="You will be asked questions once the therapy session starts", 
                         width=100, 
                         font=("Arial", 12, "italic"), 
                         anchor="w", 
                         justify=LEFT)
        self.lblQuestion.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.lblDiagonosis = Label(self, text="The therapy results will appear once the session is complete\n", 
                                  font=("Arial", 12), width=100, anchor="w", justify=LEFT)
        
        self.lblDiagonosis.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        

        self.txtDigonosis = Text(self, width=80, height=8, wrap=WORD, font=("Arial", 10))
        self.txtDigonosis.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.txtQuestion = Text(self, width=80, height=6, wrap=WORD, font=("Arial", 10))
        self.txtQuestion.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        

        self.btnYes = Button(self, text="YES", width=12, bg="white", font=("Arial", 10, "bold"), command=self.btnYes_Click)
        self.btnYes.grid(row=6, column=0, padx=20, pady=10)
        

        self.btnNo = Button(self, text="NO", width=12, bg="white", font=("Arial", 10, "bold"), command=self.btnNo_Click)
        self.btnNo.grid(row=6, column=1, padx=20, pady=10)


        self.btnClear = Button(self, text="Clear", width=12, bg="skyblue", font=("Arial", 10), command=self.btnClear_Click)
        self.btnClear.grid(row=7, column=0, padx=20, pady=10)

        self.btnStart = Button(self, text="Start", width=12, bg="skyblue", font=("Arial", 10, "bold"), command=self.btnStart_Click)
        self.btnStart.grid(row=7, column=1, padx=20, pady=10)


        self.createMenuBar()

    def createMenuBar(self):
        # Create menu bar
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)

        # Add navigation options
        nav_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Navigation", menu=nav_menu)

        nav_menu.add_command(label="Coping Strategies", command=self.openStepsWindow)
        nav_menu.add_command(label="Journal", command=self.run_journal_script)
        nav_menu.add_command(label="Habit Tracker", command=self.openHabitTrackerWindow)
        nav_menu.add_separator()
        nav_menu.add_command(label="Exit", command=self.master.quit)
        
    def openStepsWindow(self):
        # Create a new window
        steps_window = Toplevel(self.master)
        steps_window.title("Coping Strategies")
        steps_window.geometry("400x400")

        # Create a label for the title
        title_label = Label(steps_window, text="Coping Strategies for Mental Illnesses", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Create a Text widget to display the coping strategies
        strategies_text = Text(steps_window, wrap=WORD, font=("Arial", 10))
        strategies_text.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Insert coping strategies into the Text widget
        for illness, strategies in coping_strategies.items():
            strategies_text.insert(END, f"{illness}:\n")
            for strategy in strategies:
                strategies_text.insert(END, f"{strategy}\n")
            strategies_text.insert(END, "\n")  # Add a newline for spacing

        # Make the Text widget read-only
        strategies_text.config(state=DISABLED)
      
    coping_strategies = {
        "Depression": [
            "1. Talk to someone you trust.",
            "2. Engage in physical activity.",
            "3. Practice mindfulness or meditation.",
            "4. Maintain a regular sleep schedule.",
            "5. Set small, achievable goals."
        ],
        "Anxiety": [
            "1. Practice deep breathing exercises.",
            "2. Limit caffeine and sugar intake.",
            "3. Keep a journal to express your thoughts.",
            "4. Engage in hobbies you enjoy.",
            "5. Seek professional help if needed."
        ],
        "Schizophrenia": [
            "1. Stick to a treatment plan.",
            "2. Avoid drugs and alcohol.",
            "3. Stay connected with family and friends.",
            "4. Join a support group.",
            "5. Practice stress management techniques."
        ],
        "Bipolar Disorder": [
            "1. Keep a mood diary.",
            "2. Establish a routine.",
            "3. Avoid high-stress situations.",
            "4. Stay active and eat healthily.",
            "5. Communicate openly with your support system."
        ],
        "PTSD": [
            "1. Practice grounding techniques.",
            "2. Engage in physical exercise.",
            "3. Seek therapy or counseling.",
            "4. Connect with support groups.",
            "5. Avoid isolating yourself."
        ]
        }
    
        
    def run_journal_script(self):
        """Runs the journal.py script using subprocess"""
        try:
            # Assuming journal.py is in the same directory as this script
            subprocess.run(['python', 'journal.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    
    def openHabitTrackerWindow(self):
        """Runs the habitTracker .py script using subprocess"""
        try:
            # Assuming habitTracker.py is in the same directory as this script
            subprocess.run(['python', 'habitTracker.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")

    


        
    def btnNo_Click(self):
        
        global val,ans
        ans='no'
        try:
            str1 = QuestionDigonosis.objIter.__next__()
            
            # Ensure str1 is a valid string
            if isinstance(str1, str):
                self.txtQuestion.delete(0.0, END)
                self.txtQuestion.insert(END, str1 + "\n")
            else:
                # Handle the case where str1 is not a string
                self.txtQuestion.delete(0.0, END)
                self.txtQuestion.insert(END, "No more Quetsions\n")
                
        except StopIteration:
            # Handle the case when the iteration is complete
            self.txtQuestion.delete(0.0, END)
            self.txtQuestion.insert(END, "No more questions available\n")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Error: {e}")
            self.txtQuestion.delete(0.0, END)
            self.txtQuestion.insert(END, "No more Questions\n")
        
    def btnYes_Click(self):
        global val,ans
        ans='yes'
        
        try:
            str1 = QuestionDigonosis.objIter.__next__()
            
            # Ensure str1 is a valid string
            if isinstance(str1, str):
                self.txtQuestion.delete(0.0, END)
                self.txtQuestion.insert(END, str1 + "\n")
            else:
                # Handle the case where str1 is not a string
                self.txtQuestion.delete(0.0, END)
                self.txtQuestion.insert(END, "No more Quetsions\n")
                
        except StopIteration:
            # Handle the case when the iteration is complete
            self.txtQuestion.delete(0.0, END)
            self.txtQuestion.insert(END, "No more questions available\n")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Error: {e}")
            self.txtQuestion.delete(0.0, END)
            self.txtQuestion.insert(END, "No more Questions\n")
        
        
    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
        self.txtDigonosis.insert(END,"Please Click on Yes or No for the Above symptoms in Question")                  
        QuestionDigonosis.objIter=recurse(0, 1)
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END,str1+"\n")


class MainForm(Frame):
    main_Root = None
    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        master.geometry("1920x1080")
        master.title("Account")
        self.createWidget()
    def createWidget(self):
        self.lblMsg = Label(
            self,
            text="MENTAL HEALTHCARE CHATBOT",
            bg="lightblue",
            fg="black",
            width="280",
            height="2",
            font=("Helvetica 13 bold")
        )
        self.lblMsg.pack(pady=(20, 30))

        # Login Button
        self.btnLogin = Button(
            self,
            text="LOGIN",
            bg="lightgreen",
            fg="black",
            height="1",
            width="15",
            font=("Helvetica", 13),
            command=self.lblLogin_Click
        )
        self.btnLogin.pack(pady=10)

        # Register Button
        self.btnRegister = Button(
            self,
            text="REGISTER",
            bg="lightgreen",
            fg="black",
            height="1",
            width="15",
            font=("Helvetica", 13),
            command = self.btnRegister_Click
        )
        self.btnRegister.pack(pady=10)

        # Footer Text
        self.footer = Label(
            self,
            text="Your companion for mental well-being.",
            bg="white",
            fg="gray",
            font=("Helvetica", 10, "italic")
        )
        self.footer.pack(side="bottom", pady=20)


        
        
        
    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmLogin=Login(MainForm.main_Root)
        frmLogin.pack()
    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmSignUp = SignUp(MainForm.main_Root)
        frmSignUp.pack()



        
class Login(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        Login.main_Root=master
        super().__init__(master=master)
        master.title("Login")
        master.geometry("1920x1080")
        self.createWidget()
    def createWidget(self):
        self.lblMsg = Label(
            self,
            text="Please enter details below to login",
            width=30,
            font=("Calibri", 18),
            padx=10,
            pady=10,
            bg="black",
            fg="white"
        )
        self.lblMsg.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="ew")

        # Username Label and Entry
        self.username = Label(
            self,
            text="Username ",
            padx=10,
            pady=10,
            font=("Calibri", 18),
            bg="black",
            fg="white"
        )
        self.username.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        self.username_verify = StringVar()
        self.username_login_entry = Entry(
            self,
            textvariable=self.username_verify,
            font=("Calibri", 16),
            width=25
        )
        self.username_login_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password Label and Entry
        self.password = Label(
            self,
            text="Password ",
            padx=10,
            pady=10,
            font=("Calibri", 18),
            bg="black",
            fg="white"
        )
        self.password.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        self.password_verify = StringVar()
        self.password_login_entry = Entry(
            self,
            textvariable=self.password_verify,
            show='*',
            font=("Calibri", 16),
            width=25
        )
        self.password_login_entry.grid(row=2, column=1, padx=10, pady=5)

        # Login Button
        self.btnLogin = Button(
            self,
            text="Login",
            width=10,
            height=1,
            font=("Calibri", 18),
            bg="forest green",
            fg="white",
            command=self.btnLogin_Click
        )
        self.btnLogin.grid(row=3, column=0, columnspan=2, pady=(20, 10))


    def btnLogin_Click(self):
        username1 = self.username_login_entry.get()
        password1 = self.password_login_entry.get()
        
#        messagebox.showinfo("Failure", self.username1+":"+password1)
        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                messagebox.showinfo("Sucess","Login Sucessful")
                self.destroyPackWidget(Login.main_Root)
                frmQuestion = QuestionDigonosis(Login.main_Root)
                frmQuestion.pack()
            else:
                messagebox.showinfo("Failure", "Login Details are wrong try again")
        else:
            messagebox.showinfo("Failure", "User not found try from another user\n or sign up for new user")


class SignUp(Frame):
    main_Root=None
    print("SignUp Class")
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        SignUp.main_Root=master
        master.title("Register")
        super().__init__(master=master)
        master.title("Register")
        master.geometry("1920x1080")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Please enter the details below",width="300",font=("Calibri", 18), padx=10, pady=10, bg="black", fg="white")
        self.lblMsg.pack()
        self.username_lable = Label(self, text="Username ",padx=10, pady=10,font=("Calibri", 18))
        self.username_lable.pack()
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username)
        self.username_entry.pack()

        self.password_lable = Label(self, text="Password ",padx=10, pady=10,font=("Calibri", 18))
        self.password_lable.pack()
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack()
        self.btnRegister=Button(self, text="Register",font=("Calibri", 22), bg="forest green", fg="white", command=self.register_user)
        self.btnRegister.pack()


    def register_user(self):
        file = open(self.username_entry.get(), "w")
        file.write(self.username_entry.get() + "\n")
        file.write(self.password_entry.get())
        file.close()
        
        self.destroyPackWidget(SignUp.main_Root)
        
        self.lblSucess=Label(root, text="Registration Success", fg="green", font=("calibri", 11))
        self.lblSucess.pack()
        
        self.btnSucess=Button(root, text="Click Here to proceed", command=self.btnSucess_Click)
        self.btnSucess.pack()
    def btnSucess_Click(self):

        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)

        frmQuestion.pack()



root = Tk()

frmMainForm=MainForm(root)
frmMainForm.pack()
root.mainloop()

