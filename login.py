from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys


class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Login")
        self.root.configure(bg="#0A1628")

        # ─── Hardcoded credentials (aap database se bhi le sakte hain) ───
        self.VALID_USERNAME = "admin"
        self.VALID_PASSWORD = "admin123"

        # ─── Background gradient effect (canvas) ───
        self.canvas = Canvas(self.root, width=1530, height=790, bg="#0A1628", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Decorative circles (depth effect)
        self.canvas.create_oval(-100, -100, 500, 500, fill="#0D2137", outline="")
        self.canvas.create_oval(1100, 400, 1700, 950, fill="#0D2137", outline="")

        # ─── Left side – branding panel ───
        left_frame = Frame(self.root, bg="#0D2137", width=680, height=790)
        left_frame.place(x=0, y=0)

        # Title text
        Label(left_frame,
              text="FACE RECOGNITION",
              font=("Georgia", 30, "bold"),
              bg="#0D2137", fg="#4A9EDB").place(x=60, y=200)

        Label(left_frame,
              text="ATTENDANCE SYSTEM",
              font=("Georgia", 28, "bold"),
              bg="#0D2137", fg="white").place(x=60, y=255)

        Label(left_frame,
              text="Secure  ·  Fast  ·  Accurate",
              font=("times new roman", 14),
              bg="#0D2137", fg="#6B8FA8").place(x=60, y=320)

        # Decorative line
        Frame(left_frame, bg="#4A9EDB", width=80, height=3).place(x=60, y=370)

        Label(left_frame,
              text="Apni attendance record karo\nbina kisi extra effort ke.\nSirf apna chehra dikhaao!",
              font=("times new roman", 13),
              bg="#0D2137", fg="#8FAEC0",
              justify=LEFT).place(x=60, y=400)

        # ─── Right side – login card ───
        card = Frame(self.root, bg="white", width=500, height=560,
                     relief="flat", bd=0)
        card.place(x=760, y=115)
        card.pack_propagate(False)

        # Card header
        header = Frame(card, bg="#1565C0", height=90)
        header.pack(fill=X)

        Label(header,
              text="Admin Login",
              font=("times new roman", 20, "bold"),
              bg="#1565C0", fg="white").pack(pady=28)

        # Form area
        form = Frame(card, bg="white", padx=50)
        form.pack(fill=BOTH, expand=True)

        # Username
        Label(form, text="Username", font=("times new roman", 12),
              bg="white", fg="#374151", anchor=W).pack(fill=X, pady=(30, 4))

        self.username_var = StringVar()
        username_entry = Entry(form, textvariable=self.username_var,
                               font=("times new roman", 13),
                               bd=1, relief="solid",
                               highlightthickness=2,
                               highlightcolor="#1565C0",
                               highlightbackground="#D1D5DB",
                               fg="#111827", bg="#F9FAFB")
        username_entry.pack(fill=X, ipady=8)
        username_entry.focus()

        # Password
        Label(form, text="Password", font=("times new roman", 12),
              bg="white", fg="#374151", anchor=W).pack(fill=X, pady=(20, 4))

        self.password_var = StringVar()
        self.password_entry = Entry(form, textvariable=self.password_var,
                                    show="*",
                                    font=("times new roman", 13),
                                    bd=1, relief="solid",
                                    highlightthickness=2,
                                    highlightcolor="#1565C0",
                                    highlightbackground="#D1D5DB",
                                    fg="#111827", bg="#F9FAFB")
        self.password_entry.pack(fill=X, ipady=8)

        # Show/Hide password checkbox
        self.show_pass = BooleanVar()
        Checkbutton(form, text="Show Password",
                    variable=self.show_pass,
                    command=self.toggle_password,
                    font=("times new roman", 11),
                    bg="white", fg="#6B7280",
                    activebackground="white",
                    cursor="hand2").pack(anchor=W, pady=(8, 0))

        # Login button
        login_btn = Button(form,
                           text="LOGIN",
                           command=self.check_login,
                           font=("times new roman", 14, "bold"),
                           bg="#1565C0", fg="white",
                           activebackground="#0D47A1",
                           activeforeground="white",
                           relief="flat", cursor="hand2",
                           bd=0)
        login_btn.pack(fill=X, ipady=10, pady=(25, 0))

        # Hover effects
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#0D47A1"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#1565C0"))

        # Enter key shortcut
        self.root.bind("<Return>", lambda e: self.check_login())

        # Footer
        Label(card,
              text="© 2024 Face Recognition Attendance System",
              font=("times new roman", 9),
              bg="white", fg="#9CA3AF").pack(pady=20)

        # Status label (for error messages)
        self.status_var = StringVar()
        self.status_label = Label(form, textvariable=self.status_var,
                                  font=("times new roman", 11),
                                  bg="white", fg="red")
        self.status_label.pack(pady=(10, 0))

    # ─── Toggle password visibility ───
    def toggle_password(self):
        if self.show_pass.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    # ─── Login verification ───
    def check_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            self.status_var.set("⚠ Username aur Password dono bharein!")
            return

        if username == self.VALID_USERNAME and password == self.VALID_PASSWORD:
            self.status_var.set("")
            messagebox.showinfo("Welcome", f"Welcome, {username}!\nLogin successful.")
            self.open_main_system()
        else:
            self.status_var.set("✗ Galat username ya password!")
            self.password_var.set("")
            self.password_entry.focus()

    # ─── Open main system ───
    def open_main_system(self):
        self.root.destroy()
        # Main system import aur launch
        from main import Face_recognition_system   # <-- aapki main file ka naam
        new_root = Tk()
        Face_recognition_system(new_root)
        new_root.mainloop()


# ─── Entry point ───
if __name__ == "__main__":
    root = Tk()
    Login(root)
    root.mainloop()