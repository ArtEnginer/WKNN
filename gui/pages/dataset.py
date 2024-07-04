import customtkinter
import os
from PIL import Image
from tksheet import Sheet
from api.db import session, Pasien, Models
# import END
from tkinter import END
from CTkMessagebox import CTkMessagebox

class Dataset(customtkinter.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.input_frame = customtkinter.CTkScrollableFrame(master=self, label_text="Input Data")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label_nama = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Nama Pasien")
        self.label_nama.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.input_nama = customtkinter.CTkEntry(master=self.input_frame)
        self.input_nama.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.label_jk = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Jenis Kelamin")
        self.label_jk.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.input_jk = customtkinter.CTkComboBox(self.input_frame, values=["Pria", "Wanita"])
        self.input_jk.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.label_usia = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Usia")
        self.label_usia.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.input_usia = customtkinter.CTkEntry(master=self.input_frame)
        self.input_usia.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.label_bb = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Berat Badan")
        self.label_bb.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.input_bb = customtkinter.CTkEntry(master=self.input_frame)
        self.input_bb.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        self.label_sistolik = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Sistolik")
        self.label_sistolik.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

        self.input_sistolik = customtkinter.CTkEntry(master=self.input_frame)
        self.input_sistolik.grid(row=9, column=0, padx=20, pady=10, sticky="ew")

        self.label_diastolik = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Diastolik")
        self.label_diastolik.grid(row=10, column=0, padx=20, pady=10, sticky="ew")

        self.input_diastolik = customtkinter.CTkEntry(master=self.input_frame)
        self.input_diastolik.grid(row=11, column=0, padx=20, pady=10, sticky="ew")

        self.label_hb = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Hemoglobin")
        self.label_hb.grid(row=12, column=0, padx=20, pady=10, sticky="ew")

        self.input_hb = customtkinter.CTkEntry(master=self.input_frame)
        self.input_hb.grid(row=13, column=0, padx=20, pady=10, sticky="ew")

        self.label_nadi = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Nadi")
        self.label_nadi.grid(row=14, column=0, padx=20, pady=10, sticky="ew")

        self.input_nadi = customtkinter.CTkEntry(master=self.input_frame)
        self.input_nadi.grid(row=15, column=0, padx=20, pady=10, sticky="ew")

        self.label_waktu = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Waktu")
        self.label_waktu.grid(row=16, column=0, padx=20, pady=10, sticky="ew")

        self.input_waktu = customtkinter.CTkEntry(master=self.input_frame)
        self.input_waktu.grid(row=17, column=0, padx=20, pady=10, sticky="ew")

        self.label_status = customtkinter.CTkLabel(master=self.input_frame, justify=customtkinter.LEFT, text="Status")
        self.label_status.grid(row=18, column=0, padx=20, pady=10, sticky="ew")

        self.input_status = customtkinter.CTkComboBox(self.input_frame, values=["Berhasil", "Batal"])
        self.input_status.grid(row=19, column=0, padx=20, pady=10, sticky="ew")

        self.button_submit = customtkinter.CTkButton(master=self.input_frame, text="Submit", command=self.button_submit_event)
        self.button_submit.grid(row=20, column=0, padx=20, pady=10, sticky="ew")

        self.button_reset = customtkinter.CTkButton(master=self.input_frame, text="Reset", command=self.button_reset_event)
        self.button_reset.grid(row=21, column=0, padx=20, pady=10, sticky="ew")

        self.sheet = Sheet(self, header=["id", "Nama", "Jenis Kelamin", "Usia", "Berat Badan", "Sistolik", "Diastolik", "Hemoglobin", "Nadi", "Waktu", "Status"], show_row_index=False)
        self.sheet.grid(row=0, column=1, padx=20, pady=50, sticky="nsew")

        self.refreshData()

    def button_submit_event(self):
        nama = self.input_nama.get()
        waktu = self.input_waktu.get()
        jk = self.input_jk.get()
        usia = self.input_usia.get()
        bb = self.input_bb.get()
        sistolik = self.input_sistolik.get()
        diastolik = self.input_diastolik.get()
        hb = self.input_hb.get()
        nadi = self.input_nadi.get()
        waktu = self.input_waktu.get()
        status = self.input_status.get() == "Berhasil"

        if (nama == "" or jk == "" or usia == "" or bb == "" or sistolik == "" or diastolik == "" or hb == "" or nadi == "" or waktu == "" or status == ""):
            msg = CTkMessagebox(title="Error", message="Data tidak boleh ada yang kosong", icon="cancel", option_1="OK")
        else:
            pasien = Pasien(nama=nama, jk=jk, usia=int(usia), bb=int(bb), sistole=int(sistolik), diastole=int(diastolik), hb=int(hb), nadi=int(nadi), waktu=int(waktu), status=status)
            session.add(pasien)
            session.commit()
            self.button_reset_event()
            self.refreshData()
    
    def button_reset_event(self):
        self.input_nama.delete(0, END)
        self.input_waktu.delete(0, END)
        self.input_usia.delete(0, END)
        self.input_bb.delete(0, END)
        self.input_sistolik.delete(0, END)
        self.input_diastolik.delete(0, END)
        self.input_hb.delete(0, END)
        self.input_nadi.delete(0, END)
        self.input_waktu.delete(0, END)

    def refreshData(self):
        q = session.query(Pasien).all()
        a = [i.toList() for i in q]
        self.sheet.set_sheet_data(a)