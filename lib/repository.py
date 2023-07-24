import copy
import csv
import datetime
from pathlib import Path

import settings


class Student:
    def __init__(self, data: dict[str, str]):
        self.data = data

    @property
    def cial(self):
        return self.data.get('CIAL', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def exp(self):
        return self.data.get('Expediente', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def id(self):
        return self.data.get('NIF - NIE', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def name(self):
        return self.data.get('Nombre', '')

    @property
    def surname1(self):
        return self.data.get('Primer apellido', '')

    @property
    def surname2(self):
        return self.data.get('Segundo apellido', '')

    @property
    def surname(self):
        if self.surname2:
            return f'{self.surname1} {self.surname2}'
        return self.surname1

    @property
    def fullname(self):
        return f'{self.name} {self.surname}'

    @property
    def date_of_birth(self):
        return self.data.get('Fecha de nacimiento', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def calculated_age(self):
        a = datetime.datetime.strptime(self.date_of_birth, '%d/%m/%Y')
        b = datetime.datetime.now()
        return int((b - a).days / 365)

    @property
    def age(self) -> int | str:
        if dage := self.data.get('Edad'):
            return int(dage)
        return settings.EMPTY_FIELD_PLACEHOLDER

    def is_adult(self):
        return self.age >= 18

    @property
    def study(self):
        return self.data.get('Estudio den. corta', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def group(self):
        return self.data.get('Grupo Clase', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def shift(self):
        return self.data.get('Turnos', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def cshift(self):
        return self.shift[0].upper()

    @property
    def list_number(self):
        return self.data.get('Nº Lista', settings.EMPTY_FIELD_PLACEHOLDER)

    @property
    def pic(self):
        return settings.PROFILE_PICS_PATH / (self.exp + '.jpg')


class StudentRepository:
    def __init__(self, data_path: Path = settings.STUDENTS_DATA_PATH):
        with open(data_path, encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            self.data = [Student(row) for row in reader]
            self.filtered_data = copy.deepcopy(self.data)
        self.read_pointer = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.read_pointer >= len(self.filtered_data):
            raise StopIteration()
        next_data = self.filtered_data[self.read_pointer]
        self.read_pointer += 1
        return next_data

    def __getitem__(self, index: int) -> Student:
        return self.filtered_data[index]

    def all(self):
        self.read_pointer = 0
        return self
