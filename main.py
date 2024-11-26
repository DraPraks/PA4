import tkinter as tk
from tkinter import Menu, messagebox
from datetime import datetime as dt
import random

class SimpleChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chatbot")
        self.root.geometry("400x400")

        # Track current theme
        self.current_theme = "light"

        # Chat history for saving sessions
        self.chat_history = []

        # Create Menu Bar
        self.menu_bar = Menu(self.root)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save Session", command=self.save_session)
        self.file_menu.add_command(label="Reset Session", command=self.reset_session)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Theme Menu
        self.theme_menu = Menu(self.menu_bar, tearoff=0)
        self.theme_menu.add_command(label="Light Mode", command=self.set_light_mode)
        self.theme_menu.add_command(label="Dark Mode", command=self.set_dark_mode)
        self.menu_bar.add_cascade(label="Theme", menu=self.theme_menu)

        # About Menu (dummy)
        self.menu_bar.add_cascade(label="About", menu=Menu(self.menu_bar, tearoff=0))

        self.root.config(menu=self.menu_bar)

        # Chat Display Area
        self.text_display = tk.Text(self.root, height=15, width=50)
        self.text_display.insert(tk.END, "Chatbot: Hello! How can I help you today?\n")
        self.text_display.config(state=tk.DISABLED)  # Make text read-only
        self.text_display.pack(pady=10)

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.joke_button = tk.Button(self.button_frame, text="Crack a Joke", command=self.crack_a_joke)
        self.time_button = tk.Button(self.button_frame, text="Time?", command=self.show_time)
        self.math_button = tk.Button(self.button_frame, text="Math Question", command=self.math_question)
        self.xyz_button = tk.Button(self.button_frame, text="XYZ", command=self.xyz_function)

        self.joke_button.grid(row=0, column=0, padx=5, pady=5)
        self.time_button.grid(row=0, column=1, padx=5, pady=5)
        self.math_button.grid(row=0, column=2, padx=5, pady=5)
        self.xyz_button.grid(row=0, column=3, padx=5, pady=5)
        self.button_frame.pack()

        # Entry and Send Button
        self.entry_frame = tk.Frame(self.root)
        self.entry_box = tk.Entry(self.entry_frame, width=35)
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)

        self.entry_box.grid(row=0, column=0, padx=5, pady=5)
        self.send_button.grid(row=0, column=1, padx=5, pady=5)
        self.entry_frame.pack()

    # Functions for Button Actions
    def crack_a_joke(self):
        jokes = [
            "Knock-knock... who's there? PA4",
            "Why did the math book look sad? Because it had problems! HAHA",
            "Why was the computer cold? Idk!"
        ]
        self.append_chatbot_message(random.choice(jokes))

    def show_time(self):
        current_time = dt.now().strftime("%H:%M:%S")
        self.append_chatbot_message(f"The current time is {current_time}.")

    def math_question(self):
        import random
        # Generate two random numbers and a random operator
        num1 = random.randint(1, 20)  # Random number between 1 and 20
        num2 = random.randint(1, 20)
        operator = random.choice(["+", "-", "*", "/"])

        # Formulate the question
        if operator == "/":
            # Ensure the division results in an integer
            num1 = num1 * num2  # Make num1 divisible by num2
        question = f"How much is {num1} {operator} {num2}?"

        # Save the answer for later verification
        self.answer = eval(f"{num1} {operator} {num2}")  # Calculate the correct answer
        self.append_chatbot_message(question)

    def verify_answer(self):
        user_input = self.entry_box.get().strip()
        try:
            if float(user_input) == self.answer:
                self.append_chatbot_message("Correct! 🎉")
            else:
                self.append_chatbot_message(f"Oops! The correct answer is {self.answer}.")
        except ValueError:
            self.append_chatbot_message("Please enter a valid number.")
        self.entry_box.delete(0, tk.END)

    def xyz_function(self):
        self.append_chatbot_message("XYZ feature coming soon!")

    def send_message(self):
        user_input = self.entry_box.get().strip()
        if hasattr(self, "answer"):  # Check if a math question was asked
            self.verify_answer()
        else:
            self.append_user_message(user_input)
        self.entry_box.delete(0, tk.END)

            # Handle specific cases
        if user_input.lower() in ["time", "time?", "time!"]:
            self.show_time()

    def append_user_message(self, message):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, f"You: {message}\n")
        self.text_display.config(state=tk.DISABLED)
        self.chat_history.append(f"You: {message}\n")

    def append_chatbot_message(self, message):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, f"Chatbot: {message}\n")
        self.text_display.config(state=tk.DISABLED)
        self.chat_history.append(f"Chatbot: {message}\n")

    # Save Session
    def save_session(self):
        if not self.chat_history:
            messagebox.showinfo("Info", "No chat history to save.")
            return

        filename = f"chat_session_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        try:
            with open(filename, "w") as file:
                file.writelines(self.chat_history)
            messagebox.showinfo("Success", f"The session has been successfully saved as '{filename}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {e}")

    # Reset Session
    def reset_session(self):
        self.chat_history = []
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, "Chatbot: Hello! How can I help you today?\n")
        self.text_display.config(state=tk.DISABLED)
        messagebox.showinfo("Info", "Session has been reset.")

    # Set Light Mode
    def set_light_mode(self):
        self.current_theme = "light"
        self.root.config(bg="white")
        self.text_display.config(bg="white", fg="black", insertbackground="black")
        self.entry_box.config(bg="white", fg="black", insertbackground="black")
        for button in self.button_frame.winfo_children():
            button.config(bg="white", fg="black")

    # Set Dark Mode
    def set_dark_mode(self):
        self.current_theme = "dark"
        self.root.config(bg="black")
        self.text_display.config(bg="black", fg="white", insertbackground="white")
        self.entry_box.config(bg="black", fg="white", insertbackground="white")
        for button in self.button_frame.winfo_children():
            button.config(bg="black", fg="white")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleChatbotApp(root)
    root.mainloop()
