import customtkinter
import os
from PIL import Image
from gui.pages import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    width = 960
    height = 550
    
    def __init__(self):
        super().__init__()

        self.title("WKNN")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets/images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.dataset_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dataset_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "dataset_light.png")), size=(20, 20))
        self.learn_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "learn_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "learn_light.png")), size=(20, 20))
        self.predict_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "predict_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "predict_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  W-KNN", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.dataset_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dataset",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.dataset_image, anchor="w", command=self.dataset_button_event)
        self.dataset_button.grid(row=2, column=0, sticky="ew")

        self.learning_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Learning",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.learn_image, anchor="w", command=self.learning_button_event)
        self.learning_button.grid(row=3, column=0, sticky="ew")

        self.prediksi_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Prediksi",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.predict_image, anchor="w", command=self.prediksi_button_event)
        self.prediksi_button.grid(row=4, column=0, sticky="ew")

        self.home_frame = Home(self, corner_radius=0, fg_color="transparent")
        self.dataset_frame = Dataset(self, corner_radius=0, fg_color="transparent")
        self.learning_frame = Learning(self, corner_radius=0, fg_color="transparent")
        self.prediksi_frame = Prediksi(self, corner_radius=0, fg_color="transparent")

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.dataset_button.configure(fg_color=("gray75", "gray25") if name == "dataset" else "transparent")
        self.learning_button.configure(fg_color=("gray75", "gray25") if name == "learning" else "transparent")
        self.prediksi_button.configure(fg_color=("gray75", "gray25") if name == "prediksi" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "dataset":
            self.dataset_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dataset_frame.grid_forget()
        if name == "learning":
            self.learning_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.learning_frame.grid_forget()
        if name == "prediksi":
            self.prediksi_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.prediksi_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def dataset_button_event(self):
        self.select_frame_by_name("dataset")
        self.dataset_frame.refreshData()

    def learning_button_event(self):
        self.select_frame_by_name("learning")
        self.learning_frame.refreshData()

    def prediksi_button_event(self):
        self.select_frame_by_name("prediksi")