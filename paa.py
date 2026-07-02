from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector
import csv
import os
import datetime
from collections import defaultdict

# ─── Matplotlib for charts ───────────────────────────────────────────────────
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# ─── DB Config (same as your project) ────────────────────────────────────────
DB_CONFIG = dict(host="localhost", user="root", password="MYsql@6264", database="face_recognizer")
CSV_FILE = "vikram.csv"   # your attendance CSV


# ═════════════════════════════════════════════════════════════════════════════
#  Utility helpers
# ═════════════════════════════════════════════════════════════════════════════

def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception:
        return None


def load_csv_data():
    """Read attendance CSV → list of dicts (skip unknown / blank rows)."""
    rows = []
    if not os.path.exists(CSV_FILE):
        return rows
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("ID") or row["ID"].strip() in ("", "Unknown"):
                continue
            # normalise date format  dd/mm/yyyy  or  dd-mm-yyyy
            date_raw = row.get("Date", "").strip()
            for sep in ("/", "-"):
                if sep in date_raw:
                    parts = date_raw.split(sep)
                    if len(parts) == 3:
                        try:
                            row["_date"] = datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
                        except Exception:
                            row["_date"] = None
                    break
            rows.append(row)
    return rows


def get_students_from_db():
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT Student_id, name, roll, depatment FROM student")
        return cur.fetchall()
    except Exception:
        return []
    finally:
        conn.close()


def calc_stats(rows):
    """Aggregate stats from CSV rows."""
    total_days = set()
    student_stats = defaultdict(lambda: {"name": "", "roll": "", "dept": "", "days_present": set(), "days_absent": set()})

    for r in rows:
        d = r.get("_date")
        if d:
            total_days.add(d)
        sid = r["ID"].strip()
        student_stats[sid]["name"] = r.get("Name", "").strip()
        student_stats[sid]["roll"] = r.get("Roll", "").strip()
        student_stats[sid]["dept"] = r.get("Department", "").strip()
        if d:
            student_stats[sid]["days_present"].add(d)

    return total_days, student_stats


# ═════════════════════════════════════════════════════════════════════════════
#  Color & style constants
# ═════════════════════════════════════════════════════════════════════════════

BG         = "#0F1117"   # page background
SURFACE    = "#1A1D27"   # card / panel
SURFACE2   = "#22263A"   # inner card
BORDER     = "#2E3250"
ACCENT     = "#4F8EF7"   # blue
GREEN      = "#2ECC71"
RED        = "#E74C3C"
AMBER      = "#F39C12"
PURPLE     = "#9B59B6"
TEXT_PRI   = "#EAEAF0"
TEXT_SEC   = "#8A8FA8"
TEXT_MUTED = "#5A5F7A"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_HEAD   = ("Segoe UI", 14, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 11)

CHART_STYLE = {
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE2,
    "savefig.facecolor": SURFACE,

    "axes.edgecolor": BORDER,
    "axes.labelcolor": TEXT_SEC,

    "xtick.color": TEXT_SEC,
    "ytick.color": TEXT_SEC,

    "text.color": TEXT_PRI,

    "grid.color": BORDER,
    "grid.alpha": 0.5,

    "axes.spines.top": False,
    "axes.spines.right": False,

    "axes.titlecolor": TEXT_PRI,
    "axes.titleweight": "bold",

    "legend.facecolor": SURFACE,
    "legend.edgecolor": BORDER,
}


# ═════════════════════════════════════════════════════════════════════════════
#  Main Dashboard Class
# ═════════════════════════════════════════════════════════════════════════════

class Dashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Analytics Dashboard")
        self.root.geometry("1530x860+0+0")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self._all_rows = []
        self._filtered_rows = []
        self._period = StringVar(value="All Time")
        self._search_var = StringVar()
        self._dept_var = StringVar(value="All Departments")

        self._build_ui()
        self.refresh_data()

    # ─── UI Construction ─────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top header bar ──────────────────────────────────────────────────
        header = Frame(self.root, bg=SURFACE, height=64)
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(header, text="📊  Attendance Analytics Dashboard",
              font=("Segoe UI", 18, "bold"), bg=SURFACE, fg=TEXT_PRI
              ).place(x=24, y=16)

        # Refresh button
        Button(header, text="⟳  Refresh", command=self.refresh_data,
               font=FONT_BODY, bg=ACCENT, fg="white", bd=0,
               padx=14, pady=6, cursor="hand2", relief=FLAT
               ).place(relx=0.78, y=14)

        # Export CSV button
        Button(header, text="⬇  Export Report", command=self.export_report,
               font=FONT_BODY, bg=GREEN, fg="white", bd=0,
               padx=14, pady=6, cursor="hand2", relief=FLAT
               ).place(relx=0.87, y=14)

        # Close / back
        Button(header, text="✕  Close", command=self.root.destroy,
               font=FONT_BODY, bg=RED, fg="white", bd=0,
               padx=14, pady=6, cursor="hand2", relief=FLAT
               ).place(relx=0.95, y=14)

        # ── Filter bar ──────────────────────────────────────────────────────
        fbar = Frame(self.root, bg=SURFACE2, height=50)
        fbar.pack(fill=X, pady=(1, 0))
        fbar.pack_propagate(False)

        Label(fbar, text="Period:", font=FONT_SMALL, bg=SURFACE2, fg=TEXT_SEC).place(x=16, y=15)
        period_cb = ttk.Combobox(fbar, textvariable=self._period, state="readonly",
                                 values=["All Time", "Today", "This Week", "This Month"],
                                 width=14, font=FONT_SMALL)
        period_cb.place(x=68, y=13)
        period_cb.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())

        Label(fbar, text="Department:", font=FONT_SMALL, bg=SURFACE2, fg=TEXT_SEC).place(x=240, y=15)
        self._dept_cb = ttk.Combobox(fbar, textvariable=self._dept_var, state="readonly",
                                     values=["All Departments"], width=18, font=FONT_SMALL)
        self._dept_cb.place(x=320, y=13)
        self._dept_cb.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())

        Label(fbar, text="Search Student:", font=FONT_SMALL, bg=SURFACE2, fg=TEXT_SEC).place(x=500, y=15)
        Entry(fbar, textvariable=self._search_var, font=FONT_SMALL, bg=SURFACE,
              fg=TEXT_PRI, insertbackground=ACCENT, bd=0, relief=FLAT, width=22
              ).place(x=610, y=13, height=26)
        self._search_var.trace_add("write", lambda *a: self._apply_filters())

        self._filter_info = Label(fbar, text="", font=FONT_SMALL, bg=SURFACE2, fg=ACCENT)
        self._filter_info.place(x=840, y=15)

        # ── Notebook (tabs) ──────────────────────────────────────────────────
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TNotebook", background=BG, borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
                        background=SURFACE2, foreground=TEXT_SEC,
                        font=("Segoe UI", 11, "bold"),
                        padding=[18, 8], borderwidth=0)
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        self._nb = ttk.Notebook(self.root, style="Dark.TNotebook")
        self._nb.pack(fill=BOTH, expand=True, padx=0, pady=2)

        # Tab 1 – Overview
        self._tab_overview = Frame(self._nb, bg=BG)
        self._nb.add(self._tab_overview, text="  📋  Overview  ")

        # Tab 2 – Student Detail
        self._tab_student = Frame(self._nb, bg=BG)
        self._nb.add(self._tab_student, text="  👤  Student Detail  ")

        # Tab 3 – All Records
        self._tab_records = Frame(self._nb, bg=BG)
        self._nb.add(self._tab_records, text="  📂  All Records  ")

        # Tab 4 – Charts
        self._tab_charts = Frame(self._nb, bg=BG)
        self._nb.add(self._tab_charts, text="  📈  Graphs & Analytics  ")

        self._build_overview_tab()
        self._build_student_tab()
        self._build_records_tab()
        self._build_charts_tab()

    # ═══════════════ TAB 1 – Overview ════════════════════════════════════════

    def _build_overview_tab(self):
        p = self._tab_overview

        # ── Stat cards row ──────────────────────────────────────────────────
        self._stat_frame = Frame(p, bg=BG)
        self._stat_frame.pack(fill=X, padx=20, pady=(16, 8))

        self._stat_cards = {}
        for label in ["Total Students", "Total Classes", "Avg Attendance %",
                       "Present Today", "Below 75%", "Top Performer"]:
            c = self._make_stat_card(self._stat_frame, label, "--")
            self._stat_cards[label] = c
            c["frame"].pack(side=LEFT, padx=8, expand=True, fill=X)

        # ── Two columns below ────────────────────────────────────────────────
        cols = Frame(p, bg=BG)
        cols.pack(fill=BOTH, expand=True, padx=20, pady=4)

        # Left – dept attendance table
        left = Frame(cols, bg=SURFACE, bd=0)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        Label(left, text="Department-wise Attendance", font=FONT_HEAD, bg=SURFACE, fg=TEXT_PRI
              ).pack(anchor=W, padx=16, pady=(12, 4))

        cols_dept = ("Department", "Students", "Classes", "Avg %")
        self._dept_tree = ttk.Treeview(left, columns=cols_dept, show="headings", height=10)
        self._style_tree(self._dept_tree, cols_dept)
        self._dept_tree.pack(fill=BOTH, expand=True, padx=8, pady=(0, 12))

        # Right – recent activity
        right = Frame(cols, bg=SURFACE, bd=0)
        right.pack(side=LEFT, fill=BOTH, expand=True, padx=(8, 0))

        Label(right, text="Recent Attendance Activity", font=FONT_HEAD, bg=SURFACE, fg=TEXT_PRI
              ).pack(anchor=W, padx=16, pady=(12, 4))

        rcols = ("Date", "ID", "Name", "Department", "Time", "Status")
        self._recent_tree = ttk.Treeview(right, columns=rcols, show="headings", height=10)
        self._style_tree(self._recent_tree, rcols)
        self._recent_tree.pack(fill=BOTH, expand=True, padx=8, pady=(0, 12))

    def _make_stat_card(self, parent, label, value):
        frame = Frame(parent, bg=SURFACE2, bd=0)
        lbl = Label(frame, text=label, font=FONT_SMALL, bg=SURFACE2, fg=TEXT_SEC)
        lbl.pack(anchor=W, padx=14, pady=(12, 2))
        val = Label(frame, text=value, font=("Segoe UI", 22, "bold"), bg=SURFACE2, fg=TEXT_PRI)
        val.pack(anchor=W, padx=14, pady=(0, 12))
        return {"frame": frame, "label": lbl, "value": val}

    def _update_stat(self, key, val, color=None):
        card = self._stat_cards[key]
        card["value"].config(text=str(val), fg=color or TEXT_PRI)

    # ═══════════════ TAB 2 – Student Detail ══════════════════════════════════

    def _build_student_tab(self):
        p = self._tab_student

        # Search bar
        top = Frame(p, bg=BG)
        top.pack(fill=X, padx=20, pady=(16, 8))

        Label(top, text="Student Name or Roll:", font=FONT_BODY, bg=BG, fg=TEXT_SEC).pack(side=LEFT)
        self._stu_search = Entry(top, font=FONT_BODY, bg=SURFACE, fg=TEXT_PRI,
                                 insertbackground=ACCENT, bd=0, relief=FLAT, width=28)
        self._stu_search.pack(side=LEFT, padx=(8, 0), ipady=5, ipadx=8)
        Button(top, text="Search", command=self._search_student,
               font=FONT_BODY, bg=ACCENT, fg="white", bd=0, padx=12, pady=4,
               cursor="hand2", relief=FLAT).pack(side=LEFT, padx=8)
        Button(top, text="Show All", command=self._show_all_students,
               font=FONT_BODY, bg=SURFACE2, fg=TEXT_PRI, bd=0, padx=12, pady=4,
               cursor="hand2", relief=FLAT).pack(side=LEFT)

        # Two panels
        main = Frame(p, bg=BG)
        main.pack(fill=BOTH, expand=True, padx=20, pady=4)

        # Left: student info card
        info_frame = Frame(main, bg=SURFACE, width=340)
        info_frame.pack(side=LEFT, fill=Y, padx=(0, 10))
        info_frame.pack_propagate(False)

        Label(info_frame, text="Student Profile", font=FONT_HEAD, bg=SURFACE, fg=TEXT_PRI
              ).pack(anchor=W, padx=16, pady=(12, 8))

        # Big avatar
        self._avatar_label = Label(info_frame, text="?", font=("Segoe UI", 48, "bold"),
                                    bg=ACCENT, fg="white", width=4, height=2)
        self._avatar_label.pack(pady=(8, 16))

        self._info_labels = {}
        fields = [("Name", TEXT_PRI), ("Roll No", TEXT_SEC), ("Department", TEXT_SEC),
                  ("Days Present", GREEN), ("Days Absent", RED), ("Attendance %", AMBER),
                  ("Last Seen", TEXT_SEC), ("Status", TEXT_PRI)]
        for f, col in fields:
            row = Frame(info_frame, bg=SURFACE)
            row.pack(fill=X, padx=16, pady=3)
            Label(row, text=f"{f}:", font=FONT_SMALL, bg=SURFACE, fg=TEXT_MUTED, width=14, anchor=W
                  ).pack(side=LEFT)
            lbl = Label(row, text="—", font=FONT_BODY, bg=SURFACE, fg=col, anchor=W)
            lbl.pack(side=LEFT)
            self._info_labels[f] = lbl

        # Right: attendance log for this student
        right = Frame(main, bg=SURFACE)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        Label(right, text="Attendance Log", font=FONT_HEAD, bg=SURFACE, fg=TEXT_PRI
              ).pack(anchor=W, padx=16, pady=(12, 4))

        log_cols = ("Date", "Day", "Time", "Status")
        self._stu_tree = ttk.Treeview(right, columns=log_cols, show="headings", height=22)
        self._style_tree(self._stu_tree, log_cols)

        sb = ttk.Scrollbar(right, orient=VERTICAL, command=self._stu_tree.yview)
        self._stu_tree.configure(yscrollcommand=sb.set)
        self._stu_tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(8, 0), pady=(0, 12))
        sb.pack(side=RIGHT, fill=Y, pady=(0, 12))

        # Month mini-calendar / summary on the right side
        cal_frame = Frame(main, bg=SURFACE, width=220)
        cal_frame.pack(side=LEFT, fill=Y, padx=(10, 0))
        cal_frame.pack_propagate(False)

        Label(cal_frame, text="Monthly Summary", font=FONT_HEAD, bg=SURFACE, fg=TEXT_PRI
              ).pack(anchor=W, padx=12, pady=(12, 8))

        self._month_summary_frame = Frame(cal_frame, bg=SURFACE)
        self._month_summary_frame.pack(fill=BOTH, expand=True, padx=8, pady=4)

    # ═══════════════ TAB 3 – All Records ═════════════════════════════════════

    def _build_records_tab(self):
        p = self._tab_records

        top = Frame(p, bg=BG)
        top.pack(fill=X, padx=20, pady=(14, 4))
        Label(top, text="All Attendance Records", font=FONT_HEAD, bg=BG, fg=TEXT_PRI).pack(side=LEFT)
        self._rec_count_lbl = Label(top, text="", font=FONT_SMALL, bg=BG, fg=ACCENT)
        self._rec_count_lbl.pack(side=LEFT, padx=12)

        rcols = ("ID", "Roll", "Name", "Department", "Time", "Date", "Status", "% Attendance")
        self._rec_tree = ttk.Treeview(p, columns=rcols, show="headings", height=30)
        self._style_tree(self._rec_tree, rcols)

        vsb = ttk.Scrollbar(p, orient=VERTICAL, command=self._rec_tree.yview)
        hsb = ttk.Scrollbar(p, orient=HORIZONTAL, command=self._rec_tree.xview)
        self._rec_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self._rec_tree.pack(fill=BOTH, expand=True, padx=20, pady=(4, 0))
        vsb.pack(side=RIGHT, fill=Y, padx=(0, 20))
        hsb.pack(fill=X, padx=20)

        # Tag colours
        self._rec_tree.tag_configure("present", foreground=GREEN)
        self._rec_tree.tag_configure("low", foreground=RED)
        self._rec_tree.tag_configure("medium", foreground=AMBER)

    # ═══════════════ TAB 4 – Charts ══════════════════════════════════════════

    def _build_charts_tab(self):
        p = self._tab_charts

        # 2x2 chart grid
        grid = Frame(p, bg=BG)
        grid.pack(fill=BOTH, expand=True, padx=16, pady=12)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)

        self._chart_frames = {}
        positions = {
            "daily": (0, 0, "Daily Attendance Trend"),
            "dept":  (0, 1, "Department-wise Attendance %"),
            "top":   (1, 0, "Top 10 Students by Attendance"),
            "pie":   (1, 1, "Overall Present / Absent Distribution"),
        }
        for key, (r, c, title) in positions.items():
            frame = Frame(grid, bg=SURFACE, bd=0)
            frame.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            Label(frame, text=title, font=FONT_HEAD, bg=SURFACE, fg=TEXT_PRI
                  ).pack(anchor=W, padx=14, pady=(10, 4))
            canvas_frame = Frame(frame, bg=SURFACE)
            canvas_frame.pack(fill=BOTH, expand=True)
            self._chart_frames[key] = canvas_frame

    # ═══════════════ Styling helper ══════════════════════════════════════════

    def _style_tree(self, tree, columns):
        style = ttk.Style()
        style.configure("Dark.Treeview",
                         background=SURFACE2, foreground=TEXT_PRI,
                         fieldbackground=SURFACE2, borderwidth=0,
                         rowheight=28, font=FONT_SMALL)
        style.configure("Dark.Treeview.Heading",
                         background=SURFACE, foreground=TEXT_SEC,
                         font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])
        tree.configure(style="Dark.Treeview")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=CENTER)

    # ═══════════════ Data Loading & Filtering ════════════════════════════════

    def refresh_data(self):
        self._all_rows = load_csv_data()
        # Build dept list
        depts = sorted(set(r.get("Department", "").strip()
                           for r in self._all_rows
                           if r.get("Department", "").strip()))
        self._dept_cb["values"] = ["All Departments"] + depts
        self._dept_var.set("All Departments")
        self._period.set("All Time")
        self._search_var.set("")
        self._filtered_rows = self._all_rows[:]
        self._render_all()

    def _apply_filters(self):
        today = datetime.date.today()
        period = self._period.get()
        dept = self._dept_var.get()
        search = self._search_var.get().strip().lower()

        rows = self._all_rows[:]

        if period == "Today":
            rows = [r for r in rows if r.get("_date") == today]
        elif period == "This Week":
            week_start = today - datetime.timedelta(days=today.weekday())
            rows = [r for r in rows if r.get("_date") and r["_date"] >= week_start]
        elif period == "This Month":
            rows = [r for r in rows if r.get("_date") and
                    r["_date"].month == today.month and r["_date"].year == today.year]

        if dept != "All Departments":
            rows = [r for r in rows if r.get("Department", "").strip() == dept]

        if search:
            rows = [r for r in rows if
                    search in r.get("Name", "").lower() or
                    search in r.get("Roll", "").lower() or
                    search in r.get("ID", "").lower()]

        self._filtered_rows = rows
        n = len(rows)
        self._filter_info.config(text=f"Showing {n} record{'s' if n != 1 else ''}")
        self._render_all()

    def _render_all(self):
        rows = self._filtered_rows
        total_days, student_stats = calc_stats(rows)

        self._render_overview(rows, total_days, student_stats)
        self._render_records(rows, student_stats, len(total_days))
        self._render_charts(rows, total_days, student_stats)

    # ═══════════════ Render Overview Tab ═════════════════════════════════════

    def _render_overview(self, rows, total_days, student_stats):
        n_students = len(student_stats)
        n_classes  = len(total_days)
        today = datetime.date.today()

        # Average attendance %
        if n_students and n_classes:
            percs = [(len(v["days_present"]) / n_classes) * 100 for v in student_stats.values()]
            avg_perc = sum(percs) / len(percs)
        else:
            avg_perc = 0.0

        # Present today
        today_rows = [r for r in rows if r.get("_date") == today]
        present_today = len(set(r["ID"] for r in today_rows))

        # Below 75%
        below = sum(1 for v in student_stats.values()
                    if n_classes and (len(v["days_present"]) / n_classes) * 100 < 75)

        # Top performer
        if student_stats and n_classes:
            top_id = max(student_stats, key=lambda k: len(student_stats[k]["days_present"]))
            top_name = student_stats[top_id]["name"] or top_id
        else:
            top_name = "—"

        self._update_stat("Total Students", n_students)
        self._update_stat("Total Classes", n_classes)
        self._update_stat("Avg Attendance %", f"{avg_perc:.1f}%",
                          GREEN if avg_perc >= 75 else RED)
        self._update_stat("Present Today", present_today, GREEN)
        self._update_stat("Below 75%", below, RED if below else GREEN)
        self._update_stat("Top Performer", top_name, ACCENT)

        # Dept table
        for i in self._dept_tree.get_children():
            self._dept_tree.delete(i)

        dept_agg = defaultdict(lambda: {"students": set(), "present": 0, "total": 0})
        for sid, s in student_stats.items():
            dept_agg[s["dept"]]["students"].add(sid)
            dept_agg[s["dept"]]["present"] += len(s["days_present"])
            dept_agg[s["dept"]]["total"] += n_classes

        for dept, info in sorted(dept_agg.items()):
            perc = (info["present"] / info["total"] * 100) if info["total"] else 0
            self._dept_tree.insert("", END, values=(
                dept, len(info["students"]), n_classes, f"{perc:.1f}%"
            ))

        # Recent rows (last 20)
        for i in self._recent_tree.get_children():
            self._recent_tree.delete(i)
        sorted_rows = sorted(rows, key=lambda r: (r.get("_date") or datetime.date.min), reverse=True)
        for r in sorted_rows[:20]:
            d = r.get("_date")
            day_name = d.strftime("%A") if d else ""
            self._recent_tree.insert("", END, values=(
                r.get("Date", ""), r.get("ID", ""), r.get("Name", ""),
                r.get("Department", ""), r.get("Time", ""), r.get("Status", "")
            ))

    # ═══════════════ Render Records Tab ══════════════════════════════════════

    def _render_records(self, rows, student_stats, n_classes):
        for i in self._rec_tree.get_children():
            self._rec_tree.delete(i)

        self._rec_count_lbl.config(text=f"({len(rows)} records)")

        for r in rows:
            sid = r["ID"].strip()
            days_pres = len(student_stats[sid]["days_present"]) if sid in student_stats else 0
            perc = (days_pres / n_classes * 100) if n_classes else 0
            tag = "present" if perc >= 75 else ("medium" if perc >= 60 else "low")
            self._rec_tree.insert("", END, values=(
                r.get("ID", ""), r.get("Roll", ""), r.get("Name", ""),
                r.get("Department", ""), r.get("Time", ""), r.get("Date", ""),
                r.get("Status", ""), f"{perc:.1f}%"
            ), tags=(tag,))

    # ═══════════════ Render Charts Tab ═══════════════════════════════════════

    def _render_charts(self, rows, total_days, student_stats):
        plt.rcParams.update(CHART_STYLE)

        # ── Chart 1: Daily trend ─────────────────────────────────────────────
        self._clear_frame(self._chart_frames["daily"])
        day_counts = defaultdict(int)
        for r in rows:
            d = r.get("_date")
            if d:
                day_counts[d] += 1

        fig1, ax1 = plt.subplots(figsize=(5.8, 3.2))
        fig1.patch.set_facecolor(SURFACE)
        ax1.set_facecolor(SURFACE2)
        if day_counts:
            dates = sorted(day_counts)
            counts = [day_counts[d] for d in dates]
            date_strs = [d.strftime("%d %b") for d in dates]
            ax1.bar(date_strs, counts, color=ACCENT, alpha=0.85, width=0.6, zorder=3)
            ax1.plot(date_strs, counts, color=GREEN, linewidth=1.5, marker="o",
                     markersize=4, zorder=4)
            ax1.set_ylabel("Students Present", color=TEXT_SEC, fontsize=9)
            ax1.tick_params(axis="x", rotation=30, labelsize=8)
            ax1.tick_params(axis="y", labelsize=8)
            ax1.grid(axis="y", alpha=0.3, color=BORDER)
        else:
            ax1.text(0.5, 0.5, "No data", ha="center", va="center",
                     transform=ax1.transAxes, color=TEXT_MUTED)
        fig1.tight_layout(pad=0.8)
        FigureCanvasTkAgg(fig1, self._chart_frames["daily"]).get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close(fig1)

        # ── Chart 2: Dept bar ─────────────────────────────────────────────────
        self._clear_frame(self._chart_frames["dept"])
        fig2, ax2 = plt.subplots(figsize=(5.8, 3.2))
        fig2.patch.set_facecolor(SURFACE)
        ax2.set_facecolor(SURFACE2)
        n_classes = len(total_days)
        dept_perc = defaultdict(list)
        for s in student_stats.values():
            d = s["dept"] or "Unknown"
            perc = (len(s["days_present"]) / n_classes * 100) if n_classes else 0
            dept_perc[d].append(perc)

        if dept_perc:
            depts = sorted(dept_perc)
            avgs = [sum(dept_perc[d]) / len(dept_perc[d]) for d in depts]
            colors = [GREEN if a >= 75 else AMBER if a >= 60 else RED for a in avgs]
            bars = ax2.barh(depts, avgs, color=colors, alpha=0.85, height=0.5, zorder=3)
            ax2.set_xlim(0, 110)
            ax2.axvline(75, color=AMBER, linestyle="--", linewidth=1, alpha=0.7, label="75% threshold")
            for bar, val in zip(bars, avgs):
                ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                         f"{val:.1f}%", va="center", color=TEXT_SEC, fontsize=8)
            ax2.tick_params(labelsize=8)
            ax2.grid(axis="x", alpha=0.3, color=BORDER)
            ax2.legend(fontsize=7, facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT_SEC)
        else:
            ax2.text(0.5, 0.5, "No data", ha="center", va="center",
                     transform=ax2.transAxes, color=TEXT_MUTED)
        fig2.tight_layout(pad=0.8)
        FigureCanvasTkAgg(fig2, self._chart_frames["dept"]).get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close(fig2)

        # ── Chart 3: Top 10 students ──────────────────────────────────────────
        self._clear_frame(self._chart_frames["top"])
        fig3, ax3 = plt.subplots(figsize=(5.8, 3.2))
        fig3.patch.set_facecolor(SURFACE)
        ax3.set_facecolor(SURFACE2)
        if student_stats and n_classes:
            sorted_stu = sorted(student_stats.items(),
                                key=lambda x: len(x[1]["days_present"]), reverse=True)[:10]
            names = [s["name"] or sid[:8] for sid, s in sorted_stu]
            percs = [(len(s["days_present"]) / n_classes * 100) for _, s in sorted_stu]
            colors = [GREEN if p >= 75 else AMBER if p >= 60 else RED for p in percs]
            ax3.barh(names[::-1], percs[::-1], color=colors[::-1], alpha=0.85, height=0.6, zorder=3)
            ax3.axvline(75, color=AMBER, linestyle="--", linewidth=1, alpha=0.7)
            ax3.set_xlim(0, 110)
            ax3.tick_params(labelsize=8)
            ax3.grid(axis="x", alpha=0.3, color=BORDER)
        else:
            ax3.text(0.5, 0.5, "No data", ha="center", va="center",
                     transform=ax3.transAxes, color=TEXT_MUTED)
        fig3.tight_layout(pad=0.8)
        FigureCanvasTkAgg(fig3, self._chart_frames["top"]).get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close(fig3)

        # ── Chart 4: Pie chart ────────────────────────────────────────────────
        self._clear_frame(self._chart_frames["pie"])
        fig4, ax4 = plt.subplots(figsize=(5.8, 3.2))
        fig4.patch.set_facecolor(SURFACE)
        ax4.set_facecolor(SURFACE)
        if student_stats and n_classes:
            all_present = sum(len(s["days_present"]) for s in student_stats.values())
            all_possible = len(student_stats) * n_classes
            all_absent = all_possible - all_present
            if all_possible > 0:
                sizes = [all_present, all_absent]
                labels = [f"Present\n{all_present}", f"Absent\n{all_absent}"]
                colors_pie = [GREEN, RED]
                wedges, texts, autotexts = ax4.pie(
                    sizes, labels=labels, colors=colors_pie,
                    autopct="%1.1f%%", startangle=90,
                    wedgeprops={"linewidth": 2, "edgecolor": SURFACE},
                    textprops={"color": TEXT_PRI, "fontsize": 9}
                )
                for at in autotexts:
                    at.set_color("white")
                    at.set_fontweight("bold")
                    at.set_fontsize(9)
        else:
            ax4.text(0.5, 0.5, "No data", ha="center", va="center",
                     transform=ax4.transAxes, color=TEXT_MUTED)
        fig4.tight_layout(pad=0.8)
        FigureCanvasTkAgg(fig4, self._chart_frames["pie"]).get_tk_widget().pack(fill=BOTH, expand=True)
        plt.close(fig4)

    def _clear_frame(self, frame):
        for w in frame.winfo_children():
            w.destroy()

    # ═══════════════ Student Detail Search ═══════════════════════════════════

    def _search_student(self):
        query = self._stu_search.get().strip().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a name or roll number.", parent=self.root)
            return
        rows = [r for r in self._all_rows if
                query in r.get("Name", "").lower() or
                query in r.get("Roll", "").lower() or
                query in r.get("ID", "").lower()]
        if not rows:
            messagebox.showinfo("Not Found", f"No records found for '{query}'.", parent=self.root)
            return
        self._display_student(rows)

    def _show_all_students(self):
        # Show first student's full records as demo; better: show list
        self._stu_search.delete(0, END)
        self._display_student(self._all_rows)

    def _display_student(self, rows):
        total_days, student_stats = calc_stats(self._all_rows)  # use ALL rows for %
        n_classes = len(total_days)

        # Find the most relevant student
        for i in self._stu_tree.get_children():
            self._stu_tree.delete(i)

        # Group by student (show the first found student's profile)
        first_sid = None
        for r in rows:
            sid = r["ID"].strip()
            if sid and sid != "Unknown":
                first_sid = sid
                break

        if not first_sid:
            return

        s = student_stats[first_sid]
        days_pres = len(s["days_present"])
        perc = (days_pres / n_classes * 100) if n_classes else 0
        days_abs = n_classes - days_pres

        # Avatar initials
        name = s["name"] or first_sid
        initials = "".join(w[0].upper() for w in name.split()[:2]) if name else "?"
        self._avatar_label.config(text=initials)

        # Status
        if perc >= 75:
            status_text, status_col = "✅ Good Standing", GREEN
        elif perc >= 60:
            status_text, status_col = "⚠ Warning", AMBER
        else:
            status_text, status_col = "❌ Low Attendance", RED

        info = {
            "Name": name,
            "Roll No": s["roll"],
            "Department": s["dept"],
            "Days Present": str(days_pres),
            "Days Absent": str(days_abs),
            "Attendance %": f"{perc:.1f}%",
            "Last Seen": max(s["days_present"]).strftime("%d %b %Y") if s["days_present"] else "—",
            "Status": status_text,
        }
        for f, lbl in self._info_labels.items():
            lbl.config(text=info.get(f, "—"))
        self._info_labels["Status"].config(fg=status_col)
        self._info_labels["Attendance %"].config(
            fg=GREEN if perc >= 75 else AMBER if perc >= 60 else RED)

        # Attendance log
        stu_rows = [r for r in self._all_rows if r["ID"].strip() == first_sid]
        stu_rows_sorted = sorted(stu_rows, key=lambda r: r.get("_date") or datetime.date.min, reverse=True)
        for r in stu_rows_sorted:
            d = r.get("_date")
            day_name = d.strftime("%A") if d else ""
            self._stu_tree.insert("", END, values=(
                r.get("Date", ""), day_name, r.get("Time", ""), r.get("Status", "")
            ))

        # Monthly summary
        for w in self._month_summary_frame.winfo_children():
            w.destroy()

        month_data = defaultdict(int)
        for d in s["days_present"]:
            month_data[d.strftime("%b %Y")] += 1

        for month, cnt in sorted(month_data.items(),
                                  key=lambda x: datetime.datetime.strptime(x[0], "%b %Y"),
                                  reverse=True):
            row = Frame(self._month_summary_frame, bg=SURFACE)
            row.pack(fill=X, pady=3)
            Label(row, text=month, font=FONT_SMALL, bg=SURFACE, fg=TEXT_SEC, width=12, anchor=W
                  ).pack(side=LEFT)
            Label(row, text=f"{cnt} days", font=("Segoe UI", 11, "bold"),
                  bg=SURFACE, fg=GREEN, anchor=W).pack(side=LEFT)

    # ═══════════════ Export ══════════════════════════════════════════════════

    def export_report(self):
        total_days, student_stats = calc_stats(self._filtered_rows)
        n_classes = len(total_days)

        if not student_stats:
            messagebox.showinfo("Export", "No data to export.", parent=self.root)
            return

        fln = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],
            title="Save Report",
            parent=self.root,
        )
        if not fln:
            return

        with open(fln, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Student ID", "Roll", "Name", "Department",
                              "Days Present", "Days Absent", "Total Classes",
                              "Attendance %", "Status"])
            for sid, s in sorted(student_stats.items(), key=lambda x: x[1]["name"]):
                pres = len(s["days_present"])
                abs_ = n_classes - pres
                perc = (pres / n_classes * 100) if n_classes else 0
                status = "Good" if perc >= 75 else "Warning" if perc >= 60 else "Low"
                writer.writerow([sid, s["roll"], s["name"], s["dept"],
                                  pres, abs_, n_classes, f"{perc:.1f}%", status])

        messagebox.showinfo("Exported", f"Report saved to:\n{os.path.basename(fln)}", parent=self.root)


# ═════════════════════════════════════════════════════════════════════════════
#  Entry point (standalone or imported from main.py)
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = Tk()
    Dashboard(root)
    root.mainloop()