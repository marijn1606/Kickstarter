import tkinter as tk
import printer
import detect
import time
from PIL import ImageTk, Image

printer1 = printer.Printer("/dev/ttyUSB0", 115200, 55, 50)

demoPadRange = [[2, 0, 0], [55, 255, 255]]
demoPCBRange = [[135, 100, 78], [160, 255, 255]]
pixelsPerMilimeter = 27.3315496994
offset = (69.9, 11.2, 0)

detector = detect.Detector(demoPadRange, demoPCBRange, pixelsPerMilimeter, offset)
detections = []

def start():
    global detections
    print("starting......")
    for widget in window.winfo_children():
        widget.destroy()
    label = tk.Label(window, text="Making an image...")
    label.config(font=("Courier", 44))
    label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    window.update()
    printer1.make_photo()
    time.sleep(1)
    detections = detector.detect("test.jpg", (75, 150, 100), (3280, 2464))
    showImage()

def confirm():
    for widget in window.winfo_children():
        widget.destroy()
    label = tk.Label(window, text="Placing solderpaste...")
    label.config(font=("Courier", 44))
    label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    window.update()
    # time.sleep(5)
    printer1.dispense_at_points(detections)
    for widget in window.winfo_children():
        widget.destroy()
    label = tk.Label(window, text="Done!")
    label.config(font=("Courier", 44))
    label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    restartButton = tk.Button(window, text="Restart", height=5, width=20, command=home)
    restartButton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
    window.update()

def reject():
    print("Rejected boys")

window = tk.Tk()
window.attributes("-fullscreen", True)

def home():
    for widget in window.winfo_children():
        widget.destroy()
    greeting = tk.Label(text="The PasteMaster", )
    greeting.config(font=("Courier", 60))
    startButton = tk.Button(window, text="Start", height=5, width=20, command=start)
    greeting.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    startButton.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    window.mainloop()

def showImage():
    image = Image.open("detected.jpg")
    image = image.resize((820, 616))
    tkImage = ImageTk.PhotoImage(image)
    label = tk.Label(window, image = tkImage)
    label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    label.config(image=tkImage)
    confirmButton = tk.Button(window, text="Confirm", height=5, width=20, command=confirm)
    rejectButton = tk.Button(window, text="Reject", height=5, width=20, command=reject)
    confirmButton.place(relx=0.4, rely=0.85, anchor=tk.CENTER)
    rejectButton.place(relx=0.6, rely=0.85, anchor=tk.CENTER)
    window.mainloop()

home()