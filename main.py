"""A simple flashcard learning application using Tkinter and JSON."""

import json
import random
import tkinter as tk
from tkinter import messagebox


DATA_FILE = "flashcards.json"
DEFAULT_FLASHCARDS = {
    "What is Python?": "A high-level, general-purpose programming language.",
    "What is a variable?": "A named place used to store a value.",
    "What is a list?": "An ordered, changeable collection of items.",
    "What is a dictionary?": "A collection that stores key-value pairs.",
    "What does a function do?": "A reusable block of code that performs a task.",
}


def save_flashcards(cards):
    """Write the flashcard dictionary to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(cards, file, indent=4)
    except OSError as error:
        messagebox.showerror("File Error", f"Could not save flashcards:\n{error}")


def load_flashcards():
    """Load saved flashcards, creating defaults if this is the first run."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            cards = json.load(file)
        if not isinstance(cards, dict):
            raise ValueError("The JSON data must be a dictionary.")
        # Keep only non-empty text question/answer pairs.
        return {
            question.strip(): answer.strip()
            for question, answer in cards.items()
            if isinstance(question, str)
            and isinstance(answer, str)
            and question.strip()
            and answer.strip()
        }
    except FileNotFoundError:
        cards = DEFAULT_FLASHCARDS.copy()
        save_flashcards(cards)
        return cards
    except (json.JSONDecodeError, ValueError, TypeError):
        messagebox.showwarning(
            "Invalid File",
            "The flashcards file is invalid. A new file with sample flashcards will be created.",
        )
        cards = DEFAULT_FLASHCARDS.copy()
        save_flashcards(cards)
        return cards
    except OSError as error:
        messagebox.showerror("File Error", f"Could not read flashcards:\n{error}")
        return DEFAULT_FLASHCARDS.copy()


class FlashcardApp:
    """Controls the screens and learning flow of the application."""

    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Learning Application")
        self.root.geometry("620x440")
        self.root.minsize(500, 360)
        self.cards = load_flashcards()
        self.quiz_questions = []
        self.card_index = 0
        self.correct = 0
        self.incorrect = 0
        self.answer_visible = False
        self.show_main_menu()

    def clear_screen(self):
        """Remove the current screen's widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_heading(self, text):
        tk.Label(self.root, text=text, font=("Arial", 18, "bold")).pack(pady=(24, 18))

    def show_main_menu(self):
        self.clear_screen()
        self.add_heading("Flashcard Learning Application")
        tk.Button(self.root, text="Start Learning", width=24, command=self.start_learning).pack(pady=7)
        tk.Button(self.root, text="Add Flashcard", width=24, command=self.show_add_flashcard).pack(pady=7)
        tk.Button(self.root, text="View Flashcards", width=24, command=self.view_flashcards).pack(pady=7)
        tk.Button(self.root, text="Exit", width=24, command=self.root.destroy).pack(pady=7)

    def start_learning(self):
        self.cards = load_flashcards()
        if not self.cards:
            messagebox.showinfo("No Flashcards", "There are no flashcards to study.")
            self.show_main_menu()
            return
        self.quiz_questions = list(self.cards.keys())
        random.shuffle(self.quiz_questions)
        self.card_index = 0
        self.correct = 0
        self.incorrect = 0
        self.show_question()

    def show_question(self):
        if self.card_index >= len(self.quiz_questions):
            self.show_results()
            return
        self.clear_screen()
        self.answer_visible = False
        question = self.quiz_questions[self.card_index]
        self.add_heading("Study Flashcards")
        tk.Label(
            self.root,
            text=f"Question {self.card_index + 1} of {len(self.quiz_questions)}",
            font=("Arial", 10),
        ).pack(pady=4)
        tk.Label(
            self.root, text=question, font=("Arial", 14), wraplength=520, justify="center"
        ).pack(padx=25, pady=20)
        self.answer_label = tk.Label(
            self.root, text="", font=("Arial", 12), wraplength=520, justify="center"
        )
        self.answer_label.pack(padx=25, pady=8)
        self.show_answer_button = tk.Button(
            self.root, text="Show Answer", command=self.show_answer
        )
        self.show_answer_button.pack(pady=10)
        self.choice_frame = tk.Frame(self.root)
        self.choice_frame.pack(pady=8)
        tk.Button(
            self.choice_frame, text="I Know", width=14,
            command=lambda: self.next_card(True)
        ).pack(side="left", padx=6)
        tk.Button(
            self.choice_frame, text="I Don't Know", width=14,
            command=lambda: self.next_card(False)
        ).pack(side="left", padx=6)
        self.choice_frame.pack_forget()
        tk.Button(self.root, text="Reset Quiz", command=self.start_learning).pack(pady=8)
        tk.Button(self.root, text="Main Menu", command=self.show_main_menu).pack(pady=4)

    def show_answer(self):
        if not self.answer_visible:
            question = self.quiz_questions[self.card_index]
            self.answer_label.config(text=self.cards.get(question, "Answer not found."))
            self.answer_visible = True
            self.show_answer_button.config(state="disabled")
            self.choice_frame.pack(pady=8)

    def next_card(self, knew_answer):
        if not self.answer_visible:
            messagebox.showinfo("Show Answer", "Click Show Answer before choosing.")
            return
        if knew_answer:
            self.correct += 1
        else:
            self.incorrect += 1
        self.card_index += 1
        self.show_question()

    def show_results(self):
        self.clear_screen()
        total = len(self.quiz_questions)
        attempted = self.correct + self.incorrect
        score = (self.correct / total * 100) if total else 0
        self.add_heading("Quiz Completed!")
        tk.Label(self.root, text=f"Total Questions: {total}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Total Attempted: {attempted}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Correct: {self.correct}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Incorrect: {self.incorrect}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Score: {score:.0f}%", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", command=self.show_main_menu).pack(pady=20)

    def show_add_flashcard(self):
        self.clear_screen()
        self.add_heading("Add Flashcard")
        tk.Label(self.root, text="Question:").pack(anchor="w", padx=60)
        self.question_entry = tk.Entry(self.root, width=62)
        self.question_entry.pack(padx=60, pady=(4, 14))
        tk.Label(self.root, text="Answer:").pack(anchor="w", padx=60)
        self.answer_entry = tk.Entry(self.root, width=62)
        self.answer_entry.pack(padx=60, pady=(4, 16))
        buttons = tk.Frame(self.root)
        buttons.pack(pady=6)
        tk.Button(buttons, text="Save Flashcard", command=self.add_flashcard).pack(side="left", padx=6)
        tk.Button(buttons, text="Back", command=self.show_main_menu).pack(side="left", padx=6)

    def add_flashcard(self):
        question = self.question_entry.get().strip()
        answer = self.answer_entry.get().strip()
        if not question:
            messagebox.showwarning("Missing Question", "Please enter a question.")
            return
        if not answer:
            messagebox.showwarning("Missing Answer", "Please enter an answer.")
            return
        self.cards = load_flashcards()
        if question.casefold() in (saved_question.casefold() for saved_question in self.cards):
            messagebox.showwarning("Duplicate Question", "That question already exists.")
            return
        self.cards[question] = answer
        save_flashcards(self.cards)
        messagebox.showinfo("Saved", "Flashcard added successfully!")
        self.show_main_menu()

    def view_flashcards(self):
        self.cards = load_flashcards()
        self.clear_screen()
        self.add_heading("View Flashcards")
        if not self.cards:
            tk.Label(self.root, text="No flashcards available.").pack(pady=12)
            tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=10)
            return

        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=24, pady=4)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.flashcard_list = tk.Listbox(list_frame, width=72, height=12, yscrollcommand=scrollbar.set)
        self.flashcard_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.flashcard_list.yview)
        self.visible_questions = list(self.cards.keys())
        for number, question in enumerate(self.visible_questions, start=1):
            self.flashcard_list.insert("end", f"{number}. {question} — {self.cards[question]}")
        buttons = tk.Frame(self.root)
        buttons.pack(pady=10)
        tk.Button(buttons, text="Delete Selected", command=self.delete_flashcard).pack(side="left", padx=6)
        tk.Button(buttons, text="Back", command=self.show_main_menu).pack(side="left", padx=6)

    def delete_flashcard(self):
        selection = self.flashcard_list.curselection()
        if not selection:
            messagebox.showinfo("Select Flashcard", "Select a flashcard to delete.")
            return
        question = self.visible_questions[selection[0]]
        if messagebox.askyesno("Confirm Delete", f"Delete this flashcard?\n\n{question}"):
            self.cards.pop(question, None)
            save_flashcards(self.cards)
            self.view_flashcards()


def main():
    root = tk.Tk()
    FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
