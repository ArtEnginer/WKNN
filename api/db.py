from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, Float, Text, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import json
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "id_ID")

engine = create_engine("sqlite+pysqlite:///dataset/database.db", echo=True)
engine.connect()

# Apply the mixin to your Models
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Pasien(Base, SerializerMixin):
    __tablename__ = "pasien"
    id = Column(Integer, primary_key=True)
    nama = Column(Text, nullable=False)
    jk = Column(Text, nullable=False)
    usia = Column(Integer, nullable=False)
    bb = Column(Integer, nullable=False)
    sistole = Column(Integer, nullable=False)
    diastole = Column(Integer, nullable=False)
    hb = Column(Integer, nullable=False)
    nadi = Column(Integer, nullable=False)
    waktu = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "jk": self.jk,
            "usia": self.usia,
            "bb": self.bb,
            "sistole": self.sistole,
            "diastole": self.diastole,
            "hb": self.hb,
            "nadi": self.nadi,
            "Waktu": self.waktu,
            "status": self.status
        }
    
    def toList(self):
        return [
            self.id,
            self.nama,
            self.jk,
            self.usia,
            self.bb,
            self.sistole,
            self.diastole,
            self.hb,
            self.nadi,
            self.waktu,
            self.status
        ]


class Models(Base, SerializerMixin):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    nama = Column(Text, nullable=False)
    testsize = Column(Float, nullable=False)
    weighted = Column(Boolean, nullable=False)
    k = Column(Integer, nullable=False)
    preprocessing = Column(Text, nullable=False)
    accuracy = Column(Float, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "testsize": self.testsize,
            "weighted": self.weighted,
            "k": self.k,
            "preprocessing": self.preprocessing,
            "accuracy": self.accuracy
        }
    
    def toList(self):
        return [
            self.id,
            self.nama,
            self.testsize,
            self.weighted,
            self.k,
            self.preprocessing,
            self.accuracy
        ]

Base.metadata.create_all(engine)