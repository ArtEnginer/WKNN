import customtkinter
import os
from PIL import Image
from tksheet import Sheet
from api.db import session, Pasien, Models
# import END
from tkinter import END
from CTkMessagebox import CTkMessagebox
from KNearestNeighbor_weighted import KNearestNeighbors
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump


class Learning(customtkinter.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.input_frame = customtkinter.CTkScrollableFrame(
            master=self, label_text="Learning")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label_testsize = customtkinter.CTkLabel(
            master=self.input_frame, justify=customtkinter.LEFT, text="Ukuran Data Testing (%)")
        self.label_testsize.grid(
            row=0, column=0, padx=20, pady=10, sticky="ew")

        # only allow number
        self.input_testsize = customtkinter.CTkEntry(master=self.input_frame)
        self.input_testsize.grid(
            row=1, column=0, padx=20, pady=10, sticky="ew")

        self.label_model = customtkinter.CTkLabel(
            master=self.input_frame, justify=customtkinter.LEFT, text="Jenis Model")
        self.label_model.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.input_model = customtkinter.CTkComboBox(
            self.input_frame, values=["KNN", "Weighted KNN"])
        self.input_model.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.label_k = customtkinter.CTkLabel(
            master=self.input_frame, justify=customtkinter.LEFT, text="Nilai K")
        self.label_k.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.input_k = customtkinter.CTkEntry(master=self.input_frame)
        self.input_k.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.label_preprocessing = customtkinter.CTkLabel(
            master=self.input_frame, justify=customtkinter.LEFT, text="Preprocessing")
        self.label_preprocessing.grid(
            row=6, column=0, padx=20, pady=10, sticky="ew")

        self.input_preprocessing = customtkinter.CTkComboBox(
            self.input_frame, values=["Tanpa Preprocessing", "StandardScaler"])
        self.input_preprocessing.grid(
            row=7, column=0, padx=20, pady=10, sticky="ew")

        self.label_nama = customtkinter.CTkLabel(
            master=self.input_frame, justify=customtkinter.LEFT, text="Nama Model")
        self.label_nama.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

        self.input_nama = customtkinter.CTkEntry(master=self.input_frame)
        self.input_nama.grid(row=9, column=0, padx=20, pady=10, sticky="ew")

        self.button_submit = customtkinter.CTkButton(
            master=self.input_frame, text="Submit", command=self.button_submit_event)
        self.button_submit.grid(
            row=10, column=0, padx=20, pady=10, sticky="ew")

        self.button_reset = customtkinter.CTkButton(
            master=self.input_frame, text="Reset", command=self.button_reset_event)
        self.button_reset.grid(row=11, column=0, padx=20, pady=10, sticky="ew")

        self.sheet = Sheet(self, header=["id", "Nama Model", "Ukuran Data Testing (%)",
                           "Weighted", "Nilai K", "Preprocessing", "Akurasi"], show_row_index=False)
        self.sheet.grid(row=0, column=1, padx=20, pady=50, sticky="nsew")

        self.refreshData()

    def button_submit_event(self):
        nama = self.input_nama.get()
        testsize = self.input_testsize.get()
        mode = self.input_model.get()
        k = self.input_k.get()
        preprocessing = self.input_preprocessing.get()

        if (nama == "" or testsize == "" or mode == "" or k == "" or preprocessing == ""):
            msg = CTkMessagebox(
                title="Error", message="Input tidak boleh ada yang kosong", icon="cancel", option_1="OK")
        else:
            if not testsize.isnumeric() or not k.isnumeric():
                msg = CTkMessagebox(
                    title="Error", message="Ukuran data testing dan Nilai K harus berupa angka", icon="cancel", option_1="OK")
                return

            model = Models(nama=nama, testsize=float(
                testsize) / 100, weighted=(mode == "Weighted KNN"), k=int(k), preprocessing=preprocessing)

            q = session.query(Pasien).all()
            # q to pandas
            df = pd.DataFrame([i.toList() for i in q], columns=[
                "id", "Nama Pasien", "Jenis Kelamin", "Usia", "Berat Badan", "Sistolik", "Diastolik", "Hemoglobin", "Nadi", "Waktu", "Status"])
            X = df.iloc[:, 2:10].values
            y = df.iloc[:, -1].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=model.testsize, shuffle=False)

            lb = LabelBinarizer()
            # binarizer first column in X_Train
            lb.fit(X_train[:, 0])
            X_train[:, 0] = lb.transform(X_train[:, 0]).flatten()
            X_test[:, 0] = lb.transform(X_test[:, 0]).flatten()

            if model.preprocessing == "StandardScaler":
                scaler = StandardScaler()
                X_train = scaler.fit_transform(X_train)
                X_test = scaler.fit_transform(X_test)

            knn = KNearestNeighbors(k=model.k, weighted=model.weighted)
            knn.fit(X_train=X_train, y_train=y_train)
            y_pred = knn.predict(X_test)

            model.accuracy = accuracy_score(y_test, y_pred)

            session.add(model)
            session.commit()

            dump(knn, "models/"+model.nama+".joblib")

            self.button_reset_event()
            self.refreshData()

    def button_reset_event(self):
        self.input_nama.delete(0, END)
        self.input_testsize.delete(0, END)
        self.input_k.delete(0, END)

    def refreshData(self):
        q = session.query(Models).all()
        a = [i.toList() for i in q]
        self.sheet.set_sheet_data(a)
