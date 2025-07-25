import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

def crop_pdf(input_pdf_path, output_pdf_path, crop_box):
    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()

    for page in doc:
        rect = fitz.Rect(*crop_box)
        page.set_cropbox(rect)
        new_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)

    new_doc.save(output_pdf_path)
    doc.close()
    new_doc.close()

def browse_pdf():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_path_var.set(filepath)

def get_crop_box(platform):
    if platform == "Flipkart":
        return (50, 50, 400, 600)
    elif platform == "Meesho":
        return (30, 80, 370, 570)
    elif platform == "Amazon":
        return (20, 60, 380, 580)
    else:
        return (50, 50, 400, 600)

def run_crop():
    input_path = input_path_var.get()
    selected_platform = platform_var.get()

    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return

    crop_box = get_crop_box(selected_platform)
    output_path = os.path.splitext(input_path)[0] + f"_{selected_platform.lower()}_cropped.pdf"

    try:
        crop_pdf(input_path, output_path, crop_box)
        messagebox.showinfo("Success", f"Cropped PDF saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Code
root = tk.Tk()
root.title("Shipping Label Cropper Tool")
root.geometry("550x250")

input_path_var = tk.StringVar()
platform_var = tk.StringVar(value="Flipkart")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill="both")

tk.Label(frame, text="Select PDF File:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=input_path_var, width=50).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="Browse", command=browse_pdf).grid(row=1, column=1, padx=5)

tk.Label(frame, text="Select Platform:").grid(row=2, column=0, sticky="w", pady=(10, 0))
platform_dropdown = ttk.Combobox(frame, textvariable=platform_var, values=["Flipkart", "Meesho", "Amazon"], state="readonly")
platform_dropdown.grid(row=3, column=0, padx=5, pady=5)

tk.Button(frame, text="Crop Now", command=run_crop, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
