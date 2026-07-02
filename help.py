# =============================================================
#  HELP DESK — Face Recognition Attendance System
#  Features:
#    • Issue submission form (naam, ID, category, priority, message)
#    • Issues auto-saved to helpdesk_issues.txt
#    • Admin view: all issues as cards (newest first)
#    • Refresh + Clear All for admin
#    • Contact info: Gmail + Phone
# =============================================================

from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os

SUPPORT_EMAIL = "vikrampatel0232@gmail.com"
SUPPORT_PHONE = "+91 98765 43210"
ISSUES_FILE   = "helpdesk_issues.txt"


class HelpDesk:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x700+200+50")
        self.root.title("Help Desk — Support Center")
        self.root.configure(bg="#0B1120")
        self.root.resizable(False, False)
        self._build_ui()
        self._load_existing_issues()

    # ──────────────────────── UI ────────────────────────

    def _build_ui(self):
        # Header
        header = Frame(self.root, bg="#0EA5E9", height=58)
        header.pack(fill=X)
        header.pack_propagate(False)
        Label(header, text="◉  HELP DESK  &  SUPPORT CENTER",
              font=("Georgia", 18, "bold"),
              bg="#0EA5E9", fg="white").pack(side=LEFT, padx=20, pady=12)
        Label(header, text="Aapki problem humse share karein",
              font=("times new roman", 12, "italic"),
              bg="#0EA5E9", fg="#E0F2FE").pack(side=RIGHT, padx=20)

        body = Frame(self.root, bg="#0B1120")
        body.pack(fill=BOTH, expand=True)

        # Left panel
        left = Frame(body, bg="#0F1E35", width=420)
        left.pack(side=LEFT, fill=Y)
        left.pack_propagate(False)
        self._build_form(left)

        Frame(body, bg="#1E3A5F", width=2).pack(side=LEFT, fill=Y)

        # Right panel
        right = Frame(body, bg="#0B1120")
        right.pack(side=LEFT, fill=BOTH, expand=True)
        self._build_log(right)

    def _build_form(self, parent):
        Label(parent, text="Submit Your Issue",
              font=("Georgia", 15, "bold"),
              bg="#0F1E35", fg="#38BDF8").pack(pady=(20, 4), padx=20, anchor=W)
        Frame(parent, bg="#38BDF8", height=2, width=370).pack(padx=20, anchor=W)

        f = Frame(parent, bg="#0F1E35")
        f.pack(fill=X, padx=20, pady=8)

        def field(label_text, var, is_entry=True):
            Label(f, text=label_text,
                  font=("times new roman", 11, "bold"),
                  bg="#0F1E35", fg="#94A3B8").pack(anchor=W, pady=(10, 2))
            if is_entry:
                e = Entry(f, textvariable=var,
                          font=("times new roman", 12),
                          bg="#162032", fg="white",
                          insertbackground="white", relief="flat",
                          highlightthickness=1,
                          highlightbackground="#1E3A5F",
                          highlightcolor="#38BDF8")
                e.pack(fill=X, ipady=7)

        self.name_var = StringVar()
        self.uid_var  = StringVar()
        field("Aapka Naam *", self.name_var)
        field("Student / User ID *", self.uid_var)

        # Category
        Label(f, text="Issue Category *",
              font=("times new roman", 11, "bold"),
              bg="#0F1E35", fg="#94A3B8").pack(anchor=W, pady=(10, 2))
        self.cat_var = StringVar()
        cat = ttk.Combobox(f, textvariable=self.cat_var,
                           font=("times new roman", 12), state="readonly")
        cat["values"] = (
            "Category chunein",
            "Face Recognition nahi ho raha",
            "Attendance mark nahi hua",
            "Photo sample issue",
            "Login problem",
            "Database error",
            "Camera nahi chal raha",
            "Kuch aur"
        )
        cat.current(0)
        cat.pack(fill=X, ipady=5)

        # Priority
        Label(f, text="Priority",
              font=("times new roman", 11, "bold"),
              bg="#0F1E35", fg="#94A3B8").pack(anchor=W, pady=(10, 2))
        self.priority_var = StringVar(value="Normal")
        prow = Frame(f, bg="#0F1E35")
        prow.pack(anchor=W)
        for val, col in [("Low","#22C55E"),("Normal","#38BDF8"),
                          ("High","#F97316"),("Urgent","#EF4444")]:
            Radiobutton(prow, text=val, variable=self.priority_var, value=val,
                        font=("times new roman", 11),
                        bg="#0F1E35", fg=col, activebackground="#0F1E35",
                        selectcolor="#162032", cursor="hand2").pack(side=LEFT, padx=5)

        # Message
        Label(f, text="Apni Problem Likhein *",
              font=("times new roman", 11, "bold"),
              bg="#0F1E35", fg="#94A3B8").pack(anchor=W, pady=(12, 2))
        self.msg_text = Text(f, height=5,
                             font=("times new roman", 12),
                             bg="#162032", fg="white",
                             insertbackground="white", relief="flat",
                             highlightthickness=1,
                             highlightbackground="#1E3A5F",
                             highlightcolor="#38BDF8", wrap=WORD)
        self.msg_text.pack(fill=X)

        # Status
        self.form_status = StringVar()
        Label(f, textvariable=self.form_status,
              font=("times new roman", 11),
              bg="#0F1E35", fg="#4ADE80", wraplength=370).pack(pady=(6,0), anchor=W)

        # Submit button
        sb = Button(f, text="  📨  ISSUE SUBMIT KAREIN",
                    command=self._submit,
                    font=("Georgia", 12, "bold"),
                    bg="#0EA5E9", fg="white",
                    activebackground="#0284C7",
                    relief="flat", cursor="hand2", bd=0)
        sb.pack(fill=X, ipady=11, pady=(12,0))
        sb.bind("<Enter>", lambda e: sb.config(bg="#0284C7"))
        sb.bind("<Leave>", lambda e: sb.config(bg="#0EA5E9"))

        # Contact box
        cbox = Frame(parent, bg="#0A1628",
                     highlightthickness=1, highlightbackground="#1E3A5F")
        cbox.pack(fill=X, padx=20, pady=(16, 0))
        Label(cbox, text="📞  Direct Contact",
              font=("Georgia", 12, "bold"),
              bg="#0A1628", fg="#38BDF8").pack(anchor=W, padx=14, pady=(10,4))
        Label(cbox, text=f"📧  {SUPPORT_EMAIL}",
              font=("Courier", 11), bg="#0A1628", fg="#94A3B8").pack(anchor=W, padx=14, pady=2)
        Label(cbox, text=f"📱  {SUPPORT_PHONE}",
              font=("Courier", 11), bg="#0A1628", fg="#94A3B8").pack(anchor=W, padx=14, pady=(2,10))

    def _build_log(self, parent):
        top = Frame(parent, bg="#0B1120")
        top.pack(fill=X, padx=16, pady=(14,6))
        Label(top, text="Submitted Issues  (Admin View)",
              font=("Georgia", 14, "bold"),
              bg="#0B1120", fg="#38BDF8").pack(side=LEFT)

        clr = Button(top, text="🗑 Clear All", command=self._clear_all,
                     font=("times new roman", 10, "bold"),
                     bg="#450A0A", fg="#FCA5A5",
                     activebackground="#7F1D1D",
                     relief="flat", cursor="hand2", bd=0)
        clr.pack(side=RIGHT, ipadx=8, ipady=4)

        ref = Button(top, text="⟳ Refresh", command=self._load_existing_issues,
                     font=("times new roman", 10, "bold"),
                     bg="#1E3A5F", fg="#38BDF8",
                     activebackground="#162032",
                     relief="flat", cursor="hand2", bd=0)
        ref.pack(side=RIGHT, ipadx=8, ipady=4, padx=(0,8))

        Frame(parent, bg="#1E3A5F", height=1).pack(fill=X, padx=16)

        self.count_var = StringVar(value="Issues: 0")
        Label(parent, textvariable=self.count_var,
              font=("Courier", 10), bg="#0B1120", fg="#4A6FA5").pack(anchor=E, padx=20, pady=2)

        lf = Frame(parent, bg="#0B1120")
        lf.pack(fill=BOTH, expand=True, padx=12, pady=(0,12))

        self.log_canvas = Canvas(lf, bg="#0B1120", highlightthickness=0)
        sb2 = ttk.Scrollbar(lf, orient=VERTICAL, command=self.log_canvas.yview)
        self.log_canvas.configure(yscrollcommand=sb2.set)
        sb2.pack(side=RIGHT, fill=Y)
        self.log_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.log_inner = Frame(self.log_canvas, bg="#0B1120")
        self.log_win = self.log_canvas.create_window((0,0), window=self.log_inner, anchor="nw")

        self.log_inner.bind("<Configure>",
            lambda e: self.log_canvas.configure(scrollregion=self.log_canvas.bbox("all")))
        self.log_canvas.bind("<Configure>",
            lambda e: self.log_canvas.itemconfig(self.log_win, width=e.width))
        self.log_canvas.bind_all("<MouseWheel>",
            lambda e: self.log_canvas.yview_scroll(-1*(e.delta//120), "units"))

    # ──────────────────────── LOGIC ────────────────────────

    def _submit(self):
        name     = self.name_var.get().strip()
        uid      = self.uid_var.get().strip()
        category = self.cat_var.get()
        priority = self.priority_var.get()
        message  = self.msg_text.get("1.0", END).strip()

        if not name:
            self.form_status.set("⚠ Naam zaroori hai!")
            return
        if not uid:
            self.form_status.set("⚠ Student/User ID zaroori hai!")
            return
        if category == "Category chunein":
            self.form_status.set("⚠ Category select karein!")
            return
        if not message:
            self.form_status.set("⚠ Problem likhna zaroori hai!")
            return

        self.form_status.set("")
        now       = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        ticket_no = f"TKT-{datetime.now().strftime('%d%m%y%H%M%S')}"

        issue_text = (
            f"\n{'='*60}\n"
            f"Ticket   : {ticket_no}\n"
            f"Date     : {now}\n"
            f"Name     : {name}\n"
            f"User ID  : {uid}\n"
            f"Category : {category}\n"
            f"Priority : {priority}\n"
            f"Status   : Open\n"
            f"Message  :\n{message}\n"
            f"{'='*60}\n"
        )

        try:
            with open(ISSUES_FILE, "a", encoding="utf-8") as f:
                f.write(issue_text)
        except Exception as e:
            messagebox.showerror("Error", f"File save nahi hua:\n{str(e)}", parent=self.root)
            return

        # Clear form
        self.name_var.set("")
        self.uid_var.set("")
        self.cat_var.set("Category chunein")
        self.priority_var.set("Normal")
        self.msg_text.delete("1.0", END)

        self._load_existing_issues()
        self.form_status.set(f"✓ Submitted!  Ticket: {ticket_no}")

        messagebox.showinfo(
            "Issue Submitted ✅",
            f"Aapka issue successfully submit ho gaya!\n\n"
            f"Ticket No : {ticket_no}\n"
            f"Category  : {category}\n"
            f"Priority  : {priority}\n\n"
            f"Admin jald hi aapki madad karega.\n"
            f"Contact: {SUPPORT_EMAIL}",
            parent=self.root
        )

    def _load_existing_issues(self):
        for w in self.log_inner.winfo_children():
            w.destroy()

        if not os.path.exists(ISSUES_FILE):
            Label(self.log_inner,
                  text="Abhi koi issue submit nahi hua.",
                  font=("times new roman", 13, "italic"),
                  bg="#0B1120", fg="#334155").pack(pady=40)
            self.count_var.set("Issues: 0")
            return

        try:
            with open(ISSUES_FILE, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return

        blocks = [b.strip() for b in content.split("="*60) if b.strip()]
        count  = 0
        for block in reversed(blocks):
            lines = block.strip().splitlines()
            data, msg_lines, in_msg = {}, [], False
            for line in lines:
                if line.startswith("Message  :"):
                    in_msg = True
                    continue
                if in_msg:
                    msg_lines.append(line)
                elif ":" in line:
                    k, _, v = line.partition(":")
                    data[k.strip()] = v.strip()
            if data:
                count += 1
                self._add_card(data, "\n".join(msg_lines).strip())

        self.count_var.set(f"Issues: {count}")
        self.log_canvas.yview_moveto(0)

    def _add_card(self, data, message):
        p_colors = {"Low":"#22C55E","Normal":"#38BDF8","High":"#F97316","Urgent":"#EF4444"}
        priority = data.get("Priority","Normal")
        p_col    = p_colors.get(priority,"#38BDF8")

        card = Frame(self.log_inner, bg="#0F1E35",
                     highlightthickness=1, highlightbackground="#1E3A5F")
        card.pack(fill=X, padx=8, pady=5, ipadx=8, ipady=6)

        top = Frame(card, bg="#0F1E35")
        top.pack(fill=X, padx=10, pady=(6,2))
        Label(top, text=f"🎫  {data.get('Ticket','N/A')}",
              font=("Courier", 10, "bold"),
              bg="#0F1E35", fg="#64748B").pack(side=LEFT)
        Label(top, text=f"  {priority}  ",
              font=("times new roman", 10, "bold"),
              bg=p_col, fg="white").pack(side=RIGHT)
        Label(top, text=data.get("Date",""),
              font=("Courier", 9),
              bg="#0F1E35", fg="#334155").pack(side=RIGHT, padx=8)

        ir = Frame(card, bg="#0F1E35")
        ir.pack(fill=X, padx=10, pady=2)
        Label(ir, text=f"👤  {data.get('Name','')}",
              font=("times new roman", 12, "bold"),
              bg="#0F1E35", fg="white").pack(side=LEFT)
        Label(ir, text=f"  |  ID: {data.get('User ID','')}",
              font=("times new roman", 11),
              bg="#0F1E35", fg="#64748B").pack(side=LEFT)

        Label(card, text=f"📌  {data.get('Category','')}",
              font=("times new roman", 11),
              bg="#0F1E35", fg="#38BDF8").pack(anchor=W, padx=10, pady=1)

        if message:
            mf = Frame(card, bg="#162032",
                       highlightthickness=1, highlightbackground="#1E3A5F")
            mf.pack(fill=X, padx=10, pady=(4,4))
            Label(mf, text=message,
                  font=("times new roman", 11),
                  bg="#162032", fg="#CBD5E1",
                  wraplength=520, justify=LEFT, anchor=W).pack(padx=10, pady=6, anchor=W)

        Label(card, text=f"  {data.get('Status','Open')}  ",
              font=("times new roman", 10),
              bg="#064E3B", fg="#4ADE80").pack(anchor=W, padx=10, pady=(2,4))

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Saare issues delete ho jaayenge?", parent=self.root):
            try:
                if os.path.exists(ISSUES_FILE):
                    os.remove(ISSUES_FILE)
                self._load_existing_issues()
                messagebox.showinfo("Done", "Saare issues clear ho gaye!", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)


if __name__ == "__main__":
    root = Tk()
    HelpDesk(root)
    root.mainloop()