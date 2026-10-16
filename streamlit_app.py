"""Streamlit web app: Student Performance Analytics System."""
from pathlib import Path
import pandas as pd
import streamlit as st

from functions import load_dataset, calculate_student_results, subject_summary, build_analysis

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "students.csv"
MARK_COLUMNS = [
    "python_marks",
    "statistics_marks",
    "database_marks",
    "ai_marks",
]

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Student Performance Analytics System")
st.write(
    "Analyse student marks and attendance with Python, Pandas, and NumPy. "
    "Use the sample dataset or upload a compatible CSV file."
)

with st.sidebar:
    st.header("Dataset")
    uploaded_file = st.file_uploader(
        "Upload a student CSV file (optional)",
        type=["csv"],
        help="Your uploaded file must contain the columns listed below.",
    )
    st.caption("Required columns")
    st.code(
        "student_id, name, department,\n"
        "python_marks, statistics_marks,\n"
        "database_marks, ai_marks,\n"
        "attendance_percent",
        language="text",
    )

try:
    if uploaded_file is None:
        data = load_dataset(str(DATASET_PATH))
        st.info("Using the included sample dataset: students.csv")
    else:
        data = pd.read_csv(uploaded_file)
        required_columns = {
            "student_id",
            "name",
            "department",
            "attendance_percent",
            *MARK_COLUMNS,
        }
        missing = sorted(required_columns.difference(data.columns))
        if missing:
            st.error("Missing required CSV columns: " + ", ".join(missing))
            st.stop()

        if data.empty:
            st.error("The uploaded CSV has no student records.")
            st.stop()

        for column in MARK_COLUMNS + ["attendance_percent"]:
            data[column] = pd.to_numeric(data[column], errors="coerce")
            if data[column].isna().any():
                st.error(f"Column '{column}' contains blank or non-numeric values.")
                st.stop()
            if not data[column].between(0, 100).all():
                st.error(f"Values in '{column}' must be between 0 and 100.")
                st.stop()

        st.success(f"Uploaded {len(data)} student records.")

    results = calculate_student_results(data)
    summary = build_analysis(results)
    subjects = subject_summary(results)

    st.subheader("Class Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Students", summary["student_count"])
    m2.metric("Class Average", f"{summary['class_average']:.2f}%")
    m3.metric("Pass Rate", f"{summary['pass_percentage']:.2f}%")
    m4.metric("Highest Average", f"{summary['highest_average']:.2f}%")

    pass_col, fail_col = st.columns(2)
    pass_col.metric("Passed", summary["passed_count"])
    fail_col.metric("Failed", summary["failed_count"])

    st.subheader("Student Results")
    department_options = ["All departments"] + sorted(
        results["department"].astype(str).unique().tolist()
    )
    selected_department = st.selectbox("Filter by department", department_options)
    filtered = results.copy()
    if selected_department != "All departments":
        filtered = filtered[filtered["department"] == selected_department]

    search_text = st.text_input("Search by student name or ID")
    if search_text.strip():
        term = search_text.strip().lower()
        filtered = filtered[
            filtered["name"].astype(str).str.lower().str.contains(term, na=False)
            | filtered["student_id"].astype(str).str.lower().str.contains(term, na=False)
        ]

    result_columns = [
        "student_id",
        "name",
        "department",
        *MARK_COLUMNS,
        "total_marks",
        "average_marks",
        "grade",
        "result",
        "attendance_percent",
        "attendance_status",
    ]
    st.dataframe(
        filtered[result_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇️ Download student results CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="student_results.csv",
        mime="text/csv",
    )

    st.subheader("Subject-wise Performance")
    st.dataframe(subjects, use_container_width=True, hide_index=True)
    st.bar_chart(subjects.set_index("subject")["average"])

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.subheader("Pass / Fail Summary")
        pass_fail = (
            results["result"]
            .value_counts()
            .rename_axis("result")
            .to_frame("students")
        )
        st.bar_chart(pass_fail)
    with chart_right:
        st.subheader("Attendance Summary")
        attendance = (
            results["attendance_status"]
            .value_counts()
            .rename_axis("attendance_status")
            .to_frame("students")
        )
        st.bar_chart(attendance)

    st.subheader("Top-performing Student(s)")
    st.dataframe(summary["top_students"], use_container_width=True, hide_index=True)

    class_summary = pd.DataFrame(
        [
            {
                "student_count": summary["student_count"],
                "class_average": summary["class_average"],
                "highest_average": summary["highest_average"],
                "lowest_average": summary["lowest_average"],
                "passed_count": summary["passed_count"],
                "failed_count": summary["failed_count"],
                "pass_percentage": summary["pass_percentage"],
            }
        ]
    )

    st.subheader("Download Reports")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download subject summary CSV",
            data=subjects.to_csv(index=False).encode("utf-8"),
            file_name="subject_summary.csv",
            mime="text/csv",
        )
    with c2:
        st.download_button(
            "Download class summary CSV",
            data=class_summary.to_csv(index=False).encode("utf-8"),
            file_name="class_summary.csv",
            mime="text/csv",
        )

    with st.expander("About this project"):
        st.markdown(
            """
            This educational project uses **Python**, **Pandas**, and **NumPy**.
            It calculates student totals and averages, assigns grades, reports
            Pass/Fail status, analyses subjects, and summarizes attendance.

            **Project rules:** a student passes when every subject mark is at
            least 40. Grades are based on the average: A+ (90+), A (80+),
            B (70+), C (60+), D (50+), and F (below 50). Attendance of 75%
            or above meets the sample attendance threshold. These are
            demonstration rules, not official institutional grading rules.
            """
        )

except FileNotFoundError:
    st.error("Could not find students.csv. Add it beside streamlit_app.py in your GitHub repository.")
except Exception as error:
    st.error(f"Could not analyse the dataset: {error}")
    st.info("Check the CSV columns and make sure marks and attendance are between 0 and 100.")
