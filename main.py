"""Main entry point for Student Performance Analytics System."""
from pathlib import Path
import pandas as pd

from functions import load_dataset, calculate_student_results, subject_summary, build_analysis

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "students.csv"
OUTPUT_DIR = BASE_DIR / "output"

def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_dataset(str(DATASET_PATH))
    results = calculate_student_results(df)
    subjects = subject_summary(results)
    analysis = build_analysis(results)

    print("=" * 68)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 68)
    print(f"\nDataset loaded successfully: {analysis['student_count']} student records")
    print("\nSTUDENT RESULTS")
    display_cols = ["student_id", "name", "department", "total_marks", "average_marks", "grade", "result", "attendance_status"]
    print(results[display_cols].to_string(index=False))
    print("\nCLASS SUMMARY")
    print(f"Class average: {analysis['class_average']:.2f}/100")
    print(f"Highest student average: {analysis['highest_average']:.2f}/100")
    print(f"Lowest student average: {analysis['lowest_average']:.2f}/100")
    print(f"Passed: {analysis['passed_count']} | Failed: {analysis['failed_count']}")
    print(f"Pass percentage: {analysis['pass_percentage']:.2f}%")
    print("\nSUBJECT-WISE PERFORMANCE (best average first)")
    print(subjects.to_string(index=False))
    print("\nTOP-PERFORMING STUDENT(S)")
    print(analysis["top_students"].to_string(index=False))

    results.to_csv(OUTPUT_DIR / "student_results.csv", index=False)
    subjects.to_csv(OUTPUT_DIR / "subject_summary.csv", index=False)
    summary = pd.DataFrame([{
        "student_count": analysis["student_count"],
        "class_average": analysis["class_average"],
        "highest_average": analysis["highest_average"],
        "lowest_average": analysis["lowest_average"],
        "passed_count": analysis["passed_count"],
        "failed_count": analysis["failed_count"],
        "pass_percentage": analysis["pass_percentage"],
    }])
    summary.to_csv(OUTPUT_DIR / "class_summary.csv", index=False)
    print(f"\nSaved analysis files in: {OUTPUT_DIR}")
    print("Project completed successfully.")

if __name__ == "__main__":
    main()
