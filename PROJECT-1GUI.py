import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ==========================================
# DATABASE SETUP
# ==========================================
def init_db():
    conn = sqlite3.connect("PROJECT-1.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """)
    conn.commit()
    conn.close()

# ==========================================
# CRUD HELPERS
# ==========================================
def db_add(name, age, grade, email):
    conn = sqlite3.connect("PROJECT-1.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, grade, email) VALUES (?, ?, ?, ?)",
        (name, age, grade, email)
    )
    conn.commit()
    conn.close()

def db_fetch_all(search_term=""):
    conn = sqlite3.connect("PROJECT-1.db")
    cur = conn.cursor()
    if search_term:
        like = f"%{search_term}%"
        cur.execute(
            "SELECT * FROM students WHERE name LIKE ? OR email LIKE ? OR grade LIKE ?",
            (like, like, like)
        )
    else:
        cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def db_update(student_id, name, age, grade, email):
    conn = sqlite3.connect("PROJECT-1.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name = ?, age = ?, grade = ?, email = ? WHERE id = ?",
        (name, age, grade, email, student_id)
    )
    conn.commit()
    conn.close()

def db_delete(student_id):
    conn = sqlite3.connect("PROJECT-1.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

# ==========================================
# MAIN APP CLASS
# ==========================================
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f4f8")
        
        self.selected_id = None # Tracks which student is selected for update/delete
        
        self._build_header()
        self._build_form()
        self._build_buttons()
        self._build_table()
        self._build_status_bar()
        self.load_table()

    # Header section
    def _build_header(self):
        header = tk.Frame(self.root, bg="#2c3e50", pady=14)
        header.pack(fill="x")
        tk.Label(
            header, text="Student Management System",
            font=("Segoe UI", 18, "bold"),
            bg="#2c3e50", fg="white"
        ).pack()

    # Input Form section
    def _build_form(self):
        form_frame = tk.LabelFrame(
            self.root, text=" Student Details ",
            font=("Segoe UI", 10, "bold"),
            bg="#f0f4f8", fg="#2c3e50",
            padx=15, pady=10
        )
        form_frame.pack(fill="x", padx=20, pady=(12, 0))
        
        labels = ["Name", "Age", "Grade / Class", "Email"]
        self.entries = {}
        
        for i, lbl in enumerate(labels):
            tk.Label(
                form_frame, text=lbl + ":",
                font=("Segoe UI", 10),
                bg="#f0f4f8", fg="#34495e", width=12, anchor="e"
            ).grid(row=i // 2, column=(i % 2) * 2, padx=(10, 4), pady=6, sticky="e")
            
            entry = ttk.Entry(form_frame, font=("Segoe UI", 10), width=28)
            entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=(0, 20), pady=6, sticky="w")
            self.entries[lbl] = entry

        # Search bar integration
        tk.Label(
            form_frame, text="Search:",
            font=("Segoe UI", 10),
            bg="#f0f4f8", fg="#34495e", width=12, anchor="e"
        ).grid(row=2, column=0, padx=(10, 4), pady=6, sticky="e")
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *_: self.load_table(self.search_var.get()))
        search_entry = ttk.Entry(form_frame, textvariable=self.search_var, font=("Segoe UI", 10), width=28)
        search_entry.grid(row=2, column=1, padx=(0, 20), pady=6, sticky="w")

    # Control Buttons
    def _build_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#f0f4f8", pady=10)
        btn_frame.pack(fill="x", padx=20)
        
        btn_cfg = [
            ("Add", "#27ae60", self.add_student),
            ("Update", "#2980b9", self.update_student),
            ("Delete", "#e74c3c", self.delete_student),
            ("Clear", "#8e44ad", self.clear_fields),
            ("Exit", "#7f8c8d", self.root.quit),
        ]
        
        for text, color, cmd in btn_cfg:
            tk.Button(
                btn_frame, text=text,
                bg=color, fg="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat", cursor="hand2",
                padx=14, pady=6,
                activebackground=color, activeforeground="white",
                command=cmd
            ).pack(side="left", padx=6)

    # Data Table View
    def _build_table(self):
        table_frame = tk.Frame(self.root, bg="#f0f4f8")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        cols = ("ID", "Name", "Age", "Grade", "Email")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)
        col_widths = {"ID": 50, "Name": 200, "Age": 60, "Grade": 120, "Email": 250}
        
        for col in cols:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_column(c, False))
            self.tree.column(col, width=col_widths[col], anchor="center")
            
        # Scrollbars configuration
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        
        # Zebra striping for rows
        self.tree.tag_configure("oddrow", background="#ffffff")
        self.tree.tag_configure("evenrow", background="#eaf2fb")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # Bottom Status Bar
    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(
            self.root, textvariable=self.status_var,
            bg="#2c3e50", fg="white",
            font=("Segoe UI", 9), anchor="w", padx=10
        ).pack(fill="x", side="bottom")

    # ==========================================
    # TABLE OPERATIONS
    # ==========================================
    def load_table(self, search_term=""):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = db_fetch_all(search_term)
        for i, row in enumerate(rows):
            tag = "oddrow" if i % 2 == 0 else "evenrow"
            self.tree.insert("", "end", values=row, tags=(tag,))
        self.status_var.set(f"{len(rows)} record(s) found.")

    def on_row_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        if not values:
            return
            
        self.selected_id = values[0]
        self.entries["Name"].delete(0, tk.END)
        self.entries["Name"].insert(0, values[1])
        self.entries["Age"].delete(0, tk.END)
        self.entries["Age"].insert(0, values[2])
        self.entries["Grade / Class"].delete(0, tk.END)
        self.entries["Grade / Class"].insert(0, values[3])
        self.entries["Email"].delete(0, tk.END)
        self.entries["Email"].insert(0, values[4])
        self.status_var.set(f"Selected: {values[1]} (ID {self.selected_id})")

    def _sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)
            
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.tree.item(k, tags=(tag,))
            
        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))

    # ==========================================
    # CRUD ACTIONS & VALIDATIONS
    # ==========================================
    def _get_fields(self):
        name = self.entries["Name"].get().strip()
        age = self.entries["Age"].get().strip()
        grade = self.entries["Grade / Class"].get().strip()
        email = self.entries["Email"].get().strip()
        return name, age, grade, email

    def _validate(self, name, age, grade, email):
        if not all([name, age, grade, email]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return False
        if not age.isdigit() or not (1 <= int(age) <= 120):
            messagebox.showwarning("Invalid Age", "Age must be a number between 1 and 120.")
            return False
        if "@" not in email or "." not in email:
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return False
        return True

    def add_student(self):
        name, age, grade, email = self._get_fields()
        if not self._validate(name, age, grade, email):
            return
        try:
            db_add(name, int(age), grade, email)
            self.load_table()
            self.clear_fields()
            self.status_var.set(f"✓ Student '{name}' added successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Email", "A student with this email already exists.")

    def update_student(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Please click a row in the table to select a student.")
            return
        name, age, grade, email = self._get_fields()
        if not self._validate(name, age, grade, email):
            return
        if not messagebox.askyesno("Confirm Update", f"Update record for '{name}'?"):
            return
        try:
            db_update(self.selected_id, name, int(age), grade, email)
            self.load_table()
            self.clear_fields()
            self.status_var.set(f" Student '{name}' updated successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Email", "Another student already uses this email.")

    def delete_student(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Please click a row in the table to select a student.")
            return
        name = self.entries["Name"].get().strip() or f"ID {self.selected_id}"
        if not messagebox.askyesno("Confirm Delete", f"Delete '{name}'? This cannot be undone."):
            return
        db_delete(self.selected_id)
        self.load_table()
        self.clear_fields()
        self.status_var.set(f" Student '{name}' deleted.")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_id = None
        self.search_var.set("")
        self.status_var.set("Fields cleared. Ready.")

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=26, background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2c3e50", foreground="white")
    style.map("Treeview", background=[("selected", "#2980b9")])
    
    app = StudentApp(root)
    root.mainloop()