from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import time


class student:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # ================= COLORS =================
        self.bg_color = "#F5F7FA"
        self.primary = "#1E3A5F"
        self.secondary = "#00A8E8"
        self.white = "#FFFFFF"

        self.root.config(bg=self.bg_color)

        # ================= VARIABLES =================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_sem = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radio = StringVar()

        # ================= TITLE =================
        title_lbl = Label(
            self.root,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Segoe UI", 28, "bold"),
            bg=self.primary,
            fg="white"
        )
        title_lbl.place(x=0, y=0, width=1530, height=60)

        # ================= MAIN FRAME =================
        main_frame = Frame(self.root, bd=0, bg=self.bg_color)
        main_frame.place(x=10, y=70, width=1500, height=700)

        # ================= LEFT FRAME =================
        left_frame = LabelFrame(
            main_frame,
            bd=2,
            bg=self.white,
            relief=RIDGE,
            text=" Student Details ",
            font=("Segoe UI", 14, "bold"),
            fg=self.primary
        )
        left_frame.place(x=10, y=10, width=730, height=670)

        # ================= COURSE FRAME =================
        course_frame = LabelFrame(
            left_frame,
            bd=2,
            bg=self.white,
            relief=RIDGE,
            text="Current Course Information",
            font=("Segoe UI", 12, "bold"),
            fg=self.primary
        )
        course_frame.place(x=10, y=10, width=705, height=130)

        # Department
        Label(course_frame, text="Department",
              font=("Segoe UI", 11, "bold"),
              bg=self.white).grid(row=0, column=0, padx=10, pady=10)

        dep_combo = ttk.Combobox(
            course_frame,
            textvariable=self.var_dep,
            width=18,
            font=("Segoe UI", 10),
            state="readonly"
        )

        dep_combo["values"] = (
            "Select Department",
            "Computer",
            "CSIT",
            "Civil",
            "Mechanical"
        )

        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10)

        # Course
        Label(course_frame, text="Course",
              font=("Segoe UI", 11, "bold"),
              bg=self.white).grid(row=0, column=2, padx=10)

        course_combo = ttk.Combobox(
            course_frame,
            textvariable=self.var_course,
            width=18,
            font=("Segoe UI", 10),
            state="readonly"
        )

        course_combo["values"] = (
            "Select Course",
            "B.Tech",
            "M.Tech",
            "Diploma"
        )

        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=10)

        # Year
        Label(course_frame, text="Year",
              font=("Segoe UI", 11, "bold"),
              bg=self.white).grid(row=1, column=0, padx=10, pady=10)

        year_combo = ttk.Combobox(
            course_frame,
            textvariable=self.var_year,
            width=18,
            font=("Segoe UI", 10),
            state="readonly"
        )

        year_combo["values"] = (
            "Select Year",
            "2023-24",
            "2024-25",
            "2025-26"
        )

        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=10)

        # Semester
        Label(course_frame, text="Semester",
              font=("Segoe UI", 11, "bold"),
              bg=self.white).grid(row=1, column=2, padx=10)

        sem_combo = ttk.Combobox(
            course_frame,
            textvariable=self.var_sem,
            width=18,
            font=("Segoe UI", 10),
            state="readonly"
        )

        sem_combo["values"] = (
            "Select Semester",
            "1st",
            "2nd",
            "3rd",
            "4th"
        )

        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=10)

        # ================= STUDENT INFO FRAME =================
        class_frame = LabelFrame(
            left_frame,
            bd=2,
            bg=self.white,
            relief=RIDGE,
            text="Class Student Information",
            font=("Segoe UI", 12, "bold"),
            fg=self.primary
        )

        class_frame.place(x=10, y=150, width=705, height=490)

        # ================= LABELS & ENTRIES =================

        labels = [
            ("Student ID", self.var_std_id),
            ("Student Name", self.var_std_name),
            ("Division", self.var_div),
            ("Roll No", self.var_roll),
            ("Gender", self.var_gender),
            ("DOB", self.var_dob),
            ("Email", self.var_email),
            ("Phone", self.var_phone),
            ("Address", self.var_address),
            ("Teacher", self.var_teacher),
        ]

        row = 0
        col = 0

        for text, variable in labels:

            Label(
                class_frame,
                text=text,
                font=("Segoe UI", 10, "bold"),
                bg=self.white
            ).grid(row=row, column=col, padx=10, pady=10, sticky=W)

            ttk.Entry(
                class_frame,
                textvariable=variable,
                width=22,
                font=("Segoe UI", 10)
            ).grid(row=row, column=col + 1, padx=10, pady=10)

            if col == 0:
                col = 2
            else:
                col = 0
                row += 1

        # ================= RADIO BUTTON =================
        ttk.Radiobutton(
            class_frame,
            text="Take Photo Sample",
            variable=self.var_radio,
            value="Yes"
        ).place(x=20, y=260)

        ttk.Radiobutton(
            class_frame,
            text="No Photo Sample",
            variable=self.var_radio,
            value="No"
        ).place(x=220, y=260)

        # ================= BUTTON FRAME =================
        btn_frame = Frame(class_frame, bg=self.white)
        btn_frame.place(x=10, y=320, width=670, height=120)

        Button(
            btn_frame,
            text="Save",
            command=self.add_data,
            font=("Segoe UI", 11, "bold"),
            bg="#198754",
            fg="white",
            cursor="hand2",
            width=15
        ).grid(row=0, column=0, padx=5, pady=10)

        Button(
            btn_frame,
            text="Update",
            command=self.update_data,
            font=("Segoe UI", 11, "bold"),
            bg="#0D6EFD",
            fg="white",
            cursor="hand2",
            width=15
        ).grid(row=0, column=1, padx=5)

        Button(
            btn_frame,
            text="Delete",
            command=self.delete_data,
            font=("Segoe UI", 11, "bold"),
            bg="#DC3545",
            fg="white",
            cursor="hand2",
            width=15
        ).grid(row=0, column=2, padx=5)

        Button(
            btn_frame,
            text="Reset",
            command=self.reset_data,
            font=("Segoe UI", 11, "bold"),
            bg="#6C757D",
            fg="white",
            cursor="hand2",
            width=15
        ).grid(row=0, column=3, padx=5)

        Button(
            btn_frame,
            text="Take Photo Sample",
            command=self.generate_dataset,
            font=("Segoe UI", 11, "bold"),
            bg=self.primary,
            fg="white",
            cursor="hand2",
            width=30
        ).grid(row=1, column=0, columnspan=2, pady=20)

        Button(
            btn_frame,
            text="Update Photo Sample",
            font=("Segoe UI", 11, "bold"),
            bg=self.secondary,
            fg="white",
            cursor="hand2",
            width=30
        ).grid(row=1, column=2, columnspan=2)

        # ================= RIGHT FRAME =================
        right_frame = LabelFrame(
            main_frame,
            bd=2,
            bg=self.white,
            relief=RIDGE,
            text=" Student Details ",
            font=("Segoe UI", 14, "bold"),
            fg=self.primary
        )

        right_frame.place(x=760, y=10, width=720, height=670)

        # ================= SEARCH FRAME =================
        search_frame = LabelFrame(
            right_frame,
            bd=2,
            bg=self.white,
            relief=RIDGE,
            text="Search System",
            font=("Segoe UI", 12, "bold"),
            fg=self.primary
        )

        search_frame.place(x=10, y=10, width=690, height=80)

        Label(
            search_frame,
            text="Search By",
            font=("Segoe UI", 11, "bold"),
            bg=self.white
        ).grid(row=0, column=0, padx=10)

        search_combo = ttk.Combobox(
            search_frame,
            width=15,
            font=("Segoe UI", 10),
            state="readonly"
        )

        search_combo["values"] = (
            "Select",
            "Roll No",
            "Department"
        )

        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=10)

        ttk.Entry(
            search_frame,
            width=20,
            font=("Segoe UI", 10)
        ).grid(row=0, column=2, padx=10)

        Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg=self.primary,
            fg="white",
            cursor="hand2",
            width=12
        ).grid(row=0, column=3, padx=5)

        Button(
            search_frame,
            text="Show All",
            font=("Segoe UI", 10, "bold"),
            bg=self.secondary,
            fg="white",
            cursor="hand2",
            width=12
        ).grid(row=0, column=4, padx=5)

        # ================= TABLE FRAME =================
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=10, y=110, width=690, height=530)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_tabel = ttk.Treeview(
            table_frame,
            columns=(
                "dep", "course", "year", "sem",
                "id", "name", "div", "roll",
                "gender", "dob", "email",
                "phone", "address", "teacher", "photo"
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_tabel.xview)
        scroll_y.config(command=self.student_tabel.yview)

        headings = [
            "Department", "Course", "Year", "Semester",
            "Student ID", "Name", "Division", "Roll",
            "Gender", "DOB", "Email", "Phone",
            "Address", "Teacher", "Photo"
        ]

        cols = [
            "dep", "course", "year", "sem",
            "id", "name", "div", "roll",
            "gender", "dob", "email",
            "phone", "address", "teacher", "photo"
        ]

        for col, heading in zip(cols, headings):
            self.student_tabel.heading(col, text=heading)
            self.student_tabel.column(col, width=120)

        self.student_tabel["show"] = "headings"

        self.student_tabel.pack(fill=BOTH, expand=1)

        self.student_tabel.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    # ================= ADD DATA =================
    def add_data(self):

        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_id.get() == ""
            or self.var_std_name.get() == ""
        ):

            messagebox.showerror(
                "Error",
                "All Fields Are Required",
                parent=self.root
            )

            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MYsql@6264",
                database="face_recognizer"
            )

            my_cursor = conn.cursor()

            my_cursor.execute(
                "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_sem.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio.get()
                )
            )

            conn.commit()
            self.fetch_data()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student Details Added Successfully",
                parent=self.root
            )

        except Exception as es:

            messagebox.showerror(
                "Error",
                f"Due To : {str(es)}",
                parent=self.root
            )

    # ================= FETCH DATA =================
    def fetch_data(self):

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MYsql@6264",
            database="face_recognizer"
        )

        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")

        data = my_cursor.fetchall()

        if len(data) != 0:

            self.student_tabel.delete(*self.student_tabel.get_children())

            for i in data:
                self.student_tabel.insert("", END, values=i)

            conn.commit()

        conn.close()

    # ================= GET CURSOR =================
    def get_cursor(self, event=""):

        cursor_focus = self.student_tabel.focus()
        content = self.student_tabel.item(cursor_focus)
        data = content["values"]

        if len(data) == 0:
            return

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_sem.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_div.set(data[6])
        self.var_roll.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_email.set(data[10])
        self.var_phone.set(data[11])
        self.var_address.set(data[12])
        self.var_teacher.set(data[13])
        self.var_radio.set(data[14])

    # ================= UPDATE =================
    def update_data(self):

        messagebox.showinfo(
            "Update",
            "Update Function Working",
            parent=self.root
        )

    # ================= DELETE =================
    def delete_data(self):

        if self.var_std_id.get() == "":

            messagebox.showerror(
                "Error",
                "Student ID Required",
                parent=self.root
            )

            return

        try:

            delete = messagebox.askyesno(
                "Delete",
                "Do You Want To Delete?",
                parent=self.root
            )

            if delete:

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="MYsql@6264",
                    database="face_recognizer"
                )

                my_cursor = conn.cursor()

                sql = "delete from student where student_id=%s"
                value = (self.var_std_id.get(),)

                my_cursor.execute(sql, value)

                conn.commit()
                conn.close()

                self.fetch_data()
                self.reset_data()

                messagebox.showinfo(
                    "Deleted",
                    "Student Deleted Successfully",
                    parent=self.root
                )

        except Exception as es:

            messagebox.showerror(
                "Error",
                f"Due To : {str(es)}",
                parent=self.root
            )

    # ================= RESET =================
    def reset_data(self):

        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("")
        self.var_roll.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio.set("")

    # ================= GENERATE DATASET =================
    def generate_dataset(self):

        if (self.var_dep.get() == "Select Department" or
           self.var_std_id.get() == "" or
           self.var_std_name.get() == "" or
           self.var_roll.get() == ""):

           messagebox.showerror("Error", "All Fields are required!", parent=self.root)

        else:
          try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MYsql@6264",
                database="face_recognizer"
            )

            my_cursor = conn.cursor()

            # ================= UPDATE STUDENT =================
            my_cursor.execute("""
                UPDATE student SET
                depatment=%s,
                course=%s,
                year=%s,
                semestor=%s,
                name=%s,
                division=%s,
                roll=%s,
                gender=%s,
                dob=%s,
                email=%s,
                phone=%s,
                address=%s,
                teacher=%s,
                photsample=%s
                WHERE student_id=%s
            """, (
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_sem.get(),
                self.var_std_name.get(),
                self.var_div.get(),
                self.var_roll.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_radio.get(),
                self.var_std_id.get()
            ))

            conn.commit()
            self.fetch_data()
            conn.close()

            # ================= CREATE DATA FOLDER =================
            os.makedirs("data", exist_ok=True)

            face_classifier = cv2.CascadeClassifier(
                "haarcascade_frontalface_default.xml"
            )

            def face_cropped(img):

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_classifier.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5
                )

                largest_face = None
                max_area = 0

                for (x, y, w, h) in faces:

                    area = w * h

                    # Take biggest/front face only
                    if area > max_area:
                        max_area = area
                        largest_face = (x, y, w, h)

                if largest_face is not None:

                    x, y, w, h = largest_face

                    # Extra margin to avoid too close crop
                    padding = 40
                    x1 = max(0, x - padding)
                    y1 = max(0, y - padding)

                    x2 = min(img.shape[1], x + w + padding)
                    y2 = min(img.shape[0], y + h + padding)

                    return img[y1:y2, x1:x2]

                return None

             # ================= CAMERA =================
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                messagebox.showerror("Error", "Webcam not found!")
                return

            img_id = 0 

            

            while True:

                ret, my_frame = cap.read()

                if not ret:
                    break

                cropped_face = face_cropped(my_frame)

                if cropped_face is not None:

                    img_id += 1

                    # Resize
                    face = cv2.resize(cropped_face, (500, 500))

                    # COLOR IMAGE SAVE
                    file_name_path = f"data/user.{self.var_std_id.get()}.{img_id}.jpg"

                    cv2.imwrite(file_name_path, face)

                    # Display count
                    cv2.putText(
                        face,
                        f"Photo {img_id}/10",
                        (20, 40),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )
                    cv2.imshow("Capturing Faces", face)

                    # ===== 1 SECOND DELAY =====
                    time.sleep(1)

                # Stop after 10 photos
                if img_id == 10:
                    break

                # ENTER key exit
                if cv2.waitKey(1) == 13:
                    break

            cap.release()
            cv2.destroyAllWindows()

            messagebox.showinfo(
                "Result",
                "10 Face Samples Collected Successfully!"
            )
          except Exception as es:

            messagebox.showerror(
                "Error",
                f"Due to: {str(es)}",
                parent=self.root
            )  


if __name__ == "__main__":

    root = Tk()
    obj = student(root)
    root.mainloop()