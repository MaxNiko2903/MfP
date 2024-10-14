import tkinter as tk
from tkinter import messagebox
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Физический научный калькулятор")
        self.geometry("330x655")
        self.configure(bg="lightgray")
        
        self.memory = [None, None, None]  # Память для сохранения результатов

        self.equation = tk.StringVar()
        self.result_display = tk.Entry(self, textvariable=self.equation, font=("Arial", 18), bd=10, insertwidth=4, width=14, borderwidth=4)
        self.result_display.grid(row=0, column=0, columnspan=4)

        self.create_buttons()

    def create_buttons(self):
        button_list = [
            '7', '8', '9', '/', 
            '4', '5', '6', '*',
            '1', '2', '3', '-', 
            '0', '.', '=', '+', 
            'sin', 'cos', 'tan', '√', 
            'log', 'ln', 'exp', '^', 
            'M1', 'M2', 'M3', 'C', 
            '(', ')', 'del', 'M+'
        ]

        row_val = 1
        col_val = 0
        for button_text in button_list:
            button = tk.Button(self, text=button_text, padx=20, pady=20, font=("Arial", 14), bg="white", command=lambda text=button_text: self.on_button_click(text))
            button.grid(row=row_val, column=col_val)
            col_val += 1
            if col_val == 4:
                row_val += 1
                col_val = 0

    def on_button_click(self, text):
        if text == '=':
            self.calculate()
        elif text == 'C':
            self.equation.set("")
        elif text == 'del':
            current_text = self.equation.get()
            self.equation.set(current_text[:-1])
        elif text == 'M1' or text == 'M2' or text == 'M3':
            self.use_memory(text)
        elif text == 'M+':
            self.save_to_memory()
        else:
            self.equation.set(self.equation.get() + text)

    def calculate(self):
        try:
            expression = self.equation.get()
            expression = expression.replace('√', 'math.sqrt').replace('^', '**')
            expression = expression.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
            expression = expression.replace('log', 'math.log10').replace('ln', 'math.log').replace('exp', 'math.exp')
            result = eval(expression)
            self.equation.set(result)
        except Exception as e:
            messagebox.showerror("Ошибка", "Неверное выражение")

    def save_to_memory(self):
        result = self.equation.get()
        if self.memory[0] is None:
            self.memory[0] = result
            messagebox.showinfo("Память", "Результат сохранен в M1")
        elif self.memory[1] is None:
            self.memory[1] = result
            messagebox.showinfo("Память", "Результат сохранен в M2")
        elif self.memory[2] is None:
            self.memory[2] = result
            messagebox.showinfo("Память", "Результат сохранен в M3")
        else:
            messagebox.showwarning("Память", "Память заполнена")

    def use_memory(self, button):
        memory_index = int(button[-1]) - 1
        if self.memory[memory_index] is not None:
            self.equation.set(self.equation.get() + self.memory[memory_index])
        else:
            messagebox.showwarning("Память", f"Память M{memory_index+1} пуста")

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
