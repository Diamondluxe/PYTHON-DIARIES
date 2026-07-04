import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# COLOR PALETTE & CONSTANTS
# ==========================================
BG_COLOR = "#f4f7f6"      # Soft grayish-white background
PRIMARY = "#2c3e50"       # Dark slate blue for header/text
ACCENT = "#3498db"        # Bright blue for primary buttons
SUCCESS = "#27ae60"       # Emerald green for correct answer
WRONG = "#e74c3c"         # Crimson red for wrong answer
WHITE = "#ffffff"

# ==========================================
# QUIZ DATA (QUESTIONS & ANSWERS)
# ==========================================
questions = [
    {
        "q": "Which data structure follows the Last-In-First-Out (LIFO) principle?",
        "options": ["Queue", "Linked List", "Stack", "Tree"],
        "correct": 2 # Index 2 is 'Stack'
    },
    {
        "q": "What is the time complexity of searching in a perfectly balanced Binary Search Tree (BST)?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct": 1 # Index 1 is 'O(log n)'
    },
    {
        "q": "Which of the following sorting algorithms has the best worst-case time complexity?",
        "options": ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"],
        "correct": 3 # Index 3 is 'Merge Sort'
    },
    {
        "q": "What does a primary key ensure in a relational database?",
        "options": ["Data redundancy", "Uniqueness of records", "Fast network transfer", "Foreign connections"],
        "correct": 1 # Index 1 is 'Uniqueness of records'
    },
    {
        "q": "In Python, which keyword is used to create a function?",
        "options": ["func", "define", "def", "lambda"],
        "correct": 2 # Index 2 is 'def'
    }
]

LABELS = ["A", "B", "C", "D"]

# ==========================================
# MAIN QUIZ APP CLASS
# ==========================================
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Science Master Quiz")
        self.root.geometry("750x550")
        self.root.configure(bg=BG_COLOR)
        
        # State trackers
        self.q_index = 0
        self.score = 0
        self.selected_option = tk.IntVar(value=-1)
        
        self._build_welcome_screen()

    # 1. First Welcome Screen
    def _build_welcome_screen(self):
        self.clear_screen()
        
        # Main Container
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            frame, text="🧠 CS Master Quiz",
            font=("Segoe UI", 28, "bold"),
            bg=BG_COLOR, fg=PRIMARY
        ).pack(pady=10)
        
        tk.Label(
            frame, text="Test your core Computer Science & Programming knowledge!",
            font=("Segoe UI", 12),
            bg=BG_COLOR, fg="#7f8c8d"
        ).pack(pady=(0, 30))
        
        tk.Button(
            frame, text="Start Quiz",
            bg=ACCENT, fg=WHITE,
            font=("Segoe UI", 12, "bold"),
            padx=30, pady=10, relief="flat", cursor="hand2",
            activebackground="#2980b9", activeforeground=WHITE,
            command=self.start_quiz
        ).pack()

    # 2. Main Question Interface
    def start_quiz(self):
        self.clear_screen()
        self.q_index = 0
        self.score = 0
        self._show_question()

    def _show_question(self):
        self.clear_screen()
        self.selected_option.set(-1) # Reset radio buttons
        
        current_q = questions[self.q_index]
        
        # Progress Bar Header
        header = tk.Frame(self.root, bg=PRIMARY, pady=10)
        header.pack(fill="x")
        
        progress_text = f"Question {self.q_index + 1} of {len(questions)}"
        tk.Label(
            header, text=progress_text,
            font=("Segoe UI", 10, "bold"),
            bg=PRIMARY, fg="#bdc3c7"
        ).pack(side="left", padx=20)
        
        # Main Question Box
        q_frame = tk.Frame(self.root, bg=BG_COLOR, padx=30, pady=20)
        q_frame.pack(fill="both", expand=True)
        
        tk.Label(
            q_frame, text=current_q["q"],
            font=("Segoe UI", 14, "bold"),
            bg=BG_COLOR, fg=PRIMARY,
            wraplength=650, justify="left"
        ).pack(anchor="w", pady=(10, 20))
        
        # Styling Radio Buttons using standard tkinter frames
        self.radio_buttons = []
        for i, option in enumerate(current_q["options"]):
            r_frame = tk.Frame(q_frame, bg=WHITE, bd=1, relief="solid", padx=10, pady=8)
            r_frame.pack(fill="x", pady=5)
            
            rb = tk.Radiobutton(
                r_frame, text=f" {LABELS[i]}.   {option}",
                variable=self.selected_option, value=i,
                font=("Segoe UI", 11),
                bg=WHITE, activebackground=WHITE,
                selectcolor=WHITE, bd=0, highlightthickness=0
            )
            rb.pack(side="left", anchor="w")
            self.radio_buttons.append((r_frame, rb))

        # Feedback text space (For Right/Wrong notifications)
        self.feedback_lbl = tk.Label(q_frame, text="", font=("Segoe UI", 11, "bold"), bg=BG_COLOR)
        self.feedback_lbl.pack(pady=10)

        # Control Buttons Footer
        footer = tk.Frame(self.root, bg=BG_COLOR, pady=15, padx=30)
        footer.pack(fill="x", side="bottom")
        
        self.submit_btn = tk.Button(
            footer, text="Submit Answer",
            bg=PRIMARY, fg=WHITE, font=("Segoe UI", 11, "bold"),
            padx=20, pady=6, relief="flat", cursor="hand2",
            command=self.check_answer
        )
        self.submit_btn.pack(side="right")
        
        self.next_btn = tk.Button(
            footer, text="Next ➜",
            bg=ACCENT, fg=WHITE, font=("Segoe UI", 11, "bold"),
            padx=20, pady=6, relief="flat", cursor="hand2",
            command=self.next_question
        )
        # Hidden initially, revealed after submission
        self.next_btn.pack_forget()

    # 3. Validation and Grade Feedback Logic
    def check_answer(self):
        choice = self.selected_option.get()
        if choice == -1:
            messagebox.showwarning("No Selection", "Please select an answer before submitting!")
            return
            
        correct = questions[self.q_index]["correct"]
        self.submit_btn.pack_forget() # Hide submit button
        
        # Disable all radio buttons after submission
        for r_frame, rb in self.radio_buttons:
            rb.config(state="disabled")

        # Color coding feedback
        if choice == correct:
            self.score += 1
            self.radio_buttons[choice][0].config(bg="#e8f8f5", bd=2) # Green tint
            self.feedback_lbl.config(text="✅ Correct Answer! Keep it up!", fg=SUCCESS)
        else:
            self.radio_buttons[choice][0].config(bg="#fce4d6", bd=2) # Red tint
            self.radio_buttons[correct][0].config(bg="#e8f8f5", bd=2) # Show correct answer in green
            self.feedback_lbl.config(
                text=f"❌ Wrong! Correct Answer was {LABELS[correct]}: {questions[self.q_index]['options'][correct]}",
                fg=WRONG
            )
            
        self.next_btn.pack(side="right")

    def next_question(self):
        self.q_index += 1
        if self.q_index < len(questions):
            self._show_question()
        else:
            self._show_results()

    # 4. Final Performance Screen
    def _show_results(self):
        self.clear_screen()
        total = len(questions)
        pct = self.score / total
        
        # Determine performance feedback dynamically
        if pct >= 0.8:
            emoji, grade = "🏆", "Outstanding! You are a CS Master!"
            color = SUCCESS
        elif pct >= 0.5:
            emoji, grade = "👍", "Good Job! Nice effort!"
            color = ACCENT
        elif pct >= 0.3:
            emoji, grade = "📚", "Keep Practising! You can do better."
            color = "#f39c12"
        else:
            emoji, grade = "💪", "Don't Give Up! Review the concepts."
            color = WRONG

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text=emoji, font=("Segoe UI", 55), bg=BG_COLOR).pack()
        tk.Label(frame, text="Quiz Completed!", font=("Segoe UI", 24, "bold"), bg=BG_COLOR, fg=PRIMARY).pack(pady=5)
        
        tk.Label(
            frame, text=f"Your Score: {self.score} / {total}",
            font=("Segoe UI", 18, "bold"), bg=BG_COLOR, fg=color
        ).pack(pady=10)
        
        tk.Label(frame, text=grade, font=("Segoe UI", 12, "italic"), bg=BG_COLOR, fg="#555555").pack(pady=(0, 30))
        
        # Restart Button
        tk.Button(
            frame, text="Try Again 🔄",
            bg=PRIMARY, fg=WHITE, font=("Segoe UI", 11, "bold"),
            padx=20, pady=8, relief="flat", cursor="hand2",
            command=self._build_welcome_screen
        ).pack()

    # Utility method to refresh views
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ==========================================
# APPLICATION ENTRY POINT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    
    # Global visual setup for standard widgets
    style = ttk.Style()
    style.theme_use("clam")
    
    app = QuizApp(root)
    root.mainloop()