import tkinter as tk
from tkinter import messagebox

# Caesar Cipher using modular arithmetic (group structure of integers modulo 26)
def caesar_cipher(text, key, encrypt=True):
    # Z_26 - the group of integers modulo 26, used for shifting characters in the Caesar cipher
    group_order = 26
    
    result = []
    
    for char in text:
        if 'A' <= char <= 'Z':  # English upper-case letters (group structure: Z_26)
            shift = 65  # ASCII for 'A'
        elif 'a' <= char <= 'z':  # English lower-case letters (group structure: Z_26)
            shift = 97  # ASCII for 'a'
        elif 'А' <= char <= 'Я':  # Russian upper-case letters (group structure: Z_32)
            shift = 1040  # ASCII for 'А'
            group_order = 32  # Russian letters form a cyclic group Z_32
        elif 'а' <= char <= 'я':  # Russian lower-case letters (group structure: Z_32)
            shift = 1072  # ASCII for 'а'
            group_order = 32  # Z_32 for Russian
        else:
            result.append(char)  # Non-alphabet characters remain unchanged
            continue
        
        # Encryption: shift forward by key; Decryption: shift backward (inverse operation in group)
        operation_key = key if encrypt else -key
        
        # Perform the modular addition (group operation in Z_n)
        new_char = chr((ord(char) - shift + operation_key) % group_order + shift)
        result.append(new_char)

    return ''.join(result)

# Function to process user input for encryption or decryption
def process_text():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get()

    # Ensure key is numeric for Caesar cipher
    if not key.isdigit():
        messagebox.showerror("Ошибка", "Для шифра Цезаря введите числовой ключ.")
        return

    key = int(key)
    
    # Determine operation (encrypt or decrypt) and perform Caesar cipher
    if operation.get() == "Encrypt":
        result = caesar_cipher(text, key, encrypt=True)
    else:
        result = caesar_cipher(text, key, encrypt=False)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# Copy-paste functionality for convenience
def copy_text(event=None):
    window.clipboard_clear()
    window.clipboard_append(output_text.get("1.0", tk.END).strip())

def paste_text(event=None):
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, window.clipboard_get())

# Setting up the GUI
window = tk.Tk()
window.title("Caesar Cipher with Algebraic Structures")

# Input text label and box
tk.Label(window, text="Введите текст:").pack()
input_text = tk.Text(window, height=5, width=40)
input_text.pack()

# Key entry label and input box
tk.Label(window, text="Введите ключ (число):").pack()
key_entry = tk.Entry(window)
key_entry.pack()

# Operation selection (Encrypt or Decrypt)
operation = tk.StringVar()
operation.set("Encrypt")
tk.Radiobutton(window, text="Шифровать", variable=operation, value="Encrypt").pack()
tk.Radiobutton(window, text="Дешифровать", variable=operation, value="Decrypt").pack()

# Process button
tk.Button(window, text="Обработать", command=process_text).pack()

# Output text label and box
tk.Label(window, text="Результат:").pack()
output_text = tk.Text(window, height=5, width=40)
output_text.pack()

# Bind copy and paste functions to Ctrl+C and Ctrl+V
window.bind('<Control-c>', copy_text)
window.bind('<Control-v>', paste_text)

# Main event loop to run the application
window.mainloop()
