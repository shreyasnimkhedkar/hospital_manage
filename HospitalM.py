import streamlit as st
import pyodbc
from datetime import date

# Database connection
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-A46VDG6\SQLEXPRESS;"  # Replace with your SQL Server name
    "Database=HospitalManagement;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Functions for database operations
def add_patient(name, age, gender, phone, address):
    cursor.execute(
        "INSERT INTO Patients (Name, Age, Gender, Phone, Address) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, phone, address)
    )
    conn.commit()
    st.success("Patient added successfully!")

def view_patients():
    cursor.execute("SELECT * FROM Patients")
    return cursor.fetchall()

def add_doctor(name, specialty, phone):
    cursor.execute(
        "INSERT INTO Doctors (Name, Specialty, Phone) VALUES (?, ?, ?)",
        (name, specialty, phone)
    )
    conn.commit()
    st.success("Doctor added successfully!")

def view_doctors():
    cursor.execute("SELECT * FROM Doctors")
    return cursor.fetchall()

def book_appointment(patient_id, doctor_id, appointment_date):
    cursor.execute(
        "INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate) VALUES (?, ?, ?)",
        (patient_id, doctor_id, appointment_date)
    )
    conn.commit()
    st.success("Appointment booked successfully!")

def view_appointments():
    cursor.execute("""
        SELECT a.AppointmentID, p.Name AS PatientName, d.Name AS DoctorName, a.AppointmentDate
        FROM Appointments a
        JOIN Patients p ON a.PatientID = p.PatientID
        JOIN Doctors d ON a.DoctorID = d.DoctorID
    """)
    return cursor.fetchall()

# Streamlit Interface
st.title("Hospital Management System")

menu = ["Add Patient", "View Patients", "Add Doctor", "View Doctors", "Book Appointment", "View Appointments"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Patient":
    st.subheader("Add a New Patient")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")
    if st.button("Add Patient"):
        add_patient(name, age, gender, phone, address)

elif choice == "View Patients":
    st.subheader("Patient List")
    patients = view_patients()
    for patient in patients:
        st.write(patient)

elif choice == "Add Doctor":
    st.subheader("Add a New Doctor")
    name = st.text_input("Doctor Name")
    specialty = st.text_input("Specialty")
    phone = st.text_input("Phone Number")
    if st.button("Add Doctor"):
        add_doctor(name, specialty, phone)

elif choice == "View Doctors":
    st.subheader("Doctor List")
    doctors = view_doctors()
    for doctor in doctors:
        st.write(doctor)

elif choice == "Book Appointment":
    st.subheader("Book an Appointment")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    doctor_id = st.number_input("Doctor ID", min_value=1, step=1)
    appointment_date = st.date_input("Appointment Date", min_value=date.today())
    if st.button("Book Appointment"):
        book_appointment(patient_id, doctor_id, appointment_date)

elif choice == "View Appointments":
    st.subheader("Appointments List")
    appointments = view_appointments()
    for appointment in appointments:
        st.write(appointment)
