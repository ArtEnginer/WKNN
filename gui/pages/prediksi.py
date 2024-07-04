from customtkinter import CTkFrame
import customtkinter
import os
from PIL import Image
from CTkMessagebox import CTkMessagebox
from tkinter import END
from api.db import session, Pasien, Models
from joblib import load

class Prediksi(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent        

        self.input_frame = customtkinter.CTkScrollableFrame(master=self, label_text="Prediksi")
        self.input_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label_model = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Pilih Model")
        self.label_model.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.input_model = customtkinter.CTkComboBox(self.input_frame)
        self.input_model.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.label_jk = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Jenis Kelamin")
        self.label_jk.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.input_jk = customtkinter.CTkComboBox(self.input_frame, values=["Pria", "Wanita"])
        self.input_jk.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.label_usia = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Usia")
        self.label_usia.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        self.input_usia = customtkinter.CTkEntry(master=self.input_frame)
        self.input_usia.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        self.label_bb = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Berat Badan")
        self.label_bb.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        self.input_bb = customtkinter.CTkEntry(master=self.input_frame)
        self.input_bb.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.label_sistolik = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Sistolik")
        self.label_sistolik.grid(row=7, column=1, padx=20, pady=10, sticky="ew")

        self.input_sistolik = customtkinter.CTkEntry(master=self.input_frame)
        self.input_sistolik.grid(row=8, column=1, padx=20, pady=10, sticky="ew")

        self.label_diastolik = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Diastolik")
        self.label_diastolik.grid(row=1, column=2, padx=20, pady=10, sticky="ew")

        self.input_diastolik = customtkinter.CTkEntry(master=self.input_frame)
        self.input_diastolik.grid(row=2, column=2, padx=20, pady=10, sticky="ew")

        self.label_hb = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Hemoglobin")
        self.label_hb.grid(row=3, column=2, padx=20, pady=10, sticky="ew")

        self.input_hb = customtkinter.CTkEntry(master=self.input_frame)
        self.input_hb.grid(row=4, column=2, padx=20, pady=10, sticky="ew")

        self.label_nadi = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Nadi")
        self.label_nadi.grid(row=5, column=2, padx=20, pady=10, sticky="ew")

        self.input_nadi = customtkinter.CTkEntry(master=self.input_frame)
        self.input_nadi.grid(row=6, column=2, padx=20, pady=10, sticky="ew")

        self.label_waktu = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Waktu")
        self.label_waktu.grid(row=7, column=2, padx=20, pady=10, sticky="ew")

        self.input_waktu = customtkinter.CTkEntry(master=self.input_frame)
        self.input_waktu.grid(row=8, column=2, padx=20, pady=10, sticky="ew")

        self.button_submit = customtkinter.CTkButton(master=self.input_frame, text="Submit", command=self.button_submit_event)
        self.button_submit.grid(row=1, column=3, padx=20, pady=10, sticky="ew")

        self.button_reset = customtkinter.CTkButton(master=self.input_frame, text="Reset", command=self.button_reset_event)
        self.button_reset.grid(row=2, column=3, padx=20, pady=10, sticky="ew")

        self.refreshData()
    
    def button_submit_event(self):
        q = session.query(Models).all()
        if q.__len__() == 0:
            msg = CTkMessagebox(title="Error", message="Model Belum Tersedia", icon="cancel", option_1="OK")
            return

        modelName = self.input_model.get()
        jk = self.input_jk.get()
        usia = self.input_usia.get()
        bb = self.input_bb.get()
        sistolik = self.input_sistolik.get()
        diastolik = self.input_diastolik.get()
        hb = self.input_hb.get()
        nadi = self.input_nadi.get()
        waktu = self.input_waktu.get()


        if (jk == "" or usia == "" or bb == "" or sistolik == "" or diastolik == "" or hb == "" or nadi == "" or waktu == ""):
            msg = CTkMessagebox(title="Error", message="Input tidak boleh ada yang kosong", icon="cancel", option_1="OK")
        else:
            model = load(f"models/{modelName}.joblib")
            pred = model.predict([[jk == "Wanita", int(usia), int(bb), int(sistolik), int(diastolik), int(hb), int(nadi), int(waktu)]])
            status = "Berhasil" if pred[0] == 1 else "Batal"
            msg = CTkMessagebox(title="Error", message=status, icon="info", option_1="OK")
            self.button_reset_event()
    
    def button_reset_event(self):
        self.input_usia.delete(0, END)
        self.input_bb.delete(0, END)
        self.input_sistolik.delete(0, END)
        self.input_diastolik.delete(0, END)
        self.input_hb.delete(0, END)
        self.input_nadi.delete(0, END)
        self.input_waktu.delete(0, END)
    
    def refreshData(self):
        q = session.query(Models).all()
        if q.__len__() != 0:
            values = [i.nama for i in q]
            self.input_model.configure(values=values)
            self.input_model.set(values[0])