import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window

# Set background color to dark blue
Window.clearcolor = (0.04, 0.07, 0.17, 1)

class MathApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        
        self.score = 0
        self.streak = 0
        self.time_left = 40
        self.timer_event = None
        
        self.difficulty_ranges = {
            "10s (1-10)": (1, 10),
            "100s (10-100)": (10, 100),
            "1,000s (100-1000)": (100, 1000),
            "100,000s (10k-100k)": (10000, 100000)
        }
        
        # Header
        self.add_widget(Label(
            text="PM SHRI GOVT SEN SEC SCHOOL\nCHEEMA JODHPUR", 
            font_size='14sp', bold=True, color=(0.98, 0.8, 0.08, 1), halign='center'
        ))
        
        # Controls
        self.op_spinner = Spinner(
            text="Addition (+)",
            values=["Addition (+)", "Subtraction (-)", "Multiplication (*)", "Division (/)"],
            size_hint=(1, None), height=40
        )
        self.op_spinner.bind(text=self.generate_question)
        self.add_widget(self.op_spinner)
        
        self.diff_spinner = Spinner(
            text="10s (1-10)",
            values=list(self.difficulty_ranges.keys()),
            size_hint=(1, None), height=40
        )
        self.diff_spinner.bind(text=self.generate_question)
        self.add_widget(self.diff_spinner)
        
        # Stats Bar
        self.stats_label = Label(
            text="Score: 0  |  Time: 40s  |  Streak: 0", 
            font_size='14sp', color=(0.98, 0.8, 0.08, 1)
        )
        self.add_widget(self.stats_label)
        
        # Question Display
        self.question_label = Label(text="", font_size='32sp', bold=True, color=(1, 1, 1, 1))
        self.add_widget(self.question_label)
        
        # Answer Entry
        self.answer_input = TextInput(
            multiline=False, input_filter='int', 
            font_size='20sp', size_hint=(1, None), height=50,
            halign='center'
        )
        self.add_widget(self.answer_input)
        
        # Submit Button
        self.submit_btn = Button(
            text="CHECK ANSWER", font_size='16sp', bold=True,
            background_color=(0.98, 0.8, 0.08, 1), color=(0.04, 0.07, 0.17, 1),
            size_hint=(1, None), height=50
        )
        self.submit_btn.bind(on_press=self.check_answer)
        self.add_widget(self.submit_btn)
        
        # Feedback Label
        self.feedback_label = Label(text="", font_size='14sp', bold=True)
        self.add_widget(self.feedback_label)
        
        # Footer
        self.add_widget(Label(
            text="TOOL BY JATINDER JOSHI", 
            font_size='12sp', bold=True, color=(0.98, 0.8, 0.08, 1)
        ))
        
        self.generate_question()

    def generate_question(self, *args):
        if self.timer_event:
            self.timer_event.cancel()
            
        self.answer_input.text = ""
        self.feedback_label.text = ""
        self.time_left = 40
        
        low, high = self.difficulty_ranges[self.diff_spinner.text]
        op = self.op_spinner.text
        
        if "Addition" in op:
            self.num1, self.num2 = random.randint(low, high), random.randint(low, high)
            self.operation = "+"
            self.correct_answer = self.num1 + self.num2
        elif "Subtraction" in op:
            a, b = random.randint(low, high), random.randint(low, high)
            self.num1, self.num2 = max(a, b), min(a, b)
            self.operation = "-"
            self.correct_answer = self.num1 - self.num2
        elif "Multiplication" in op:
            self.num1 = random.randint(low, max(10, high // 10))
            self.num2 = random.randint(1, 12)
            self.operation = "*"
            self.correct_answer = self.num1 * self.num2
        elif "Division" in op:
            self.num2 = random.randint(2, 12)
            multiplier = random.randint(low, high)
            self.num1 = self.num2 * multiplier
            self.operation = "/"
            self.correct_answer = self.num1 // self.num2

        self.question_label.text = f"{self.num1:,} {self.operation} {self.num2:,}"
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.stats_label.text = f"Score: {self.score}  |  Time: {self.time_left}s  |  Streak: {self.streak}"
        
        if self.time_left <= 0:
            self.timer_event.cancel()
            self.streak = 0
            self.feedback_label.text = f"Time Up! Answer was {self.correct_answer}"
            self.feedback_label.color = (1, 0.2, 0.2, 1)
            Clock.schedule_once(self.generate_question, 1.5)

    def check_answer(self, instance):
        if not self.answer_input.text:
            return
            
        if self.timer_event:
            self.timer_event.cancel()
            
        try:
            user_ans = int(self.answer_input.text)
            if user_ans == self.correct_answer:
                self.score += 10
                self.streak += 1
                self.feedback_label.text = "Correct! Great job!"
                self.feedback_label.color = (0.2, 0.8, 0.2, 1)
            else:
                self.streak = 0
                self.feedback_label.text = f"Wrong! Correct answer: {self.correct_answer}"
                self.feedback_label.color = (1, 0.2, 0.2, 1)
                
            self.stats_label.text = f"Score: {self.score}  |  Time: {self.time_left}s  |  Streak: {self.streak}"
            Clock.schedule_once(self.generate_question, 1.2)
        except ValueError:
            pass

class MathAppMain(App):
    def build(self):
        return MathApp()

if __name__ == '__main__':
    MathAppMain().run()
