from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog


class Attendance:
    def __init__(self, root):   
        self.root = root
        self.root.geometry("1530x790+0+0") 
        self.root.title("Face Recognition System")


        # ================= Variables =================
        self.var_atten_id = StringVar()
        self.var_atten_roll = StringVar()
        self.var_atten_name = StringVar()
        self.var_atten_dep = StringVar()
        self.var_atten_time = StringVar()
        self.var_atten_date = StringVar()
        self.var_atten_attendance = StringVar()


        # ===== Top Images =====
        img1 = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (3).jpg")
        img1 = img1.resize((600, 120))
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(self.root, image=self.photoimg1)
        f_lbl1.place(x=0, y=0, width=600, height=120)

        img2 = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (3).jpg")
        img2 = img2.resize((600, 120))
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(self.root, image=self.photoimg2)
        f_lbl2.place(x=600, y=0, width=600, height=120)

        # ===== Title =====
        title_lbl = Label(self.root, text="ATTENDANCE MANAGEMENT SYSTEM",
                          font=("times new roman", 28, "bold"),
                          bg="white", fg="green")
        title_lbl.place(x=0, y=120, width=1200, height=50)

        # ===== Main Frame =====
        main_frame = Frame(self.root, bd=2)
        main_frame.place(x=10, y=180, width=1180, height=500)

        # ===== Left Frame =====
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,
                                text="Student Attendance Details",
                                font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=580, height=480)

        # ===== Left Image =====
        img3 = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (3).jpg")
        img3 = img3.resize((570, 150))
        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl3 = Label(left_frame, image=self.photoimg3)
        f_lbl3.place(x=5, y=0, width=570, height=150)

        # ===== Form =====
        Label(left_frame, text="AttendanceId:", font=("times new roman", 12)).place(x=10, y=170)
        self.attendance_id = Entry(left_frame, width=20,textvariable=self.var_atten_id)
        self.attendance_id.place(x=130, y=170)

        Label(left_frame, text="Roll:", font=("times new roman", 12)).place(x=300, y=170)
        self.roll = Entry(left_frame, width=20,textvariable=self.var_atten_roll)
        self.roll.place(x=380, y=170)

        Label(left_frame, text="Name:", font=("times new roman", 12)).place(x=10, y=210)
        self.name = Entry(left_frame, width=20,textvariable=self.var_atten_name)
        self.name.place(x=130, y=210)

        Label(left_frame, text="Department:", font=("times new roman", 12)).place(x=300, y=210)
        self.dept = Entry(left_frame, width=20,textvariable=self.var_atten_dep)
        self.dept.place(x=380, y=210)

        Label(left_frame, text="Time:", font=("times new roman", 12)).place(x=10, y=250)
        self.time = Entry(left_frame, width=20,textvariable=self.var_atten_time)
        self.time.place(x=130, y=250)

        Label(left_frame, text="Date:", font=("times new roman", 12)).place(x=300, y=250)
        self.date = Entry(left_frame, width=20,textvariable=self.var_atten_date)
        self.date.place(x=380, y=250)

        Label(left_frame, text="Status:", font=("times new roman", 12)).place(x=10, y=290)
        self.status = ttk.Combobox(left_frame, width=18,textvariable=self.var_atten_attendance , state="readonly")
        self.status["values"] = ("Present", "Absent")
        self.status.current(0)
        self.status.place(x=130, y=290)

        # ===== Buttons =====
        btn_frame = Frame(left_frame, bd=2, relief=RIDGE)
        btn_frame.place(x=5, y=330, width=570, height=40)

        Button(btn_frame, text="Import CSV",command=self.importCsv, width=14, bg="blue", fg="white").grid(row=0, column=0)
        Button(btn_frame, text="Export CSV",command=self.exportCsv, width=14, bg="blue", fg="white").grid(row=0, column=1)
        Button(btn_frame, text="Update", width=14, bg="blue", fg="white").grid(row=0, column=2)
        Button(btn_frame, text="Reset",command=self.reset_data, width=14, bg="blue", fg="white").grid(row=0, column=3)

        # ===== Right Frame =====
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,
                                 text="Attendance Details",
                                 font=("times new roman", 12, "bold"))
        right_frame.place(x=600, y=10, width=560, height=480)

        # ===== Table =====
        scroll_x = Scrollbar(right_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(right_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(right_frame,
                                             columns=("id", "roll", "name", "dept", "time", "date", "status"),
                                             xscrollcommand=scroll_x.set,
                                             yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table.heading("id", text="Attendance ID")
        self.attendance_table.heading("roll", text="Roll")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("dept", text="Department")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("status", text="Attendance")

        self.attendance_table["show"] = "headings"

        for col in ("id", "roll", "name", "dept", "time", "date", "status"):
            self.attendance_table.column(col, width=100)

        self.attendance_table.pack(fill=BOTH, expand=1)
        self.attendance_table.bind("<ButtonRelease>",self.get_cursor)
 
# ======== fetch data====
    # ======== fetch data====
    def fetchData(self, rows):
      self.attendance_table.delete(*self.attendance_table.get_children())
      for i in rows:
        self.attendance_table.insert("", END, values=i)


# ======== import csv====
    def importCsv(self):
      global mydata
      mydata = []   # clear old data

      fln = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Open CSV",
        filetypes=(("CSV File", "*.csv"), ("ALL File", "*.*")),
        parent=self.root
    )

      if fln == "":
        return

      with open(fln) as myfile:
        csvread = csv.reader(myfile, delimiter=",")
        for i in csvread:
            mydata.append(i)

      self.fetchData(mydata)



      # export csv
    def exportCsv(self):
       try:
          if len(mydata) < 1:
            messagebox.showerror("No Data", "No Data found to export", parent=self.root)
            return False

          fln = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),parent=self.root
        )

          with open(fln, mode="w", newline="") as myfile:
            exp_write = csv.writer(myfile, delimiter=",")
            for i in mydata:
                exp_write.writerow(i)

          messagebox.showinfo(
            "Data Export",
            "Your data exported to " + os.path.basename(fln) + " successfully"
        )

       except Exception as es:
        messagebox.showerror("Error", f"Due To : {str(es)}", parent=self.root)

    def get_cursor(self, event=""):
     cursor_row = self.attendance_table.focus()
     content = self.attendance_table.item(cursor_row)
     rows = content['values']

     self.var_atten_id.set(rows[0])
     self.var_atten_roll.set(rows[1])
     self.var_atten_name.set(rows[2])
     self.var_atten_dep.set(rows[3])
     self.var_atten_time.set(rows[4])
     self.var_atten_date.set(rows[5])
     self.var_atten_attendance.set(rows[6]) 

    def reset_data(self):
     self.var_atten_id.set("")
     self.var_atten_roll.set("")
     self.var_atten_name.set("")
     self.var_atten_dep.set("")
     self.var_atten_time.set("")
     self.var_atten_date.set("")
     self.var_atten_attendance.set("") 
          


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()