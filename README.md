# Student Performance Analytics System

A beginner-friendly Python data-analysis project for the Python with AI assignment. It uses **Python, NumPy and Pandas** to analyse student marks and attendance. It does not use advanced machine learning because the assignment specifically says it is not required.

## Features
- Loads a CSV dataset with 20 sample student records.
- Uses a Pandas DataFrame to validate and organize records.
- Uses NumPy for total, average, highest, lowest and class-level numerical calculations.
- Uses reusable functions, loops and conditions.
- Calculates each student's total and average marks.
- Assigns grades using the grading scale below.
- Identifies Pass/Fail students.
- Analyses subject averages and highest/lowest subject marks.
- Identifies top-performing student(s).
- Saves detailed results to CSV files in `output/`.

## Grading and pass rules
Grades are based on the average across four subjects:
- A+: 90–100
- A: 80–89.99
- B: 70–79.99
- C: 60–69.99
- D: 50–59.99
- F: below 50

A student passes only when they score **at least 40 in every subject**. Attendance status is reported separately: 75% or above meets the attendance threshold. Attendance does not change the academic Pass/Fail result.

## Dataset
`students.csv` contains 20 illustrative sample records. Subject marks and attendance are on a 0–100 scale. Replace the sample records with your own permitted dataset if your trainer requires it. The sample names and marks are for demonstration.

## Requirements
- Python 3.10 or later
- NumPy
- Pandas

## Run on Windows
1. Install Python and select the option to add Python to PATH during installation.
2. Extract the project ZIP.
3. Open PowerShell in the extracted project folder.
4. Create a virtual environment (recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Run:
   ```powershell
   python main.py
   ```
The program prints results and writes `student_results.csv`, `subject_summary.csv`, and `class_summary.csv` into the `output` folder.

## Project structure
```text
Student_Performance_Analytics_System/
├── main.py
├── functions.py
├── students.csv
├── requirements.txt
├── README.md
├── Project_Documentation.md
├── .gitignore
├── docs/
│   └── Google_Form_Submission_Checklist.md
└── output/                 # Generated result CSVs
```

