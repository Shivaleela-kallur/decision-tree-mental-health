import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import os
from datetime import datetime
from tkcalendar import DateEntry

class JournalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Journal App")
        self.geometry("600x500")
        self.config(bg="#f0f0f0")

        # File to store journal entries
        self.journal_file = "journals.json"

        # Ensure the file exists
        if not os.path.exists(self.journal_file):
            with open(self.journal_file, "w") as f:
                json.dump({}, f)

        # Create the main menu
        self.create_main_menu()

    def create_main_menu(self):
        """Create main menu with buttons to open Journal Window and View Journal"""
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Welcome to Your Journal", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Button(self, text="Open Journal Window", font=("Arial", 14), width=20, command=self.openJournalWindow, 
                  bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self, text="View Journal by Date", font=("Arial", 14), width=20, command=self.viewJournalByDate, 
                  bg="#2196F3", fg="white").pack(pady=10)

    def openJournalWindow(self):
        """Open a new window to write a journal entry"""
        journal_window = tk.Toplevel(self)
        journal_window.title("Write Journal Entry")
        journal_window.geometry("600x500")
        journal_window.config(bg="#f0f0f0")

        tk.Label(journal_window, text="Journal Entry", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(journal_window, text="Select Date:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
        date_entry = DateEntry(journal_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.pack(pady=10)

        tk.Label(journal_window, text="Your Journal Entry:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
        journal_text = tk.Text(journal_window, wrap=tk.WORD, height=12, width=50)
        journal_text.pack(padx=20, pady=10)

        def save_entry():
            date = date_entry.get()
            content = journal_text.get("1.0", tk.END).strip()
            if content:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                try:
                    with open(self.journal_file, "r") as f:
                        journals = json.load(f)
                    # Format the date to DD/MM/YY before saving
                    formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%d/%m/%y")
                    journals[formatted_date] = {"content": content, "timestamp": timestamp}
                    with open(self.journal_file, "w") as f:
                        json.dump(journals, f, indent=4)
                    messagebox.showinfo("Success", f"Journal entry for {formatted_date} saved successfully!")
                    journal_window.destroy()
                    self.create_main_menu()  # Go back to the main menu
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving: {e}")
            else:
                messagebox.showwarning("Warning", "Journal entry is empty. Nothing to save.")

        tk.Button(journal_window, text="Save Entry", font=("Arial", 12), command=save_entry, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(journal_window, text="Close", font=("Arial", 12), command=journal_window.destroy, bg="#f44336", fg="white").pack(pady=10)

    def viewJournalByDate(self):
        """Create window to search and view journal entries by date"""
        view_window = tk.Toplevel(self)
        view_window.title("Search Journal by Date")
        view_window.geometry("600x500")
        view_window.config(bg="#f0f0f0")

        tk.Label(view_window, text="Search Journal Entry by Date", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(view_window, text="Enter Date (DD/MM/YY):", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
        date_entry_search = tk.Entry(view_window, font=("Arial", 12), width=20)
        date_entry_search.pack(pady=10)

        journal_text = tk.Text(view_window, wrap=tk.WORD, height=12, width=50)
        journal_text.pack(padx=20, pady=10)

        def search_entry():
            date = date_entry_search.get()
            # Try parsing the date in DD/MM/YY format
            try:
                formatted_date = datetime.strptime(date, "%d/%m/%y").strftime("%d/%m/%y")
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please enter the date in DD/MM/YY format.")
                return

            try:
                with open(self.journal_file, "r") as f:
                    journals = json.load(f)

                if formatted_date in journals:
                    journal_text.delete("1.0", tk.END)  # Clear the text widget first
                    journal_text.insert(tk.END, journals[formatted_date]["content"])  # Display content
                    # Do not close the window here, allow user to see the journal
                else:
                    messagebox.showwarning("Not Found", f"No journal entry found for {formatted_date}.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while searching: {e}")

        tk.Button(view_window, text="Search by Date", font=("Arial", 12), command=search_entry, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(view_window, text="Close", font=("Arial", 12), command=view_window.destroy, bg="#f44336", fg="white").pack(pady=10)


if __name__ == "__main__":
    app = JournalApp()
    app.mainloop()
