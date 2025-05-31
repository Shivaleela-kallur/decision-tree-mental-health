import itertools
import pandas as pd

# Define the symptoms
symptoms = [
    "Anxiety", "Mood Swings", "Insomnia", "Hallucinations", "Social Withdrawal", 
    "Panic Attacks", "Fatigue", "Memory Loss", "Confusion"
]

# Generate all possible combinations of 0 and 1 for the 9 symptoms
combinations = list(itertools.product([0, 1], repeat=len(symptoms)))

# Create a DataFrame with the combinations
df = pd.DataFrame(combinations, columns=symptoms)

# Define the file path to save the CSV
file_path = r'C:\Users\shiva\OneDrive\Desktop\pythonproject\symptom_combinations.csv'

# Save the DataFrame to the specified path
df.to_csv(file_path, index=False)

file_path
