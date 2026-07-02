
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from sample import student
import os
from train1 import Train
#from Face_recognition1 import Face_Recognition
from face1 import Face_Recognition
from attendance import Attendance
from paa import Dashboard
from help import HelpDesk


class Face_recognition_system:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("AI Face Recognition Attendance System")

        # ================= COLORS =================
        self.bg_color = "#0f172a"
        self.card_color = "#1e293b"
        self.btn_color = "#2563eb"
        self.hover_color = "#1d4ed8"
        self.text_color = "white"

        # ================= HEADER =================

        header = Frame(self.root, bg="#020617")
        header.place(x=0, y=0, width=1530, height=130)

        # LEFT IMAGE
        img = Image.open(
            r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP.jpg"
        )
        img = img.resize((300, 120), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        Label(
            header,
            image=self.photoimg,
            bd=0
        ).place(x=10, y=5, width=300, height=120)

        # CENTER TITLE
        title = Label(
            header,
            text="FACE RECOGNITION ATTENDANCE SYSTEM",
            font=("times new roman", 32, "bold"),
            bg="#020617",
            fg="cyan"
        )
        title.place(x=320, y=20)

        subtitle = Label(
            header,
            text="AI Powered Smart Attendance Management",
            font=("times new roman", 16, "bold"),
            bg="#020617",
            fg="white"
        )
        subtitle.place(x=520, y=75)

        # RIGHT IMAGE
        img2 = Image.open(
            r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (2).jpg"
        )
        img2 = img2.resize((300, 120), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        Label(
            header,
            image=self.photoimg2,
            bd=0
        ).place(x=1210, y=5, width=300, height=120)

        # ================= BACKGROUND =================

        bg_img = Image.open(
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (6).jpg"
        )

        bg_img = bg_img.resize((1530, 710), Image.Resampling.LANCZOS)

        self.bg_photo = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=130, width=1530, height=710)

        # Overlay
        overlay = Frame(bg_label, bg="#000000")
        overlay.place(x=0, y=0, width=1530, height=710)

        # ================= DASHBOARD TITLE =================

        dash_title = Label(
            overlay,
            text="Dashboard",
            font=("times new roman", 30, "bold"),
            bg="#000000",
            fg="white"
        )
        dash_title.place(x=650, y=20)

        # ================= BUTTON SECTION =================

        # ROW 1
        self.create_card(
            overlay,
            120,
            100,
            "Student Details",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (2).jpg",
            self.student_details
        )

        self.create_card(
            overlay,
            470,
            100,
            "Face Detector",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (1).jpg",
            self.face_data
        )

        self.create_card(
            overlay,
            820,
            100,
            "Attendance Report",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (4).jpg",
            self.attendance_data
        )

        self.create_card(
            overlay,
            1170,
            100,
            "Help Desk",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (8).jpg",
            self.help_desk
        )

        # ROW 2
        self.create_card(
            overlay,
            120,
            390,
            "Train Data",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP.jpg",
            self.train_data
        )

        self.create_card(
            overlay,
            470,
            390,
            "Photos",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (3).jpg",
            self.open_img
        )

        self.create_card(
            overlay,
            820,
            390,
            "Dashboard",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (7).jpg",
            self.open_dashboard
        )

        self.create_card(
            overlay,
            1170,
            390,
            "Exit",
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (5).jpg",
            self.iExit
        )

        # ================= FOOTER =================

        footer = Label(
            overlay,
            text="Developed By Vikram Patel | AI Attendance System",
            font=("times new roman", 12, "bold"),
            bg="#020617",
            fg="white"
        )

        footer.place(x=0, y=670, width=1530, height=40)

    # ================= CARD FUNCTION =================

    def create_card(self, parent, x, y, text, image_path, command):

        card = Frame(
            parent,
            bg=self.card_color,
            bd=0,
            cursor="hand2"
        )

        card.place(x=x, y=y, width=250, height=250)

        # IMAGE
        img = Image.open(image_path)
        img = img.resize((220, 170), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(img)

        img_btn = Button(
            card,
            image=photo,
            bd=0,
            cursor="hand2",
            command=command
        )

        img_btn.image = photo
        img_btn.place(x=15, y=15, width=220, height=170)

        # TEXT BUTTON
        txt_btn = Button(
            card,
            text=text,
            font=("times new roman", 16, "bold"),
            bg=self.btn_color,
            fg="white",
            activebackground=self.hover_color,
            activeforeground="white",
            cursor="hand2",
            bd=0,
            command=command
        )

        txt_btn.place(x=15, y=195, width=220, height=40)

    # ================= FUNCTIONS =================

    def open_img(self):

        if os.path.exists("data"):

            os.startfile("data")

        else:

            messagebox.showerror(
                "Error",
                "Data folder not found"
            )

    def student_details(self):

        new_window = Toplevel(self.root)

        student(new_window)

    def train_data(self):

        new_window = Toplevel(self.root)

        Train(new_window)

    def face_data(self):

        new_window = Toplevel(self.root)

        Face_Recognition(new_window)

    def attendance_data(self):

        new_window = Toplevel(self.root)

        Attendance(new_window)

    def open_dashboard(self):

        self.new_window = Toplevel(self.root)

        self.app = Dashboard(self.new_window)

    def help_desk(self):
        self.new_window = Toplevel(self.root)

        self.app = HelpDesk(self.new_window)


      

    def iExit(self):

        exit_confirm = messagebox.askyesno(
            "Face Recognition",
            "Are you sure you want to exit?"
        )

        if exit_confirm:
            self.root.destroy()


# ================= MAIN =================

if __name__ == "__main__":

    root = Tk()

    obj = Face_recognition_system(root)

    root.mainloop()
      