from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="#0f172a")

        # ================= TITLE =================
        title_lbl = Label(
            self.root,
            text="TRAIN FACE DATASET",
            font=("times new roman", 34, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        )
        title_lbl.place(x=0, y=0, width=1530, height=60)

        # ================= TOP IMAGE =================
        img_top = Image.open(
            r"C:\Users\vikra\OneDrive\Desktop\face re\image\OIP (12).jpg"
        )
        img_top = img_top.resize((1450, 280), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        top_frame = Frame(self.root, bd=0, bg="#0f172a")
        top_frame.place(x=40, y=75, width=1450, height=290)

        f_lbl = Label(
            top_frame,
            image=self.photoimg_top,
            bd=0,
            relief=RIDGE
        )
        f_lbl.place(x=0, y=0, width=1450, height=290)

        # ================= CENTER PANEL =================
        center_frame = Frame(
            self.root,
            bg="#1e293b",
            bd=3,
            relief=RIDGE
        )
        center_frame.place(x=250, y=390, width=1030, height=120)

        heading = Label(
            center_frame,
            text="CLICK BELOW TO START TRAINING MODEL",
            font=("times new roman", 22, "bold"),
            bg="#1e293b",
            fg="white"
        )
        heading.place(x=180, y=10)

        desc = Label(
            center_frame,
            text="This process will train all detected face images and create classifier.xml",
            font=("times new roman", 14),
            bg="#1e293b",
            fg="#cbd5e1"
        )
        desc.place(x=150, y=50)

        # ================= BUTTON =================
        b1 = Button(
            center_frame,
            text="TRAIN DATA",
            cursor="hand2",
            command=self.train_classifier,
            font=("times new roman", 20, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            bd=0
        )
        b1.place(x=360, y=80, width=300, height=45)

        # ================= BOTTOM IMAGE =================
        img_bottom = Image.open(
            r"C:\Users\vikra\OneDrive\Desktop\data for project(minor)\OIP (3).jpg"
        )
        img_bottom = img_bottom.resize((1450, 220), Image.Resampling.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        bottom_frame = Frame(self.root, bd=0, bg="#0f172a")
        bottom_frame.place(x=40, y=540, width=1450, height=220)

        f_lbl = Label(
            bottom_frame,
            image=self.photoimg_bottom,
            bd=0,
            relief=RIDGE
        )
        f_lbl.place(x=0, y=0, width=1450, height=220)

    # ================= TRAIN FUNCTION =================
    def train_classifier(self):

        data_dir = "data"

        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:

            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')

            try:
                id = int(os.path.split(image)[1].split('.')[1])

            except:
                continue

            faces.append(imageNp)
            ids.append(id)

            cv2.imshow("Training", imageNp)
            cv2.waitKey(1)

        ids = np.array(ids)

        print("Total Faces:", len(faces))

        if len(faces) == 0:
            messagebox.showerror(
                "Error",
                "No images found in data folder!"
            )
            return

        clf = cv2.face.LBPHFaceRecognizer_create()

        clf.train(faces, ids)

        clf.write("classifier.xml")

        cv2.destroyAllWindows()

        messagebox.showinfo(
            "Result",
            "Training completed & classifier.xml created!"
        )


if __name__ == "__main__":

    root = Tk()

    obj = Train(root)

    root.mainloop()
