from PIL import Image
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Function to hide text inside image
def hide_text(input_path, text, output_path):
    image = Image.open(input_path)
    binary_text = ''.join(format(ord(char), '08b') for char in text) + '00000000'
    pixels = list(image.getdata())
    new_pixels = []
    text_index = 0
    for pixel in pixels:
        r, g, b = pixel[:3]
        if text_index < len(binary_text):
            r = (r & 0xFE) | int(binary_text[text_index])
            text_index += 1
        if text_index < len(binary_text):
            g = (g & 0xFE) | int(binary_text[text_index])
            text_index += 1
        if text_index < len(binary_text):
            b = (b & 0xFE) | int(binary_text[text_index])
            text_index += 1
        new_pixels.append((r, g, b) + pixel[3:] if len(pixel) == 4 else (r, g, b))
    image.putdata(new_pixels)
    image.save(output_path)
    messagebox.showinfo("Success", "Text successfully hidden in image!")

# Function to extract text from image
def extract_text(input_path):
    image = Image.open(input_path)
    pixels = list(image.getdata())
    binary_text = ''
    for pixel in pixels:
        r, g, b = pixel[:3]
        binary_text += str(r & 1)
        binary_text += str(g & 1)
        binary_text += str(b & 1)
    chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    decoded_text = ''
    for char in chars:
        if char == '00000000':
            break
        decoded_text += chr(int(char, 2))
    messagebox.showinfo("Hidden Text", f"Extracted Text:\n{decoded_text}")

# GUI Setup
def select_encrypt():
    input_path = filedialog.askopenfilename(title="Select Image to Hide Text")
    if not input_path:
        return
    text = simpledialog.askstring("Input", "Enter text to hide:")
    if text is None:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Encrypted Image As")
    if not output_path:
        return
    hide_text(input_path, text, output_path)

def select_decrypt():
    input_path = filedialog.askopenfilename(title="Select Image to Extract Text From")
    if not input_path:
        return
    extract_text(input_path)

root = tk.Tk()
root.title("Image Text Steganography")
root.geometry("400x200")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Select a task:", font=("Arial", 14))
label.pack(pady=10)

encrypt_btn = tk.Button(frame, text="Encrypt (Hide Text)", command=select_encrypt, width=20, height=2)
encrypt_btn.pack(pady=5)

decrypt_btn = tk.Button(frame, text="Decrypt (Extract Text)", command=select_decrypt, width=20, height=2)
decrypt_btn.pack(pady=5)

root.mainloop()