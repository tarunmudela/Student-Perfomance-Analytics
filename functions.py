"""Reusable functions for Student Performance Analytics System."""
from __future__ import annotations

import numpy as np
import pandas as pd

MARKS_COLUMNS = ["python_marks", "statistics_marks", "database_marks", "ai_marks"]
PASS_MARK = 40
ATTENDANCE_THRESHOLD = 75

def assign_grade(average: float) -> str:
    """Assign a letter grade using the project's documented grading scale."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"

def load_dataset(file_path: str) -> pd.DataFrame:
    """Load and validate the student CSV dataset."""
    df = pd.read_csv(file_path)
    required = {"student_id", "name", "department", "attendance_percent", *MARKS_COLUMNS}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("The dataset contains no student records.")
    for col in MARKS_COLUMNS + ["attendance_percent"]:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not df[MARKS_COLUMNS].apply(lambda col: col.between(0, 100).all()).all():
        raise ValueError("Marks must be between 0 and 100.")
    if not df["attendance_percent"].between(0, 100).all():
        raise ValueError("Attendance must be between 0 and 100.")
    return df

def calculate_student_results(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy enriched with total, average, grade and pass/fail status."""
    result = df.copy()
    result["total_marks"] = np.sum(result[MARKS_COLUMNS].to_numpy(dtype=float), axis=1)
    result["average_marks"] = np.mean(result[MARKS_COLUMNS].to_numpy(dtype=float), axis=1).round(2)
    result["grade"] = result["average_marks"].apply(assign_grade)
    # A student passes only if every subject mark is at least PASS_MARK.
    result["result"] = result[MARKS_COLUMNS].ge(PASS_MARK).all(axis=1).map({True: "Pass", False: "Fail"})
    result["attendance_status"] = np.where(
        result["attendance_percent"] >= ATTENDANCE_THRESHOLD, "Meets threshold", "Below threshold"
    )
    return result

def subject_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize average, highest and lowest marks for each subject."""
    rows = []
    for subject in MARKS_COLUMNS:  # Explicit loop to demonstrate iteration.
        values = df[subject].to_numpy(dtype=float)
        rows.append({
            "subject": subject.replace("_marks", "").replace("_", " ").title(),
            "average": round(float(np.mean(values)), 2),
            "highest": int(np.max(values)),
            "lowest": int(np.min(values)),
        })
    return pd.DataFrame(rows).sort_values("average", ascending=False).reset_index(drop=True)

def build_analysis(results: pd.DataFrame) -> dict:
    """Calculate class-level statistics and identify top performers."""
    averages = results["average_marks"].to_numpy(dtype=float)
    passed = int((results["result"] == "Pass").sum())
    top_average = float(np.max(averages))
    top_students = results.loc[results["average_marks"] == top_average, ["student_id", "name", "average_marks", "grade"]]
    return {
        "student_count": int(len(results)),
        "class_average": round(float(np.mean(averages)), 2),
        "highest_average": round(top_average, 2),
        "lowest_average": round(float(np.min(averages)), 2),
        "passed_count": passed,
        "failed_count": int(len(results) - passed),
        "pass_percentage": round(passed / len(results) * 100, 2),
        "top_students": top_students,
    }
