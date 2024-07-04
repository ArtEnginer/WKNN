from customtkinter import CTkFrame
import customtkinter
from CTkMessagebox import CTkMessagebox
import os
from PIL import Image
from api.db import session, Pasien, Models
import pandas as pd


class Home(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.main_label = customtkinter.CTkLabel(
            self, text="Klasifikasi calon pendonor darah menggunakan algoritma Weighted K Nearet Neighbour", wraplength=500, font=("Roboto", 20))
        self.main_label.pack(side="top", pady=200, padx=20)

        self.button_reset = customtkinter.CTkButton(
            self, text="Reset", command=self.button_reset_event)
        self.button_reset.pack(side="bottom", padx=20, pady=10, anchor="e")

    def button_reset_event(self):
        msg = CTkMessagebox(title="Reset?", message="Apakah anda yakin ingin mereset data?",
                            icon="question", option_1="Batal", option_2="Ya")
        response = msg.get()

        if response == "Ya":
            allData = session.query(Pasien).all()
            for data in allData:
                session.delete(data)
                session.commit()
            pasien = pd.read_csv("dataset/pasien.csv")
            for index, row in pasien.iterrows():
                session.add(
                    Pasien(nama=row["nama"], jk=row["jk"], usia=row["usia"], bb=row["bb"], sistole=row["sistole"], diastole=row["diastole"], hb=row["hb"], nadi=row["nadi"], waktu=row["waktu"], status=row["status"]))
                session.commit()
        else:
            print("None")
