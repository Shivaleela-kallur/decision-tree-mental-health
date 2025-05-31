import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
from datetime import datetime
import matplotlib.pyplot as plt
import os

class HabitTracker:
    def __init__(self, master):
        self.master = master
        self.habits = {}
        self.load_habits()

        # GUI Setup
        self.master.title("Habit Tracker")
        self.master.geometry("600x600")
        self.master.configure(bg="#f0f8ff")  # Light blue background

        self.frame = tk.Frame(self.master, bg="#f0f8ff")
        self.frame.pack(padx=10, pady=10)

        # Title Label
        self.title_label = tk.Label(self.frame, text="Habit Tracker", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333")
        self.title_label.grid(row=0, columnspan=2, pady=10)

        # Habit Input Fields
        self.habit_name_label = tk.Label(self.frame, text="Habit Name:", bg="#f0f8ff")
        self.habit_name_label.grid(row=1, column=0, sticky="w")
        self.habit_name_entry = ttk.Entry(self.frame)
        self.habit_name_entry.grid(row=1, column=1)

        self.habit_category_label = tk.Label(self.frame, text="Category:", bg="#f0f8ff")
        self.habit_category_label.grid(row=2, column=0, sticky="w")
        self.habit_category_entry = ttk.Entry(self.frame)
        self.habit_category_entry.grid(row=2, column=1)

        self.habit_frequency_label = tk.Label(self.frame, text="Frequency (daily/weekly/custom):", bg="#f0f8ff")
        self.habit_frequency_label.grid(row=3, column=0, sticky="w")
        self.habit_frequency_entry = ttk.Entry(self.frame)
        self.habit_frequency_entry.grid(row=3, column=1)

        self.habit_description_label = tk.Label(self.frame, text="Description:", bg="#f0f8ff")
        self.habit_description_label.grid(row=4, column=0, sticky="w")
        self.habit_description_entry = ttk.Entry(self.frame)
        self.habit_description_entry.grid(row=4, column=1)

        # Buttons
        self.button_frame = tk.Frame(self.frame, bg="#f0f8ff")
        self.button_frame.grid(row=5, columnspan=2, pady=10)

        self.add_habit_button = ttk.Button(self.button_frame, text="Add Habit", command=self.add_habit)
        self.add_habit_button.pack(side="left", padx=5)

        self.delete_habit_button = ttk.Button(self.button_frame, text="Delete Habit", command=self.delete_habit)
        self.delete_habit_button.pack(side="left", padx=5)

        self.mark_completed_button = ttk.Button(self.button_frame, text="Mark Completed", command=self.mark_completed)
        self.mark_completed_button.pack(side="left", padx=5)

        self.view_progress_button = ttk.Button(self.button_frame, text="View Progress", command=self.show_progress)
        self.view_progress_button.pack(side="left", padx=5)

        # Habit Listbox
        self.habit_listbox = tk.Listbox(self.frame, width=50, bg="#ffffff", fg="#333", font=("Arial", 10))
        self.habit_listbox.grid(row=6, columnspan=2, pady=10)
        self.refresh_habit_list()

    def load_habits(self):
        if os.path.exists('habits.json'):
            try:
                with open('habits.json', 'r') as file:
                    content = file.read().strip()
                    self.habits = json.loads(content) if content else {}
            except json.JSONDecodeError:
                print("Invalid JSON file. Starting with an empty habit list.")
                self.habits = {}
        else:
            self.habits = {}

    def save_habits(self):
        with open('habits.json', 'w') as file:
            json.dump(self.habits, file, indent=4)

    def add_habit(self):
        name = self.habit_name_entry.get()
        category = self.habit_category_entry.get()
        frequency = self.habit_frequency_entry.get()
        description = self.habit_description_entry.get()

        if name and category and frequency:
            self.habits[name] = {
                'category': category,
                'frequency': frequency,
                'description': description,
                'streak': 0,
                'completed_dates': []
            }
            self.save_habits()
            messagebox.showinfo("Success", f"Habit '{name}' added successfully!")
            self.clear_inputs()
            self.refresh_habit_list()
        else:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")

    def delete_habit(self):
        selected_habit = self.habit_listbox.curselection()
        if selected_habit:
            habit_name = self.habit_listbox.get(selected_habit).split(":")[0]
            del self.habits[habit_name]
            self.save_habits()
            messagebox.showinfo("Deleted", f"Habit '{habit_name}' deleted successfully!")
            self.refresh_habit_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a habit to delete.")

    def mark_completed(self):
        selected_habit = self.habit_listbox.curselection()
        if selected_habit:
            habit_name = self.habit_listbox.get(selected_habit).split(":")[0]
            today = datetime.now().date().isoformat()
            if today not in self.habits[habit_name]['completed_dates']:
                self.habits[habit_name]['completed_dates'].append(today)
                self.habits[habit_name]['streak'] += 1
                self.save_habits()
                messagebox.showinfo("Success", f"Habit '{habit_name}' marked as completed!")
            else:
                messagebox.showinfo("Info", f"Habit '{habit_name}' has already been completed today.")
        else:
            messagebox.showwarning("Selection Error", "Please select a habit to mark as completed.")

    def show_progress(self):
        habit_names = list(self.habits.keys())
        streaks = [details['streak'] for details in self.habits.values()]

        if habit_names:
            plt.bar(habit_names, streaks, color='skyblue')
            plt.xlabel('Habits')
            plt.ylabel('Streaks')
            plt.title('Habit Progress')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No Data", "No habits to display progress for.")

    def refresh_habit_list(self):
        self.habit_listbox.delete(0, tk.END)
        for name, details in self.habits.items():
            self.habit_listbox.insert(tk.END, f"{name}: {details['category']} ({details['frequency']})")

    def clear_inputs(self):
        self.habit_name_entry.delete(0, tk.END)
        self.habit_category_entry.delete(0, tk.END)
        self.habit_frequency_entry.delete(0, tk.END)
        self.habit_description_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()
