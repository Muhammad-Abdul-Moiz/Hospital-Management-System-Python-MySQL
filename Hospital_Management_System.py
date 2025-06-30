import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# TODO: wrap this in a try-except block if time permits
db_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # 🔐 Change this before shipping — reminder to self
    database="hospital_db"
)
db_cursor = db_conn.cursor(dictionary=True)

# UI theme setup — might switch to dark later
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login | Hospital Management System")
        self.geometry("400x400")
        self.resizable(False, False)

        # Header
        ctk.CTkLabel(self, text="🏥 Login to HMS", font=("Segoe UI", 22, "bold")).pack(pady=40)

        # Login inputs
        self.user_input = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_input.pack(pady=10, padx=40)

        self.pass_input = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.pass_input.pack(pady=10, padx=40)

        # Login button
        self.login_btn = ctk.CTkButton(self, text="Login", command=self.attempt_login)
        self.login_btn.pack(pady=20)

        # Message label for feedback
        self.msg_label = ctk.CTkLabel(self, text="", text_color="red")
        self.msg_label.pack()

    def attempt_login(self):
        username = self.user_input.get()
        password = self.pass_input.get()

        # Query to check credentials — plain check for now, hashing later maybe?
        db_cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        record = db_cursor.fetchone()

        if record:
            self.destroy()
            # User role determines UI privileges
            app = HospitalDashboardApp(username, record.get("role"))
            app.mainloop()
        else:
            self.msg_label.configure(text="Invalid username or password")


class HospitalDashboardApp(ctk.CTk):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.title("🏥 Hospital Management System")
        self.geometry("1080x640")
        self.resizable(False, False)

        # Side panel navigation
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1E1E2F")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="🏥 HMS", font=("Segoe UI", 22, "bold"), text_color="white").pack(pady=30)

        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Patients", self.show_patients),
            ("Doctors", self.show_doctors),
            ("Appointments", self.show_appointments),
            ("Medical Records", self.show_records)
        ]

        for label, handler in nav_items:
            nav_btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                command=handler,
                corner_radius=10,
                fg_color="#2F2F44",
                hover_color="#3A3A5A",
                text_color="white",
                font=("Segoe UI", 14)
            )

            # Role-based access filtering — could extract later
            if self.role == "Doctor" and label not in ["Dashboard", "Medical Records"]:
                nav_btn.configure(state="disabled")
            elif self.role == "Receptionist" and label == "Doctors":
                nav_btn.configure(state="disabled")

            nav_btn.pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.quit
        ).pack(side="bottom", pady=20, padx=10, fill="x")

        # Top bar for title + user info
        self.top_bar = ctk.CTkFrame(self, height=60, fg_color="#F4F6F6")
        self.top_bar.pack(side="top", fill="x")

        ctk.CTkLabel(self.top_bar, text="Hospital Management System Dashboard", font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(self.top_bar, text=f"Logged in as: {self.username} ({self.role})", font=("Segoe UI", 12)).pack(side="right", padx=20)

        # Main display area
        self.main_panel = ctk.CTkFrame(self, corner_radius=12, fg_color="#FFFFFF")
        self.main_panel.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.show_dashboard()

        # Bottom footer
        self.footer = ctk.CTkLabel(self, text="Developed by Qubit X Innovation", font=("Segoe UI", 10), text_color="gray")
        self.footer.pack(side="bottom", pady=5)

    def clear_main_panel(self):
        for widget in self.main_panel.winfo_children():
            widget.destroy()

    def get_total_from_table(self, tbl):
        db_cursor.execute(f"SELECT COUNT(*) AS total FROM {tbl}")
        result = db_cursor.fetchone()
        return result["total"]

    def show_dashboard(self):
        self.clear_main_panel()
        ctk.CTkLabel(self.main_panel, text="📊 Dashboard Overview", font=("Segoe UI", 22, "bold")).pack(pady=20, anchor="w", padx=20)

        stats_row = ctk.CTkFrame(self.main_panel)
        stats_row.pack(padx=20, fill="x")

        self.stat_widget(stats_row, "👥 Total Patients", self.get_total_from_table("patients")).pack(side="left", padx=10, pady=20, expand=True, fill="both")
        self.stat_widget(stats_row, "🧑‍⚕️ Total Doctors", self.get_total_from_table("doctors")).pack(side="left", padx=10, pady=20, expand=True, fill="both")
        self.stat_widget(stats_row, "📅 Appointments", self.get_total_from_table("appointments")).pack(side="left", padx=10, pady=20, expand=True, fill="both")
        self.stat_widget(stats_row, "📁 Records", self.get_total_from_table("medical_records")).pack(side="left", padx=10, pady=20, expand=True, fill="both")

    def stat_widget(self, parent, title, value):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#D6EAF8")
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 14), text_color="#1B4F72").pack(pady=(12, 4))
        ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 20, "bold"), text_color="#2471A3").pack(pady=(0, 12))
        return card

    def show_patients(self):
        self.clear_main_panel()
        ctk.CTkLabel(self.main_panel, text="👥 Manage Patients", font=("Segoe UI", 22, "bold")).pack(pady=10, anchor="w", padx=20)

        form = ctk.CTkFrame(self.main_panel)
        form.pack(padx=20, pady=10)

        # Basic patient form
        name = ctk.CTkEntry(form, placeholder_text="Full Name")
        age = ctk.CTkEntry(form, placeholder_text="Age")
        gender = ctk.CTkEntry(form, placeholder_text="Gender")
        phone = ctk.CTkEntry(form, placeholder_text="Contact")
        illness = ctk.CTkEntry(form, placeholder_text="Disease")

        name.grid(row=0, column=0, padx=10, pady=5)
        age.grid(row=0, column=1, padx=10, pady=5)
        gender.grid(row=1, column=0, padx=10, pady=5)
        phone.grid(row=1, column=1, padx=10, pady=5)
        illness.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        def add_patient():
            db_cursor.execute(
                "INSERT INTO patients (name, age, gender, contact, disease) VALUES (%s, %s, %s, %s, %s)",
                (name.get(), age.get(), gender.get(), phone.get(), illness.get())
            )
            db_conn.commit()
            messagebox.showinfo("Success", "Patient added.")
            self.show_patients()

        ctk.CTkButton(form, text="Add Patient", command=add_patient, fg_color="#58D68D").grid(row=3, column=0, columnspan=2, pady=10)

    def show_doctors(self):
        self.clear_main_panel()
        ctk.CTkLabel(self.main_panel, text="🧑‍⚕️ Doctors Directory", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20, pady=20)

        form = ctk.CTkFrame(self.main_panel)
        form.pack(padx=20, pady=10)

        doc_name = ctk.CTkEntry(form, placeholder_text="Doctor Name")
        spec = ctk.CTkEntry(form, placeholder_text="Specialization")
        contact = ctk.CTkEntry(form, placeholder_text="Contact")
        avail = ctk.CTkEntry(form, placeholder_text="Availability")

        doc_name.grid(row=0, column=0, padx=10, pady=5)
        spec.grid(row=0, column=1, padx=10, pady=5)
        contact.grid(row=1, column=0, padx=10, pady=5)
        avail.grid(row=1, column=1, padx=10, pady=5)

        def save_doc():
            db_cursor.execute(
                "INSERT INTO doctors (name, specialty, contact, availability) VALUES (%s, %s, %s, %s)",
                (doc_name.get(), spec.get(), contact.get(), avail.get())
            )
            db_conn.commit()
            messagebox.showinfo("Success", "Doctor info saved.")
            self.show_doctors()

        ctk.CTkButton(form, text="Add Doctor", command=save_doc, fg_color="#5DADE2").grid(row=2, column=0, columnspan=2, pady=10)

    def show_appointments(self):
        self.clear_main_panel()
        ctk.CTkLabel(self.main_panel, text="📅 Appointments", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20, pady=20)

        form = ctk.CTkFrame(self.main_panel)
        form.pack(padx=20, pady=10)

        pname = ctk.CTkEntry(form, placeholder_text="Patient Name")
        dname = ctk.CTkEntry(form, placeholder_text="Doctor Name")
        issue = ctk.CTkEntry(form, placeholder_text="Disease")
        appt_date = ctk.CTkEntry(form, placeholder_text="Date (YYYY-MM-DD)")

        pname.grid(row=0, column=0, padx=10, pady=5)
        dname.grid(row=0, column=1, padx=10, pady=5)
        issue.grid(row=1, column=0, padx=10, pady=5)
        appt_date.grid(row=1, column=1, padx=10, pady=5)

        def add_appt():
            db_cursor.execute(
                "INSERT INTO appointments (patient_name, doctor_name, disease, date) VALUES (%s, %s, %s, %s)",
                (pname.get(), dname.get(), issue.get(), appt_date.get())
            )
            db_conn.commit()
            messagebox.showinfo("Success", "Appointment booked.")
            self.show_appointments()

        ctk.CTkButton(form, text="Schedule", command=add_appt, fg_color="#F5B041").grid(row=2, column=0, columnspan=2, pady=10)

    def show_records(self):
        self.clear_main_panel()
        ctk.CTkLabel(self.main_panel, text="📁 Medical Records", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20, pady=20)

        form = ctk.CTkFrame(self.main_panel)
        form.pack(padx=20, pady=10)

        pname = ctk.CTkEntry(form, placeholder_text="Patient Name")
        diagnosis = ctk.CTkEntry(form, placeholder_text="Diagnosis")
        treatment = ctk.CTkEntry(form, placeholder_text="Treatment")

        pname.grid(row=0, column=0, padx=10, pady=5)
        diagnosis.grid(row=1, column=0, padx=10, pady=5)
        treatment.grid(row=2, column=0, padx=10, pady=5)

        def store_record():
            db_cursor.execute(
                "INSERT INTO medical_records (patient_name, diagnosis, treatment) VALUES (%s, %s, %s)",
                (pname.get(), diagnosis.get(), treatment.get())
            )
            db_conn.commit()
            messagebox.showinfo("Success", "Record saved.")
            self.show_records()

        ctk.CTkButton(form, text="Save Record", command=store_record, fg_color="#BB8FCE").grid(row=3, column=0, pady=10)


# Boot up
if __name__ == "__main__":
    LoginPage().mainloop()
