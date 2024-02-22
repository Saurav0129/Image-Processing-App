import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog, colorchooser, Menu
import cv2
from PIL import Image, ImageTk
import os

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.configure(background='white')

    
        self.menu_bar = Menu(root)
        self.root.config(menu=self.menu_bar)

        
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="About", command=self.show_about)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="Menu", menu=self.file_menu)

        
        self.header_label = tk.Label(root, text="Image Processing App", font=("Arial", 18, "bold"), background='white')
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10)

        
        self.image_frame = tk.Frame(root, bg="white")
        self.image_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        
        self.image_label = tk.Label(self.image_frame, bg="white")
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        
        self.image_properties_label = ttk.Label(self.image_frame, text="", background='white')
        self.image_properties_label.grid(row=1, column=0, padx=10, pady=10)

        
        self.function_frame = tk.Frame(root, bg="white")
        self.function_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        
        self.load_button = ttk.Button(self.function_frame, text="Load Image", command=self.open_image)
        self.load_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")

        
        self.convert_options = ttk.Combobox(self.function_frame, values=["RGB", "Grayscale", "Binary"])
        self.convert_options.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        self.convert_options.current(0)

        self.convert_button = ttk.Button(self.function_frame, text="Convert", command=self.convert_image)
        self.convert_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        
        self.brightness_label = ttk.Label(self.function_frame, text="Brightness:")
        self.brightness_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.brightness_slider = ttk.Scale(self.function_frame, from_=-255, to=255, orient=tk.HORIZONTAL, length=200, command=self.adjust_brightness)
        self.brightness_slider.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

        
        self.contrast_label = ttk.Label(self.function_frame, text="Contrast:")
        self.contrast_label.grid(row=5, column=0, pady=5, padx=10, sticky="w")
        self.contrast_slider = ttk.Scale(self.function_frame, from_=0.0, to=3.0, orient=tk.HORIZONTAL, length=200, command=self.adjust_contrast)
        self.contrast_slider.grid(row=6, column=0, pady=5, padx=10, sticky="ew")

        
        self.annotation_options = ttk.Combobox(self.function_frame, values=["None", "Line", "Circle", "Rectangle", "Text"])
        self.annotation_options.grid(row=7, column=0, pady=5, padx=10, sticky="ew")
        self.annotation_options.current(0)

        self.annotation_button = ttk.Button(self.function_frame, text="Add Annotation", command=self.add_annotation)
        self.annotation_button.grid(row=8, column=0, pady=5, padx=10, sticky="ew")

        
        self.save_button = ttk.Button(self.function_frame, text="Save", command=self.save_image)
        self.save_button.grid(row=9, column=0, pady=5, padx=10, sticky="ew")

        self.image = None
        self.original_image = None

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                self.image = self.original_image.copy()
                self.show_image(self.image)
                self.show_image_properties(file_path)
            else:
                messagebox.showerror("Error", "Failed to load the image.")

    def show_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image.resize((300, 300)))
        self.image_label.configure(image=image)
        self.image_label.image = image

    def show_image_properties(self, file_path):
        height, width, channels = self.original_image.shape
        properties_text = f"Image Properties:\nSize: {os.path.getsize(file_path)} bytes\nDimensions: {height}x{width}\nChannels: {channels}"
        self.image_properties_label.configure(text=properties_text)

    def convert_image(self):
        if self.original_image is not None:
            convert_type = self.convert_options.get()
            if convert_type == "Grayscale":
                self.processed_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            elif convert_type == "Binary":
                threshold_value = simpledialog.askfloat("Binary Threshold", "Enter threshold value:")
                if threshold_value is not None:
                    _, self.processed_image = cv2.threshold(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY),
                                                           threshold_value, 255, cv2.THRESH_BINARY)
            else:
                self.processed_image = self.original_image.copy()

            if self.processed_image is not None:
                self.show_image(self.processed_image)

    def adjust_brightness(self, value):
        if self.original_image is not None:
            self.processed_image = cv2.convertScaleAbs(self.original_image, beta=float(value))
            self.show_image(self.processed_image)

    def adjust_contrast(self, value):
        if self.original_image is not None:
            self.processed_image = cv2.convertScaleAbs(self.original_image, alpha=float(value))
            self.show_image(self.processed_image)

    def add_annotation(self):
        if self.original_image is not None:
            annotation_type = self.annotation_options.get()
            if annotation_type == "Line":
                self.add_line_annotation()
            elif annotation_type == "Circle":
                self.add_circle_annotation()
            elif annotation_type == "Rectangle":
                self.add_rectangle_annotation()
            elif annotation_type == "Text":
                self.add_text_annotation()

    def add_line_annotation(self):
        if self.original_image is not None:
            position = simpledialog.askstring("Line Annotation", "Enter starting and ending points (x1,y1,x2,y2):")
            color = colorchooser.askcolor(title="Choose Line Color")
            thickness = simpledialog.askinteger("Line Annotation", "Enter line thickness:")
            if position and color and thickness is not None:
                points = position.split(',')
                start_point = (int(points[0]), int(points[1]))
                end_point = (int(points[2]), int(points[3]))
                # Swap red and blue channels
                color = (color[0][2], color[0][1], color[0][0])
                cv2.line(self.original_image, start_point, end_point, color, thickness)
                self.show_image(self.original_image)

    def add_circle_annotation(self):
        if self.original_image is not None:
            center = simpledialog.askstring("Circle Annotation", "Enter center point and radius (x,y,r):")
            color = colorchooser.askcolor(title="Choose Circle Color")
            thickness = simpledialog.askinteger("Circle Annotation", "Enter line thickness:")
            if center and color and thickness is not None:
                points = center.split(',')
                center_point = (int(points[0]), int(points[1]))
                radius = int(points[2])
                # Swap red and blue channels
                color = (color[0][2], color[0][1], color[0][0])
                cv2.circle(self.original_image, center_point, radius, color, thickness)
                self.show_image(self.original_image)

    def add_rectangle_annotation(self):
        if self.original_image is not None:
            points = simpledialog.askstring("Rectangle Annotation", "Enter top-left and bottom-right points (x1,y1,x2,y2):")
            color = colorchooser.askcolor(title="Choose Rectangle Color")
            thickness = simpledialog.askinteger("Rectangle Annotation", "Enter line thickness:")
            if points and color and thickness is not None:
                points = points.split(',')
                top_left = (int(points[0]), int(points[1]))
                bottom_right = (int(points[2]), int(points[3]))
                # Swap red and blue channels
                color = (color[0][2], color[0][1], color[0][0])
                cv2.rectangle(self.original_image, top_left, bottom_right, color, thickness)
                self.show_image(self.original_image)

    def add_text_annotation(self):
        if self.original_image is not None:
            text = simpledialog.askstring("Text Annotation", "Enter text:")
            position = simpledialog.askstring("Text Annotation", "Enter position (x,y):")
            color = colorchooser.askcolor(title="Choose Text Color")
            font_scale = simpledialog.askfloat("Text Annotation", "Enter font scale:")
            thickness = simpledialog.askinteger("Text Annotation", "Enter thickness:")
            if text and position and color and font_scale is not None and thickness is not None:
                position = position.split(',')
                org = (int(position[0]), int(position[1]))
                # Swap red and blue channels
                color = (color[0][2], color[0][1], color[0][0])
                cv2.putText(self.original_image, text, org, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
                self.show_image(self.original_image)

    def save_image(self):
        if self.original_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                cv2.imwrite(file_path, self.original_image)
                messagebox.showinfo("Success", "Image saved successfully.")

    def undo(self):
        if self.original_image is not None:
            self.show_image(self.original_image)

    def show_about(self):
        messagebox.showinfo("About", "This is the Image Processing App.\nDeveloped by Saurav Bisht.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

