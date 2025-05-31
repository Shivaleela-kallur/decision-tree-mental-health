import tkinter as tk
from tkinter import Toplevel, Label, Text

def openStepsWindow(root, present_disease):
    # Create a new window for coping strategies
    steps_window = Toplevel(root)
    steps_window.title("Coping Strategies")
    steps_window.geometry("400x400")  # Set the size of the window
    present_disease = "Anxiety"
    # Example coping strategies dictionary
    coping_strategies = {
        "Anxiety": [
            "Practice deep breathing exercises.",
            "Engage in physical activity.",
            "Try mindfulness meditation.",
            "Limit caffeine and sugar intake."
        ],
        "Depression": [
            "Establish a daily routine.",
            "Stay connected with friends and family.",
            "Engage in activities you enjoy.",
            "Consider journaling your thoughts."
        ],
        "OCD": [
            "Practice exposure and response prevention.",
            "Challenge your obsessive thoughts.",
            "Engage in relaxation techniques.",
            "Seek support from a therapist."
        ],
        "Bipolar Disorder": [
            "Maintain a regular sleep schedule.",
            "Monitor your mood changes.",
            "Engage in regular physical activity.",
            "Stay connected with your support network."
        ],
        "Chronic Fatigue Syndrome": [
            "Pace yourself and rest when needed.",
            "Engage in gentle exercise.",
            "Practice stress management techniques.",
            "Consider dietary changes."
        ],
        "Schizophrenia": [
            "Stay on your medication as prescribed.",
            "Engage in social activities.",
            "Practice stress reduction techniques.",
            "Seek support from mental health professionals."
        ],
        "Dementia": [
            "Engage in memory exercises.",
            "Maintain a routine.",
            "Stay socially active.",
            "Consider joining a support group."
        ],
        "PTSD": [
            "Practice grounding techniques.",
            "Engage in physical activity.",
            "Consider therapy options.",
            "Connect with support groups."
        ]
    }

    # Retrieve and display coping strategies
    strategies = coping_strategies.get(present_disease, ["No coping strategies available."])
    
    # Create a label for the present disease
    Label(steps_window, text=f"Present Disease: {present_disease}", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Create a label for coping strategies
    Label(steps_window, text="Coping Strategies:", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Create a text widget to display coping strategies
    strategies_text = Text(steps_window, height=10, width=50)
    strategies_text.pack(pady=10)

    # Insert coping strategies into the text widget
    for strategy in strategies:
        strategies_text.insert(tk.END, f"- {strategy}\n")
