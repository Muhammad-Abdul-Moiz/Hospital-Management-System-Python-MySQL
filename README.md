# Hospital Management System – Python and MySQL

This is a role-based desktop Hospital Management System built using Python for the backend and GUI (CustomTkinter) and MySQL for database management. It allows hospital staff to manage patients, doctors, appointments, and medical records through a secure and intuitive interface.

---

## Features

- Login system with user roles: Admin, Doctor, and Receptionist  
- Dashboard with real-time statistics  
- Patient management (add, view details)  
- Doctor directory management  
- Appointment scheduling system  
- Medical record logging (diagnosis and treatment)  
- GUI designed with CustomTkinter  
- MySQL integration for persistent data storage  

---

## Technologies Used

- Python 3.13+  
- CustomTkinter (for GUI)  
- MySQL  
- mysql-connector-python  

---

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system
```

### 2. Install Dependencies

```bash
pip install customtkinter mysql-connector-python
```

### 3. Set Up MySQL Database

```sql
CREATE DATABASE hospital_db;
USE hospital_db;

CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    role VARCHAR(20)
);

INSERT INTO users VALUES 
('admin', 'admin', 'Admin'),
('doctor', 'doctor', 'Doctor'),
('reception', 'reception', 'Receptionist');

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(20),
    disease VARCHAR(100)
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    contact VARCHAR(20),
    availability VARCHAR(100)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    doctor_name VARCHAR(100),
    disease VARCHAR(100),
    date DATE
);

CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    diagnosis TEXT,
    treatment TEXT
);
```

### 4. Run the Application

```bash
python Hospital_Management_System.py
```

---

## Default Login Credentials

| Role         | Username   | Password   |
|--------------|------------|------------|
| Admin        | admin      | admin      |
| Doctor       | doctor     | doctor     |
| Receptionist | reception  | reception  |


