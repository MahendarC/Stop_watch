import tkinter as tk
from PIL import Image, ImageTk
import time

class Stopwatch:
    def __init__(self, root, background_image_path):
        self.root = root
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.bg_path = background_image_path

        # Create canvas for background
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        # Bind resize event to update background
        self.root.bind("<Configure>", self.resize_bg)

        # Background placeholder
        self.bg_image = None
        self.bg_id = None

        # Stopwatch text
        self.timer_text = self.canvas.create_text(
            root.winfo_screenwidth()//2,
            root.winfo_screenheight()//2 - 50,
            text="00:00:00",
            font=("Arial", 70, "bold"),
            fill="lime"
        )

        # Button styles (solid colors for "transparent look")
        btn_style = {
            "font": ("Arial", 16, "bold"),
            "fg": "white",
            "bg": "#222222",
            "activebackground": "#444444",
            "activeforeground": "white",
            "bd": 0,
            "highlightthickness": 0,
            "width": 10
        }

        # Create buttons
        self.start_button = tk.Button(root, text="▶ Start", command=self.start, **btn_style)
        self.stop_button = tk.Button(root, text="⏸ Stop", command=self.stop, **btn_style)
        self.reset_button = tk.Button(root, text="⟳ Reset", command=self.reset, **btn_style)

        # Place buttons centered under the timer
        self.button_frame = tk.Frame(root, bg="")
        self.canvas.create_window(
            root.winfo_screenwidth()//2,
            root.winfo_screenheight()//2 + 80,
            window=self.button_frame
        )
        self.start_button.pack(side="left", padx=10)
        self.stop_button.pack(side="left", padx=10)
        self.reset_button.pack(side="left", padx=10)

    def resize_bg(self, event=None):
        """Resize background image to fit window"""
        img = Image.open(self.bg_path)
        img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img)

        if self.bg_id:
            self.canvas.itemconfig(self.bg_id, image=self.bg_image)
        else:
            self.bg_id = self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            self.canvas.lower(self.bg_id)  # background behind other widgets

    def update_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(self.elapsed_time), 60)
            hours, minutes = divmod(minutes, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            self.canvas.itemconfig(self.timer_text, text=time_str)
            self.root.after(1000, self.update_time)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_time()

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.canvas.itemconfig(self.timer_text, text="00:00:00")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Stopwatch with Fullscreen Background")
    root.state("zoomed")  # fullscreen on Windows

    background_image_path = "d:/Auto_Message/istockphoto-1946362695-612x612.jpg"
    sw = Stopwatch(root, background_image_path)
    root.mainloop()
