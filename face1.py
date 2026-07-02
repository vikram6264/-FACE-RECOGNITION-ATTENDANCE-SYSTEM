from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import time
import cv2
import os
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
CONFIDENCE_MIN   = 80      # ✅ FIX: LBPH distance threshold — lower = stricter match
                            #         50 is good starting point (not %, it's raw distance)
CONFIRM_SECONDS  = 1.5     # seconds the same face must stay still before marking
VOTE_WINDOW      = 20      # last N frames used for majority vote
VOTE_RATIO       = 0.60    # 60% agree → instant mark
NO_MATCH_TIMEOUT = 10      # seconds of unknown face before warning

# ✅ FIX: Face resize size — MUST match train.py FACE_SIZE
FACE_SIZE = (100, 100)

CSV_FILE     = "vikram.csv"
DATE_FORMAT  = "%d-%m-%Y"
TIME_FORMAT  = "%H:%M:%S"

# DB config
DB_CONFIG = dict(host="localhost", user="root",
                 password="MYsql@6264", database="face_recognizer")
# ─────────────────────────────────────────────────────────────────────────────


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="#edf2f7")

        # ── Title ─────────────────────────────────────────────────────────
        Label(self.root,
              text="FACE RECOGNITION",
              font=("times new roman", 34, "bold"),
              bg="#0f172a", fg="white"
              ).place(x=0, y=0, width=1530, height=55)

        # ── Left frame ────────────────────────────────────────────────────
        BASE = os.path.dirname(os.path.abspath(__file__))
        left_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        left_frame.place(x=20, y=80, width=730, height=650)

        left_img_path = os.path.join(BASE, "images", "face_left.jpg")
        if os.path.exists(left_img_path):
            img_left = Image.open(left_img_path).resize((720, 620), Image.Resampling.LANCZOS)
            self.photoimg_left = ImageTk.PhotoImage(img_left)
            Label(left_frame, image=self.photoimg_left).place(x=0, y=0, width=720, height=640)
        else:
            Label(left_frame, text="Face Recognition", font=("times new roman", 28, "bold"),
                  bg="#1e3a5f", fg="white").place(x=0, y=0, width=720, height=640)

        # ── Right frame ───────────────────────────────────────────────────
        right_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        right_frame.place(x=780, y=80, width=720, height=650)

        right_img_path = os.path.join(BASE, "images", "face_right.jpg")
        if os.path.exists(right_img_path):
            img_right = Image.open(right_img_path).resize((700, 340), Image.Resampling.LANCZOS)
            self.photoimg_right = ImageTk.PhotoImage(img_right)
            Label(right_frame, image=self.photoimg_right).place(x=10, y=10, width=690, height=340)
        else:
            Label(right_frame, bg="#1e3a5f").place(x=10, y=10, width=690, height=340)

        Label(right_frame,
              text="Smart Face Attendance System",
              font=("times new roman", 26, "bold"),
              bg="white", fg="#0f172a"
              ).place(x=60, y=375)

        # ── Status label ─────────────────────────────────────────────────
        self.status_var = StringVar(value="System ready. Click button to start.")
        Label(right_frame,
              textvariable=self.status_var,
              font=("times new roman", 13),
              bg="white", fg="#475569",
              wraplength=680, justify=CENTER
              ).place(x=20, y=430, width=680, height=100)

        Button(right_frame,
               text="▶  START FACE RECOGNITION",
               cursor="hand2",
               command=self.face_recog,
               font=("times new roman", 22, "bold"),
               bg="#dc2626", fg="white",
               activebackground="#b91c1c",
               relief=RIDGE, bd=4
               ).place(x=140, y=560, width=430, height=60)

    # ─────────────────────────────────────────────────────────────────────
    # DB helpers
    # ─────────────────────────────────────────────────────────────────────
    def open_db(self):
        return mysql.connector.connect(**DB_CONFIG)

    def fetch_student(self, conn, student_id):
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT Student_id, roll, name, depatment "
                "FROM student WHERE Student_id=%s",
                (student_id,)
            )
            row = cur.fetchone()
            cur.close()
            if row:
                return {"id": row[0], "roll": row[1], "name": row[2], "dept": row[3]}
            return None
        except Exception as e:
            print(f"[DB ERROR] fetch_student: {e}")
            return None

    # ─────────────────────────────────────────────────────────────────────
    # mark_attendance
    # ─────────────────────────────────────────────────────────────────────
    def mark_attendance(self, sid, roll, name, dept):
        now   = datetime.now()
        today = now.strftime(DATE_FORMAT)
        t     = now.strftime(TIME_FORMAT)

        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="") as f:
                f.write("ID,Roll,Name,Department,Time,Date,Status\n")

        existing_rows = []
        with open(CSV_FILE, "r", newline="") as f:
            lines = f.readlines()

        header = lines[0].strip() if lines else "ID,Roll,Name,Department,Time,Date,Status"
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split(",")
            if len(parts) < 7:
                continue
            if parts[0].strip() in ("", "Unknown"):
                continue
            existing_rows.append(parts)

        # Duplicate check
        for row in existing_rows:
            row_id   = row[0].strip()
            row_date = row[5].strip()
            if row_id == str(sid) and row_date == today:
                print(f"[CSV] Already marked: ID={sid} on {today}")
                return "already"

        new_row = f"{sid},{roll},{name},{dept},{t},{today},Present"
        with open(CSV_FILE, "w", newline="") as f:
            f.write(header + "\n")
            for row in existing_rows:
                f.write(",".join(row) + "\n")
            f.write(new_row + "\n")

        print(f"[CSV] Marked: {new_row}")
        return "marked"

    # ─────────────────────────────────────────────────────────────────────
    # Debug: check data folder labels
    # ─────────────────────────────────────────────────────────────────────
    def verify_data_labels(self):
        data_dir = "data"
        print("\n" + "=" * 55)
        print("  DATA LABEL CHECK")
        print("=" * 55)
        if not os.path.exists(data_dir):
            print("  ERROR: 'data/' folder not found.")
            return
        counts = {}
        for fname in os.listdir(data_dir):
            parts = fname.split(".")
            if len(parts) >= 3:
                try:
                    label = int(parts[1])
                    counts[label] = counts.get(label, 0) + 1
                except ValueError:
                    pass
        if not counts:
            print("  !! No valid images found in data/ !!")
            return
        for label in sorted(counts):
            print(f"  Student_id={label:>4}  →  {counts[label]:>3} images")
        if len(counts) == 1:
            only = list(counts.keys())[0]
            print(f"\n  !! WARNING: Only 1 label ({only}) found !!")
        else:
            print(f"\n  OK: {len(counts)} students in data/")
        print("=" * 55 + "\n")

    # ─────────────────────────────────────────────────────────────────────
    # Helper: draw shadowed text
    # ─────────────────────────────────────────────────────────────────────
    @staticmethod
    def put_text(img, text, x, y, scale=0.75, color=(255, 255, 255), thickness=2):
        cv2.putText(img, text, (x + 1, y + 1),
                    cv2.FONT_HERSHEY_COMPLEX, scale, (0, 0, 0), thickness + 1)
        cv2.putText(img, text, (x, y),
                    cv2.FONT_HERSHEY_COMPLEX, scale, color, thickness)

    # ─────────────────────────────────────────────────────────────────────
    # MAIN RECOGNITION LOOP
    # ─────────────────────────────────────────────────────────────────────
    def face_recog(self):
        self.verify_data_labels()

        for fname in ("classifier.xml", "haarcascade_frontalface_default.xml"):
            if not os.path.exists(fname):
                messagebox.showerror("Missing File",
                                     f"'{fname}' not found!\n"
                                     "Ensure it is in the same folder as this script.",
                                     parent=self.root)
                return

        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        # ✅ FIX: Print LBPH threshold info for debugging
        print(f"[CONFIG] CONFIDENCE_MIN (max raw_dist allowed) = {CONFIDENCE_MIN}")
        print(f"[CONFIG] FACE_SIZE for recognition = {FACE_SIZE}")

        try:
            db_conn = self.open_db()
        except Exception as e:
            messagebox.showerror("DB Error",
                                 f"Cannot connect to database:\n{e}",
                                 parent=self.root)
            return

        video_cap = cv2.VideoCapture(0)
        if not video_cap.isOpened():
            messagebox.showerror("Camera Error",
                                 "Camera could not be opened!\n"
                                 "Check if another app is using it.",
                                 parent=self.root)
            db_conn.close()
            return

        db_cache        = {}
        vote_history    = []
        confirm_tracker = {}
        attendance_done = False
        no_match_start  = None

        self.status_var.set("Camera running... Look at the camera.")

        def process_frame(img):
            nonlocal attendance_done, no_match_start, \
                     vote_history, confirm_tracker

            gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=4,
                minSize=(40, 40),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(faces) == 0:
                no_match_start  = None
                vote_history    = []
                confirm_tracker = {}
                self.put_text(img,
                              "No face detected — move closer",
                              20, 40, scale=0.75, color=(180, 180, 180))
                return False

            # Pick largest face
            largest_idx    = int(np.argmax([w * h for (x, y, w, h) in faces]))
            lx, ly, lw, lh = faces[largest_idx]

            for idx, (x, y, w, h) in enumerate(faces):
                if idx == largest_idx:
                    continue
                cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 100), 1)
                self.put_text(img, "Not selected", x, y - 8,
                              scale=0.5, color=(150, 150, 150), thickness=1)

            # ✅ FIX 1: Extract face ROI
            face_roi = gray[ly:ly + lh, lx:lx + lw]

            # ✅ FIX 2: Resize to SAME size used in training (100x100)
            face_resized = cv2.resize(face_roi, FACE_SIZE)

            # ✅ FIX 3: Apply histogram equalization for better lighting robustness
            face_resized = cv2.equalizeHist(face_resized)

            # ✅ FIX 4: Predict on resized face
            id_pred, raw_dist = clf.predict(face_resized)

            # ✅ FIX 5: CORRECT confidence display
            #    raw_dist is LBPH distance — LOWER = better match
            #    raw_dist < 50  → very confident
            #    raw_dist < 80  → confident
            #    raw_dist > 100 → uncertain
            #    We show it as a % where 0 raw = 100% confident
            confidence_display = max(0, int(100 - raw_dist))  # for display only

            print(f"[PREDICT] id={id_pred}  raw_dist={raw_dist:.1f}  display={confidence_display}%")

            # ✅ FIX 6: Threshold check using raw_dist (NOT %)
            #    raw_dist > CONFIDENCE_MIN → Unknown (i.e., too far from trained face)
            if raw_dist > CONFIDENCE_MIN:
                vote_history    = []
                confirm_tracker = {}

                cv2.rectangle(img, (lx, ly), (lx + lw, ly + lh), (0, 0, 220), 3)
                self.put_text(img, "Unknown Face",
                              lx, max(ly - 35, 20),
                              scale=0.85, color=(60, 60, 255))
                self.put_text(img,
                              f"Dist: {raw_dist:.0f}  (need <{CONFIDENCE_MIN})",
                              lx, ly + lh + 28,
                              scale=0.6, color=(60, 60, 255))

                if no_match_start is None:
                    no_match_start = time.time()
                else:
                    elapsed   = time.time() - no_match_start
                    remaining = max(0.0, NO_MATCH_TIMEOUT - elapsed)
                    self.put_text(img,
                                  f"No match ({remaining:.0f}s remaining)",
                                  20, 40, scale=0.8, color=(0, 0, 255))
                    if elapsed >= NO_MATCH_TIMEOUT:
                        return "timeout"

                return False

            # ── Confident match ───────────────────────────────────────────
            no_match_start = None

            if id_pred not in db_cache:
                info = self.fetch_student(db_conn, id_pred)
                if info is None:
                    cv2.rectangle(img, (lx, ly), (lx + lw, ly + lh), (0, 165, 255), 3)
                    self.put_text(img,
                                  f"ID {id_pred} not in DB — please retrain",
                                  lx, max(ly - 10, 20),
                                  scale=0.65, color=(0, 165, 255))
                    print(f"[WARN] id={id_pred} not in student table!")
                    return False
                db_cache[id_pred] = info

            # Sliding majority vote
            vote_history.append(id_pred)
            if len(vote_history) > VOTE_WINDOW:
                vote_history.pop(0)

            vote_counts = {}
            for v in vote_history:
                vote_counts[v] = vote_counts.get(v, 0) + 1

            winner_id    = max(vote_counts, key=vote_counts.get)
            winner_info  = db_cache.get(winner_id, db_cache[id_pred])
            winner_votes = vote_counts[winner_id]
            vote_ratio   = winner_votes / len(vote_history)

            # Draw green box + info
            cv2.rectangle(img, (lx, ly), (lx + lw, ly + lh), (0, 220, 0), 3)

            info_lines = [
                (f"ID   : {winner_info['id']}",   ly - 85),
                (f"Roll : {winner_info['roll']}",  ly - 60),
                (f"Name : {winner_info['name']}",  ly - 35),
                (f"Dept : {winner_info['dept']}",  ly - 10),
            ]
            for txt, ty in info_lines:
                self.put_text(img, txt, lx, max(ty, 15))

            # Confirm timer
            now_t = time.time()
            if winner_id not in confirm_tracker:
                confirm_tracker = {winner_id: now_t}
            first_seen        = confirm_tracker[winner_id]
            elapsed_confirm   = now_t - first_seen
            remaining_confirm = max(0.0, CONFIRM_SECONDS - elapsed_confirm)

            # Progress bar
            bar_y    = ly + lh + 10
            bar_w    = lw
            filled_w = int(bar_w * min(elapsed_confirm / CONFIRM_SECONDS, 1.0))
            cv2.rectangle(img, (lx, bar_y), (lx + bar_w, bar_y + 14), (50, 50, 50), -1)
            cv2.rectangle(img, (lx, bar_y), (lx + filled_w, bar_y + 14), (0, 220, 0), -1)
            self.put_text(img,
                          f"Dist: {raw_dist:.0f}   Hold still: {remaining_confirm:.1f}s",
                          lx, bar_y + 32, scale=0.6, color=(0, 230, 255))

            # ── Mark after vote + confirm ─────────────────────────────────
            if vote_ratio >= VOTE_RATIO and elapsed_confirm >= CONFIRM_SECONDS and not attendance_done:
                attendance_done = True

                self.put_text(img, "CONFIRMED!",
                              lx, ly + lh // 2, scale=1.1, color=(0, 255, 0))
                cv2.imshow("Face Recognition  |  ESC = exit", img)
                cv2.waitKey(500)
                return "done"

            return False

        # ── Main capture loop ─────────────────────────────────────────────
        final_result = None
        final_info   = None

        while True:
            ret, frame = video_cap.read()
            if not ret:
                print("[ERROR] Camera frame read failed")
                break

            result = process_frame(frame)

            if result == "done":
                if vote_history:
                    vote_counts = {}
                    for v in vote_history:
                        vote_counts[v] = vote_counts.get(v, 0) + 1
                    winner_id  = max(vote_counts, key=vote_counts.get)
                    final_info = db_cache.get(winner_id)
                final_result = "done"
                break

            elif result == "timeout":
                final_result = "timeout"
                break

            cv2.imshow("Face Recognition  |  ESC = exit", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q"), ord("Q")):
                final_result = "cancelled"
                break

        if video_cap.isOpened():
            video_cap.release()
        cv2.destroyAllWindows()

        # ── Post-loop actions ─────────────────────────────────────────────
        if final_result == "done" and final_info:
            status = self.mark_attendance(
                final_info["id"],
                final_info["roll"],
                final_info["name"],
                final_info["dept"]
            )

            if status == "already":
                msg = (f"Attendance already marked today!\n\n"
                       f"Name : {final_info['name']}\n"
                       f"Roll : {final_info['roll']}\n"
                       f"Dept : {final_info['dept']}\n\n"
                       f"Date : {datetime.now().strftime(DATE_FORMAT)}")
                self.status_var.set(f"Already marked today — {final_info['name']}")
                messagebox.showwarning("Already Marked", msg, parent=self.root)
            else:
                msg = (f"Attendance Marked Successfully!\n\n"
                       f"Name : {final_info['name']}\n"
                       f"Roll : {final_info['roll']}\n"
                       f"Dept : {final_info['dept']}\n"
                       f"Time : {datetime.now().strftime(TIME_FORMAT)}\n"
                       f"Date : {datetime.now().strftime(DATE_FORMAT)}")
                self.status_var.set(
                    f"Marked — {final_info['name']} | "
                    f"{datetime.now().strftime(TIME_FORMAT)}"
                )
                messagebox.showinfo("Attendance Marked", msg, parent=self.root)

        elif final_result == "timeout":
            self.status_var.set("No match found after timeout.")
            messagebox.showwarning(
                "Not Found",
                "No registered student matched the camera.\n\n"
                "Tips:\n"
                "• Improve lighting\n"
                "• Move closer to camera\n"
                "• Retrain photos (run Train Data again)\n"
                f"• Current threshold: CONFIDENCE_MIN={CONFIDENCE_MIN}\n"
                f"  (raise to 80-100 if real person not detected)",
                parent=self.root
            )

        elif final_result == "cancelled":
            self.status_var.set("Recognition cancelled.")

        try:
            db_conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    root = Tk()
    obj  = Face_Recognition(root)
    root.mainloop()