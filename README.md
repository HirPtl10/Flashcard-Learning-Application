# Flashcard Learning Application

## Objective

This project is a small desktop application for studying Python concepts with question-and-answer flashcards. Users can add and view cards, delete a selected card, and take a randomized quiz while tracking their score.

## Features

- Study flashcards one question at a time and reveal each answer.
- Mark each answer as known or not known and see quiz results.
- Restart the current quiz with a new random order.
- Add new cards and prevent empty or duplicate questions.
- View and delete cards with a confirmation prompt.
- Save cards between runs in `flashcards.json`.
- Create sample cards on the first run and recover from invalid JSON.

## Technologies Used

- Python
- Tkinter
- JSON

## Python Concepts Used

- **Dictionaries:** Store each question as a key and its answer as a value.
- **Lists:** Hold the shuffled questions for one quiz and the questions shown in the listbox.
- **Functions:** Separate tasks such as loading data, showing screens, and recording answers.
- **File handling:** `open()` reads and writes the JSON file.
- **Exception handling:** Specific exceptions handle a missing file, invalid JSON, and file errors.
- **Loops:** A loop clears old screen widgets and another displays saved cards.
- **Conditional statements:** Check input, duplicate questions, quiz progress, and file state.
- **Tkinter:** Provides the application window, labels, buttons, entries, listbox, and dialogs.

## How to Run

Make sure Python 3 is installed, then run this command from the project folder:

```bash
python main.py
```

Tkinter is included with most standard Python installations. On some Linux distributions it may need to be installed separately through the operating system package manager.

## Viva Preparation

1. **Why did you use a dictionary?**  
   It stores each question with its matching answer using a question-answer pair.

2. **Why did you use JSON?**  
   JSON is a simple text format that can store the dictionary and is easy to read and write in Python.

3. **What is file handling?**  
   File handling means opening, reading, writing, and closing files from a program.

4. **What does `json.load()` do?**  
   It reads JSON data from an open file and converts it into Python data.

5. **What does `json.dump()` do?**  
   It writes Python data to a file in JSON format.

6. **What is Tkinter?**  
   Tkinter is Python's standard library for building desktop graphical interfaces.

7. **What is the purpose of `mainloop()`?**  
   It keeps the window open and responds to user actions such as button clicks.

8. **Why do we use `try-except`?**  
   It lets the program handle expected errors, such as missing or invalid files, without stopping unexpectedly.

9. **How is the score calculated?**  
   Correct answers are divided by the total questions and multiplied by 100.

10. **How are flashcards stored?**  
    They are stored in a dictionary and saved in `flashcards.json` as question-answer pairs.

11. **How does randomization work?**  
    The program copies the question keys into a list and uses `random.shuffle()` to change their order.

12. **Why are functions used?**  
    Functions divide the program into named tasks, which makes it easier to read, reuse, and explain.

13. **What happens if the JSON file doesn't exist?**  
    The program creates it with a few sample flashcards.

14. **What happens if the user enters an empty question?**  
    The program displays a warning and does not save the flashcard.

15. **Explain the overall flow of your application.**  
    The program loads the flashcards, shows the main menu, and opens the selected screen. During a quiz, it reveals each answer, records the user's choice, and displays the final score. Changes are saved to the JSON file.
