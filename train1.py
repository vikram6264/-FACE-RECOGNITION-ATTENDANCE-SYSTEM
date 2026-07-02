from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

# ✅ FIX: Training mein face ko isi size pe resize karo
#         jo recognition ke time use hoti hai
FACE_SIZE = (100, 100)   # training aur recognition dono same size use karenge


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

        # ================= CENTER PANEL =================
        center_frame = Frame(
            self.root,
            bg="#1e293b",
            bd=3,
            relief=RIDGE
        )
        center_frame.place(x=250, y=200, width=1030, height=160)

        heading = Label(
            center_frame,
            text="CLICK BELOW TO START TRAINING MODEL",
            font=("times new roman", 22, "bold"),
            bg="#1e293b",
            fg="white"
        )
        heading.place(x=180, y=15)

        desc = Label(
            center_frame,
            text="This process will detect faces, resize them to 100x100, and create classifier.xml",
            font=("times new roman", 13),
            bg="#1e293b",
            fg="#cbd5e1"
        )
        desc.place(x=100, y=65)

        # ================= STATUS LABEL =================
        self.status_var = StringVar(value="")
        status_lbl = Label(
            self.root,
            textvariable=self.status_var,
            font=("times new roman", 14, "bold"),
            bg="#0f172a",
            fg="#22c55e",
            wraplength=1000
        )
        status_lbl.place(x=250, y=380, width=1030, height=60)

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
        b1.place(x=360, y=105, width=300, height=45)

    # ================= TRAIN FUNCTION (FIXED) =================
    def train_classifier(self):

        data_dir = "data"

        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"'{data_dir}' folder not found!", parent=self.root)
            return

        # ✅ FIX: Load Haar cascade to detect face INSIDE image before training
        cascade_path = "haarcascade_frontalface_default.xml"
        if not os.path.exists(cascade_path):
            messagebox.showerror("Error", f"'{cascade_path}' not found!\nPlace it in the same folder.", parent=self.root)
            return

        face_cascade = cv2.CascadeClassifier(cascade_path)

        all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir)
                     if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        faces = []
        ids   = []
        skipped = 0

        for image_path in all_files:
            try:
                # ✅ FIX: Extract ID from filename (User.ID.count.jpg format)
                fname = os.path.basename(image_path)
                parts = fname.split('.')
                if len(parts) < 3:
                    skipped += 1
                    continue
                student_id = int(parts[1])
            except (ValueError, IndexError):
                skipped += 1
                continue

            # ✅ FIX: Read as grayscale
            img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img_gray is None:
                skipped += 1
                continue

            # ✅ FIX: Detect face in the saved image (crop, not full image)
            detected = face_cascade.detectMultiScale(
                img_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            if len(detected) > 0:
                # Use the largest detected face
                largest_idx = int(np.argmax([w * h for (x, y, w, h) in detected]))
                x, y, w, h  = detected[largest_idx]
                face_roi = img_gray[y:y+h, x:x+w]
            else:
                # ✅ FIX: If no face detected in image, use full image
                #         (sample.py already saves cropped faces, so this is fallback)
                face_roi = img_gray

            # ✅ FIX: Resize to fixed size — SAME size used in recognition
            face_resized = cv2.resize(face_roi, FACE_SIZE)

            faces.append(face_resized)
            ids.append(student_id)

            # Show preview
            cv2.imshow("Training - Press any key to continue", face_resized)
            cv2.waitKey(1)

        cv2.destroyAllWindows()

        if len(faces) == 0:
            messagebox.showerror(
                "Error",
                f"No valid face images found in '{data_dir}' folder!\n"
                "Please recapture photos from Student Details → Take Photo.",
                parent=self.root
            )
            return

        ids_np = np.array(ids)

        unique_labels = set(ids)
        print(f"[TRAIN] Total images  : {len(faces)}")
        print(f"[TRAIN] Unique students: {len(unique_labels)}  → IDs: {sorted(unique_labels)}")
        print(f"[TRAIN] Skipped files : {skipped}")

        # ✅ FIX: Create LBPH recognizer with tuned parameters
        clf = cv2.face.LBPHFaceRecognizer_create(
            radius=2,        # default=1 — bigger radius = more detail
            neighbors=8,
            grid_x=8,
            grid_y=8
        )

        clf.train(faces, ids_np)
        clf.write("classifier.xml")

        self.status_var.set(
            f"✅ Training Done! {len(faces)} images trained for {len(unique_labels)} student(s). "
            f"{skipped} files skipped."
        )

        messagebox.showinfo(
            "Result",
            f"Training completed!\n\n"
            f"✔ Images trained : {len(faces)}\n"
            f"✔ Students       : {len(unique_labels)}\n"
            f"✔ classifier.xml created\n\n"
            f"Face size used: {FACE_SIZE[0]}x{FACE_SIZE[1]} px",
            parent=self.root
        )


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()