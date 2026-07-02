from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2



class student:
    def __init__(self, root):   
        self.root = root
        self.root.geometry("1530x790+0+0") 
        self.root.title("Face Recognition System")



         # ================== VARIABLES ==================
        # Fix 2: Variables to store entry data for validation
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

        # --- Top Three Images ---
        img = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP.jpg")
        img = img.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photoimg).place(x=0, y=0, width=500, height=130)

        img1 = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (2).jpg")
        img1 = img1.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1).place(x=500, y=0, width=500, height=130)

        img2 = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (1).jpg")
        img2 = img2.resize((550, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2).place(x=1000, y=0, width=550, height=130)

        # --- Background and Title ---
        img3 = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (3).jpg")
        img3 = img3.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        
        bg_image = Label(self.root, image=self.photoimg3)
        bg_image.place(x=0, y=130, width=1530, height=710)

        title_lbl = Label(bg_image, text="STUDENT MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(bg_image, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1500, height=600)

        # ================== LEFT SIDE FRAME ==================
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details", font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=730, height=580)

        img_left = Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (1).jpg")
        img_left = img_left.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        Label(left_frame, image=self.photoimg_left).place(x=5, y=0, width=720, height=130)

        # Current Course Info
        course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Current course information", font=("times new roman", 12, "bold"))
        course_frame.place(x=5, y=135, width=715, height=115)

        Label(course_frame, text="Department", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, sticky=W)
        dep_combo = ttk.Combobox(course_frame, textvariable=self.var_dep,font=("times new roman", 12), state="readonly", width=18)
        dep_combo["values"] = ("Select Department", "Computer", "CSIT", "Civil", "Mechanical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10)

        Label(course_frame, text="Course", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=2, padx=10, sticky=W)
        course_combo = ttk.Combobox(course_frame, textvariable=self.var_course, font=("times new roman", 12), state="readonly", width=18)
        course_combo["values"] = ("Select Course", "B.Tech", "M.Tech", "Diploma")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10)

        Label(course_frame, text="Year", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, sticky=W)
        year_combo = ttk.Combobox(course_frame, textvariable=self.var_year, font=("times new roman", 12), state="readonly", width=18)
        year_combo["values"] = ("Select Year", "2023-24", "2024-25", "2025-26")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10)

        Label(course_frame, text="Semester", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=2, padx=10, sticky=W)
        sem_combo = ttk.Combobox(course_frame, textvariable=self.var_sem, font=("times new roman", 12), state="readonly", width=18)
        sem_combo["values"] = ("Select Semester", "1st", "2nd", "3rd", "4th")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=2, pady=10)

        # Class Student Info
        class_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Class Student information", font=("times new roman", 12, "bold"))
        class_frame.place(x=5, y=255, width=715, height=300)

        # Row 0: ID and Name
        Label(class_frame, text="StudentID:", font=("times new roman", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame, textvariable=self.var_std_id, width=20, font=("times new roman", 11)).grid(row=0, column=1, padx=5, pady=5)

        Label(class_frame, text="Student Name:", font=("times new roman", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_std_name, width=20, font=("times new roman", 11)).grid(row=0, column=3, padx=5, pady=5)

        # Row 1: Division and Roll
        Label(class_frame, text="Class Division:", font=("times new roman", 11, "bold"), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_div,width=20, font=("times new roman", 11)).grid(row=1, column=1, padx=5, pady=5)

        Label(class_frame, text="Roll No:", font=("times new roman", 11, "bold"), bg="white").grid(row=1, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_roll, width=20, font=("times new roman", 11)).grid(row=1, column=3, padx=5, pady=5)
       

        # Row 2: Gender and DOB
        Label(class_frame, text="Gender:", font=("times new roman", 11, "bold"), bg="white").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_gender, width=20, font=("times new roman", 11)).grid(row=2, column=1, padx=5, pady=5)

        Label(class_frame, text="DOB:", font=("times new roman", 11, "bold"), bg="white").grid(row=2, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_dob, width=20, font=("times new roman", 11)).grid(row=2, column=3, padx=5, pady=5)

        # Row 3: Email and Phone
        Label(class_frame, text="Email:", font=("times new roman", 11, "bold"), bg="white").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_email, width=20, font=("times new roman", 11)).grid(row=3, column=1, padx=5, pady=5)

        Label(class_frame, text="Phone No:", font=("times new roman", 11, "bold"), bg="white").grid(row=3, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_phone, width=20, font=("times new roman", 11)).grid(row=3, column=3, padx=5, pady=5)

        # Row 4: Address and Teacher
        Label(class_frame, text="Address:", font=("times new roman", 11, "bold"), bg="white").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_address, width=20, font=("times new roman", 11)).grid(row=4, column=1, padx=5, pady=5)

        Label(class_frame, text="Teacher Name:", font=("times new roman", 11, "bold"), bg="white").grid(row=4, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(class_frame,textvariable=self.var_teacher, width=20, font=("times new roman", 11)).grid(row=4, column=3, padx=5, pady=5)

        # Radio Buttons
        self.var_radio = StringVar()
        ttk.Radiobutton(class_frame,variable=self.var_radio, text="Take Photo Sample",  value="Yes").place(x=5, y=175)
        ttk.Radiobutton(class_frame,variable=self.var_radio, text="No Photo Sample",  value="No").place(x=150, y=175)

        # Button Frames
        btn_frame = Frame(class_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=200, width=710, height=35)

        Button(btn_frame, text="Save",command=self.add_data, width=17, font=("arial", 11, "bold"), bg="blue", fg="white").grid(row=0, column=0)
        Button(btn_frame, text="Update", command=self.update_data,
       width=17, font=("arial", 11, "bold"), bg="blue", fg="white").grid(row=0, column=1)

        Button(btn_frame, text="Delete",command=self.delete_data, width=17, font=("arial", 11, "bold"), bg="blue", fg="white").grid(row=0, column=2)
        Button(btn_frame, text="Reset",command=self.reset_data, width=17, font=("arial", 11, "bold"), bg="blue", fg="white").grid(row=0, column=3)

        btn_frame2 = Frame(class_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame2.place(x=0, y=235, width=710, height=35)
        Button(btn_frame2,command=self.generate_dataset, text="Take Photo Sample", width=35, font=("arial", 11, "bold"), bg="blue", fg="white").grid(row=0, column=0)
        Button(btn_frame2, text="Update Photo Sample", width=35, font=("arial", 11, "bold"), bg="blue", fg="white").grid(row=0, column=1)



        # right side frame
        right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="student details",font=("times new roman",12,"bold"))
        right_frame.place(x=780,y=10,width=660,height=580)


        img2_right=Image.open(r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (1).jpg")
        img2_right=img2_right.resize((750,130),Image.Resampling.LANCZOS)
        self.photoimg2_right=ImageTk.PhotoImage(img2_right)
        
        f_lbl=Label(right_frame,image=self.photoimg2_right)
        f_lbl.place(x=5,y=0,width=750,height=130)

# search syatem frame
        search_frame=LabelFrame(right_frame,bd=2,bg="white",relief=RIDGE,text="search system",font=("times new roman",12,"bold"))
        search_frame.place(x=5,y=135,width=730,height=70)

        search_label=Label(search_frame,text="search by",font=("times new roman",15,"bold"),bg="red",fg="white")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)


        search_combo=ttk.Combobox(search_frame,font=("times new roman",13,"bold"),state="read only",width=15)
        search_combo["values"]=("select ","roll no","csit","civil","mechnical")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)


        search_label=ttk.Entry(search_frame,width=15,font=("times new roman",13,"bold"))
        search_label.grid(row=3,column=3,padx=10,sticky=W)


        search_btn=Button(search_frame,text="search",width=12,font=("times new roman",13,"bold"),bg="blue",fg="white")
        search_btn.grid(row=0,column=2,padx=4)


        showall_btn=Button(search_frame,text="show all",width=12,font=("times new roman",13,"bold"),bg="blue",fg="white")
        showall_btn.grid(row=0,column=3,padx=4)

# tabel frame
        tabel_frame=LabelFrame(right_frame,bd=2,bg="white",relief=RIDGE)
        tabel_frame.place(x=5,y=210,width=730,height=350)

        scroll_x=ttk.Scrollbar(tabel_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(tabel_frame,orient=VERTICAL)

        self.student_tabel=ttk.Treeview(tabel_frame,column=("dep","course","year","sem","id","name","div","roll","gender","dob","email","phone","address","teacher","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_tabel.xview)
        scroll_y.config(command=self.student_tabel.yview)


        self.student_tabel.heading("dep",text="department")
        self.student_tabel.heading("course",text="course")
        self.student_tabel.heading("year",text="year")
        self.student_tabel.heading("sem",text="semester")
        self.student_tabel.heading("id",text="dstudentID")
        self.student_tabel.heading("name",text="name")
        self.student_tabel.heading("div",text="division")
        self.student_tabel.heading("roll",text="roll no")
        self.student_tabel.heading("gender",text="gender")
        self.student_tabel.heading("dob",text="dob")
        self.student_tabel.heading("email",text="email")
        self.student_tabel.heading("phone",text="phone")
        self.student_tabel.heading("address",text="address")
        self.student_tabel.heading("teacher",text="teacher")
        self.student_tabel.heading("photo",text="photosamplestatus")
        self.student_tabel["show"]="headings"




        self.student_tabel.column("dep",width=100)
        self.student_tabel.column("course",width=100)
        self.student_tabel.column("year",width=100)
        self.student_tabel.column("sem",width=100)
        self.student_tabel.column("id",width=100)
        self.student_tabel.column("name",width=100)
        self.student_tabel.column("div",width=100)
        self.student_tabel.column("roll",width=100)
        self.student_tabel.column("gender",width=100)
        self.student_tabel.column("dob",width=100)
        self.student_tabel.column("email",width=100)
        self.student_tabel.column("phone",width=100)
        self.student_tabel.column("address",width=100)
        self.student_tabel.column("teacher",width=100)
        self.student_tabel.column("photo",width=100)
        


        self.student_tabel.pack(fill=BOTH,expand=1)
        self.student_tabel.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()


        # ================== ERROR MESSAGE LOGIC ==================
    # Fix 4: Function to validate fields
    def add_data(self):
        if (self.var_dep.get() == "Select Department" or 
            self.var_std_id.get() == "" or 
            self.var_std_name.get() == "" or 
            self.var_roll.get() == ""):
            messagebox.showerror("Error", "All Fields are required!", parent=self.root)
        else:
            messagebox.showinfo("Success", "Student details have been added!", parent=self.root)

            try:
               conn=mysql.connector.connect(host="localhost",user="root",password="MYsql@6264",database="face_recognizer")
               my_cursor=conn.cursor()
               my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
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
                 ))
               
               conn.commit()
               self.fetch_data()
               conn.close()
               messagebox.showinfo("success","student details has been added successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("error",f"due to :{str(es)}",parent=self.root)

        
# searching 
        #========fetch data ========
    def fetch_data(self):
             conn=mysql.connector.connect(host="localhost",user="root",password="MYsql@6264",database="face_recognizer")
             my_cursor=conn.cursor()
             my_cursor.execute("select * from student")
             data=my_cursor.fetchall()

             if len(data)!=0:
                 self.student_tabel.delete(*self.student_tabel.get_children())
                 for i in data:
                     self.student_tabel.insert("",END,values=i)
                 conn.commit() 
             conn.close()  

    #========= get cursor=====
    def get_cursor(self,event=""):
        cursor_focus=self.student_tabel.focus()
        content=self.student_tabel.item(cursor_focus)
        data=content["values"] 


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


    # === update function 
    def update_data(self):
        if (self.var_dep.get() == "Select Department" or 
            self.var_std_id.get() == "" or 
            self.var_std_name.get() == "" or 
            self.var_roll.get() == ""):
            messagebox.showerror("Error", "All Fields are required!", parent=self.root)
        else:  
            try:
                update=messagebox.askyesno("update","do you want  to update",parent=self.root)
                if update>0:
                    conn=mysql.connector.connect(host="localhost",user="root",password="MYsql@6264",database="face_recognizer")
                    my_cursor=conn.cursor()
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
    DOB=%s,
    email=%s,
    phone=%s,
    address=%s,
    teacher=%s,
    photsample=%s
WHERE student_id=%s
""",
                    (
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
                        )
                        )
                else:
                    if  not update:
                        return 
                messagebox.showinfo("success"," student details sucessfully update completed",parent=self.root ) 
                conn.commit()
                self.fetch_data()
                conn.close()   
            except Exception as es:
                messagebox.showerror("error",f"due to:{str(es)}",parent=self.root)


                # ==== delete function
    # ================= DELETE FUNCTION =================
    def delete_data(self):

    # Check student id empty or not
      if self.var_std_id.get() == "":
        messagebox.showerror(
            "Error",
            "Student ID must be required",
            parent=self.root
        )

      else:
        try:
            # Confirmation message
            delete = messagebox.askyesno(
                "Student Delete Page",
                "Do you want to delete this student?",
                parent=self.root
            )

            if delete > 0:

                # Database connection
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="MYsql@6264",
                    database="face_recognizer"
                )

                my_cursor = conn.cursor()

                # DELETE QUERY
                sql = "DELETE FROM student WHERE student_id=%s"

                value = (self.var_std_id.get(),)

                # Execute query
                my_cursor.execute(sql, value)

                # Save changes
                conn.commit()

                # Check row deleted or not
                if my_cursor.rowcount > 0:

                    messagebox.showinfo(
                        "Success",
                        "Student details deleted successfully",
                        parent=self.root
                    )

                else:
                    messagebox.showerror(
                        "Error",
                        "Student ID not found",
                        parent=self.root
                    )

                # Refresh table
                self.fetch_data()

                # Reset fields
                self.reset_data()

                # Close connection
                conn.close()

            else:
                return

        except Exception as es:
            messagebox.showerror(
                "Error",
                f"Due To : {str(es)}",
                parent=self.root
            )
                




    def reset_data(self):
      self.var_dep.set("Select Department")
      self.var_course.set("Select Course")
      self.var_year.set("Select Year")
      self.var_sem.set("Select Semester")

      self.var_std_id.set("")
      self.var_std_name.set("")
      self.var_div.set("")
      self.var_roll.set("")
      self.var_gender.set("Male")   # default gender
      self.var_dob.set("")
      self.var_email.set("")
      self.var_phone.set("")
      self.var_address.set("")
      self.var_teacher.set("")
      self.var_radio.set("")


# ====== generate data set or take photo

    def generate_dataset(self):
         if (self.var_dep.get() == "Select Department" or 
            self.var_std_id.get() == "" or 
            self.var_std_name.get() == "" or 
            self.var_roll.get() == ""):
            messagebox.showerror("Error", "All Fields are required!", parent=self.root)
         else:  
            try:
               
                conn=mysql.connector.connect(host="localhost",user="root",password="MYsql@6264",database="face_recognizer")
                my_cursor=conn.cursor()
                my_cursor.execute("select * from student")
                myresult=my_cursor.fetchall()
                id=0
                for x in myresult:
                    id+=1
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
    DOB=%s,
    email=%s,
    phone=%s,
    address=%s,
    teacher=%s,
    photsample=%s
WHERE student_id=%s
""",
                    (
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
                             self.var_std_id.get()==id+1
                        )
                        )
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()


 # ===== load pr
                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)

                    # scaling factor = 1.3
                    # minimum neighbor = 5

                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped
                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    ret,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1

                    face=cv2.resize(face_cropped(my_frame),(450,450))
                    face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)  
                    file_name_path="data/user."+str(id)+"."+str(img_id)+".jpg"  
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50,50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                    cv2.imshow("Cropped face",face)

                    if cv2.waitKey(1)==13 or int(img_id)==10:
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("result","complete")  

            except Exception as es:
             messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)    


if __name__ == "__main__":        
    root = Tk()
    obj = student(root)
    root.mainloop()
