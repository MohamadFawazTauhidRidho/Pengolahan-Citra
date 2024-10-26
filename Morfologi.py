import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Inisialisasi root window Tkinter
root = Tk()
root.title("Operasi Morfologi - Dilasi & Erosi")
root.geometry("800x600")

# Variabel global
img = None
processed_img = None

# Fungsi untuk membuka gambar
def open_image():
    global img
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not filepath:
        return
    
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # Mengubah menjadi biner
    display_image(img, original=True)

# Fungsi untuk menampilkan gambar pada GUI
def display_image(image, original=False):
    # Konversi gambar untuk ditampilkan
    image = Image.fromarray(image)
    image = image.resize((400, 400))
    photo = ImageTk.PhotoImage(image=image)
    
    # Tampilkan gambar asli atau hasil
    if original:
        panel1.config(image=photo)
        panel1.image = photo
    else:
        panel2.config(image=photo)
        panel2.image = photo

# Fungsi untuk menyimpan gambar
def save_image():
    global processed_img
    if processed_img is None:
        messagebox.showerror("Error", "Tidak ada gambar untuk disimpan!")
        return
    
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if filepath:
        cv2.imwrite(filepath, processed_img)
        messagebox.showinfo("Sukses", "Gambar berhasil disimpan!")

# Fungsi untuk melakukan dilasi
def apply_dilation():
    global img, processed_img
    if img is None:
        messagebox.showerror("Error", "Buka gambar terlebih dahulu!")
        return
    
    kernel = np.ones((5, 5), np.uint8)
    processed_img = cv2.dilate(img, kernel, iterations=1)
    display_image(processed_img)

# Fungsi untuk melakukan erosi
def apply_erosion():
    global img, processed_img
    if img is None:
        messagebox.showerror("Error", "Buka gambar terlebih dahulu!")
        return
    
    kernel = np.ones((5, 5), np.uint8)
    processed_img = cv2.erode(img, kernel, iterations=1)
    display_image(processed_img)

# GUI Layout
panel1 = Label(root)
panel1.pack(side="left", padx=10, pady=10)
panel2 = Label(root)
panel2.pack(side="right", padx=10, pady=10)

button_frame = Frame(root)
button_frame.pack(side="bottom", pady=20)

# Tombol untuk membuka, menyimpan, dan operasi morfologi
open_button = Button(button_frame, text="Buka Gambar", command=open_image)
open_button.grid(row=0, column=0, padx=10, pady=10)

dilate_button = Button(button_frame, text="Dilasi", command=apply_dilation)
dilate_button.grid(row=0, column=1, padx=10, pady=10)

erode_button = Button(button_frame, text="Erosi", command=apply_erosion)
erode_button.grid(row=0, column=2, padx=10, pady=10)

save_button = Button(button_frame, text="Simpan Gambar", command=save_image)
save_button.grid(row=0, column=3, padx=10, pady=10)

root.mainloop()
