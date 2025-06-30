CREATE DATABASE hospital_db;

USE hospital_db;

-- Users table
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    role VARCHAR(20)
);

-- Insert sample users
INSERT INTO users VALUES ('admin', 'admin', 'Admin'), ('doctor', 'doctor', 'Doctor'), ('reception', 'reception', 'Receptionist');

-- Patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(20),
    disease VARCHAR(100)
);

-- Doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    contact VARCHAR(20),
    availability VARCHAR(100)
);

-- Appointments table
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    doctor_name VARCHAR(100),
    disease VARCHAR(100),
    date DATE
);

-- Medical records table
CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    diagnosis TEXT,
    treatment TEXT
);
