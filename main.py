import random
import customtkinter as ctk

# Force Appearance and Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MathApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Math Learning App")
        self.geometry("420x820")
        self.resizable(False, False)

        # Color Palette - Vivid Royal Blue & Canary Yellow
        self.BG_DARK = "#0B132B"       # Deep Royal Navy Background
        self.CARD_BG = "#1C2541"       # Slate Blue Container Background
        self.YELLOW_ACCENT = "#FACC15" # Vibrant Canary Yellow
        self.BLUE_ACCENT = "#3B82F6"   # Electric Blue

        # Apply Base Background Color
        self.configure(fg_color=self.BG_DARK)

        # App State Variables
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.total_questions = 0
        self.correct_questions = 0
        self.num1 = 0
        self.num2 = 0
        self.operation = "+"
        self.correct_answer = 0

        # Timer Variables
        self.time_left = 40
        self.timer_running = False
        self.timer_job = None

        self.difficulty_ranges = {
            "10s (1-10)": (1, 10),
            "100s (10-100)": (10, 100),
            "1,000s (100-1000)": (100, 1000),
            "100,000s (10k-100k)": (10000, 100000)
        }

        self.setup_ui()
        self.generate_question()

    def setup_ui(self):
        # Upper Header Banner (School Name)
        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.CARD_BG,
            border_color=self.YELLOW_ACCENT,
            border_width=2,
            corner_radius=16
        )
        header_frame.pack(fill="x", padx=15, pady=(12, 6))

        school_title = ctk.CTkLabel(
            header_frame,
            text="PM SHRI GOVT SEN SEC SCHOOL\nCHEEMA JODHPUR",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.YELLOW_ACCENT,
            justify="center"
        )
        school_title.pack(pady=8)

        sub_title = ctk.CTkLabel(
            header_frame,
            text="Math Mastery Academy",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        sub_title.pack(pady=(0, 8))

        # Controls Frame (Operations & Difficulty)
        controls_frame = ctk.CTkFrame(self, fg_color=self.CARD_BG, corner_radius=16)
        controls_frame.pack(fill="x", padx=15, pady=4)

        # Operation Dropdown
        op_label = ctk.CTkLabel(controls_frame, text="Select Operation:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.YELLOW_ACCENT)
        op_label.pack(anchor="w", padx=15, pady=(6, 2))

        self.op_var = ctk.StringVar(value="Addition (+)")
        self.op_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            values=["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"],
            variable=self.op_var,
            command=self.on_setting_change,
            fg_color=self.BLUE_ACCENT,
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_fg_color=self.CARD_BG,
            dropdown_text_color="#FFFFFF",
            text_color="white",
            corner_radius=8
        )
        self.op_dropdown.pack(fill="x", padx=15, pady=(0, 6))

        # Difficulty Dropdown
        diff_label = ctk.CTkLabel(controls_frame, text="Select Range / Difficulty:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.YELLOW_ACCENT)
        diff_label.pack(anchor="w", padx=15, pady=(0, 2))

        self.diff_var = ctk.StringVar(value="10s (1-10)")
        self.diff_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            values=list(self.difficulty_ranges.keys()),
            variable=self.diff_var,
            command=self.on_setting_change,
            fg_color=self.BLUE_ACCENT,
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_fg_color=self.CARD_BG,
            dropdown_text_color="#FFFFFF",
            text_color="white",
            corner_radius=8
        )
        self.diff_dropdown.pack(fill="x", padx=15, pady=(0, 8))

        # Main Question Card Frame
        self.card_frame = ctk.CTkFrame(
            self,
            fg_color=self.CARD_BG,
            corner_radius=20,
            border_color=self.YELLOW_ACCENT,
            border_width=2
        )
        self.card_frame.pack(fill="x", padx=15, pady=6)

        # Stats Row (Score, Timer, Streak)
        stats_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=(10, 0))

        self.score_label = ctk.CTkLabel(stats_frame, text="Score: 0", font=ctk.CTkFont(size=13, weight="bold"), text_color="#60A5FA")
        self.score_label.pack(side="left")

        self.timer_label = ctk.CTkLabel(
            stats_frame,
            text="⏱️ 40s",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.YELLOW_ACCENT
        )
        self.timer_label.pack(side="left", expand=True)

        self.streak_label = ctk.CTkLabel(stats_frame, text="🔥 Streak: 0", font=ctk.CTkFont(size=13, weight="bold"), text_color="#FB923C")
        self.streak_label.pack(side="right")

        # Question Display
        self.question_label = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color="#FFFFFF"
        )
        self.question_label.pack(pady=12)

        # Answer Input Field
        self.answer_entry = ctk.CTkEntry(
            self.card_frame,
            placeholder_text="Enter answer",
            font=ctk.CTkFont(size=20),
            justify="center",
            height=44,
            corner_radius=12,
            fg_color=self.BG_DARK,
            border_color=self.YELLOW_ACCENT,
            border_width=2,
            text_color="#FFFFFF"
        )
        self.answer_entry.pack(padx=25, pady=(0, 10), fill="x")
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        # Main Action Button
        self.submit_btn = ctk.CTkButton(
            self.card_frame,
            text="CHECK ANSWER",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=42,
            corner_radius=12,
            fg_color=self.YELLOW_ACCENT,
            hover_color="#EAB308",
            text_color=self.BG_DARK,
            command=self.check_answer
        )
        self.submit_btn.pack(padx=25, pady=(0, 12), fill="x")

        # Feedback Banner
        self.feedback_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=24
        )
        self.feedback_label.pack(fill="x", padx=15, pady=(2, 4))

        # NEW: Performance Analytics Section (Fills Vacant Space)
        analytics_frame = ctk.CTkFrame(
            self,
            fg_color=self.CARD_BG,
            corner_radius=16,
            border_color="#1D4ED8",
            border_width=1
        )
        analytics_frame.pack(fill="x", padx=15, pady=6)

        analytics_title = ctk.CTkLabel(
            analytics_frame,
            text="📊 Session Performance",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.YELLOW_ACCENT
        )
        analytics_title.pack(pady=(8, 4))

        # Detailed metrics grid
        metrics_grid = ctk.CTkFrame(analytics_frame, fg_color="transparent")
        metrics_grid.pack(fill="x", padx=15, pady=(0, 8))

        self.best_streak_label = ctk.CTkLabel(
            metrics_grid,
            text="Best Streak: 0",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8"
        )
        self.best_streak_label.pack(side="left")

        self.accuracy_label = ctk.CTkLabel(
            metrics_grid,
            text="Accuracy: 0%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4ADE80"
        )
        self.accuracy_label.pack(side="right")

        # Accuracy Progress Bar
        self.accuracy_bar = ctk.CTkProgressBar(
            analytics_frame,
            height=8,
            corner_radius=4,
            progress_color=self.YELLOW_ACCENT,
            fg_color=self.BG_DARK
        )
        self.accuracy_bar.set(0)
        self.accuracy_bar.pack(fill="x", padx=15, pady=(0, 10))

        # Bottom Footer (Branding at Bottom)
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=(0, 10))

        footer_label = ctk.CTkLabel(
            footer_frame,
            text="TOOL BY JATINDER JOSHI",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.YELLOW_ACCENT
        )
        footer_label.pack()

    def on_setting_change(self, choice):
        self.generate_question()

    def stop_timer(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False

    def start_timer(self):
        self.stop_timer()
        self.time_left = 40
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return

        self.timer_label.configure(text=f"⏱️ {self.time_left}s")

        if self.time_left <= 10:
            self.timer_label.configure(text_color="#EF4444")
        else:
            self.timer_label.configure(text_color=self.YELLOW_ACCENT)

        if self.time_left == 0:
            self.stop_timer()
            self.streak = 0
            self.total_questions += 1
            self.update_analytics()
            self.streak_label.configure(text=f"🔥 Streak: {self.streak}")
            self.feedback_label.configure(
                text=f"⏰ Time Up! The answer was {self.correct_answer:,}",
                text_color="#EF4444"
            )
            self.after(1500, self.generate_question)
        else:
            self.time_left -= 1
            self.timer_job = self.after(1000, self.update_timer)

    def generate_question(self):
        self.stop_timer()
        self.answer_entry.delete(0, 'end')
        self.feedback_label.configure(text="")

        low, high = self.difficulty_ranges[self.diff_var.get()]
        selected_op = self.op_var.get()

        if "Addition" in selected_op:
            self.num1 = random.randint(low, high)
            self.num2 = random.randint(low, high)
            self.operation = "+"
            self.correct_answer = self.num1 + self.num2
        elif "Subtraction" in selected_op:
            a = random.randint(low, high)
            b = random.randint(low, high)
            self.num1 = max(a, b)
            self.num2 = min(a, b)
            self.operation = "-"
            self.correct_answer = self.num1 - self.num2
        elif "Multiplication" in selected_op:
            mult_high = max(10, high // 10) if high > 10 else high
            self.num1 = random.randint(low, mult_high)
            self.num2 = random.randint(1, 12 if high <= 100 else 100)
            self.operation = "×"
            self.correct_answer = self.num1 * self.num2
        elif "Division" in selected_op:
            divisor_high = 12 if high <= 100 else 100
            self.num2 = random.randint(2, divisor_high)
            multiplier = random.randint(low, high)
            self.num1 = self.num2 * multiplier
            self.operation = "÷"
            self.correct_answer = self.num1 // self.num2

        self.question_label.configure(text=f"{self.num1:,} {self.operation} {self.num2:,}")
        self.start_timer()

    def update_analytics(self):
        if self.total_questions > 0:
            accuracy = int((self.correct_questions / self.total_questions) * 100)
            self.accuracy_label.configure(text=f"Accuracy: {accuracy}%")
            self.accuracy_bar.set(accuracy / 100.0)

        if self.streak > self.best_streak:
            self.best_streak = self.streak
            self.best_streak_label.configure(text=f"Best Streak: {self.best_streak}")

    def check_answer(self):
        if not self.timer_running:
            return

        user_input = self.answer_entry.get().strip().replace(",", "")

        if not user_input:
            return

        try:
            user_ans = float(user_input) if "." in user_input else int(user_input)
            self.stop_timer()
            self.total_questions += 1

            if user_ans == self.correct_answer:
                self.score += 10
                self.streak += 1
                self.correct_questions += 1
                self.feedback_label.configure(text="✨ Correct! Excellent job!", text_color="#4ADE80")
            else:
                self.streak = 0
                self.feedback_label.configure(
                    text=f"❌ Wrong! Correct answer: {self.correct_answer:,}",
                    text_color="#F87171"
                )

            self.update_analytics()
            self.score_label.configure(text=f"Score: {self.score}")
            self.streak_label.configure(text=f"🔥 Streak: {self.streak}")
            self.after(1200, self.generate_question)

        except ValueError:
            self.feedback_label.configure(text="⚠️ Enter a valid number!", text_color=self.YELLOW_ACCENT)

if __name__ == "__main__":
    app = MathApp()
    app.mainloop()