import copy
import csv
import datetime
import operator
import tempfile
from pathlib import Path

import qrcode

import settings


class Student:
    def __init__(self, data: dict[str, str]):
        self.data = data

    @staticmethod
    def fix_empty_field(default_output=settings.EMPTY_FIELD_PLACEHOLDER):
        def decorator(method):
            def wrapper(self, *args, **kwargs):
                if result := method(self, *args, **kwargs):
                    return result
                return default_output

            return wrapper

        return decorator

    @property
    @fix_empty_field()
    def cial(self):
        return self.data['CIAL']

    @property
    @fix_empty_field()
    def exp(self):
        return self.data['Expediente']

    @property
    @fix_empty_field()
    def id(self):
        return self.data['NIF - NIE']

    @property
    @fix_empty_field()
    def name(self):
        return self.data['Nombre']

    @property
    @fix_empty_field()
    def surname1(self):
        return self.data['Primer apellido']

    @property
    @fix_empty_field('')
    def surname2(self):
        return self.data['Segundo apellido']

    @property
    def surname(self):
        if self.surname2:
            return f'{self.surname1} {self.surname2}'
        return self.surname1

    @property
    def fullname(self):
        return f'{self.name} {self.surname}'.title()

    @property
    @fix_empty_field()
    def date_of_birth(self):
        return self.data['Fecha de nacimiento']

    @property
    def calculated_age(self):
        a = datetime.datetime.strptime(self.date_of_birth, '%d/%m/%Y')
        b = datetime.datetime.now()
        return int((b - a).days / 365)

    @property
    def age(self) -> int:
        try:
            return int(self.data['Edad'])
        except ValueError:
            return 0

    @property
    def adult(self):
        return self.age >= 18

    @property
    @fix_empty_field()
    def study(self):
        return self.data['Estudio den. corta']

    @property
    @fix_empty_field()
    def group(self):
        return self.data['Grupo Clase']

    @property
    @fix_empty_field()
    def gender(self):
        return self.data['Sexo']

    @property
    @fix_empty_field()
    def shift(self):
        return self.data['Turnos']

    @property
    def short_shift(self):
        return self.shift[0].upper()

    @property
    @fix_empty_field()
    def long_shift(self):
        match self.short_shift:
            case 'M':
                return 'Turno de mañana'
            case 'T':
                return 'Turno de tarde'
            case 'N':
                return 'Turno de noche'
            case _:
                return ''

    @property
    def list_number(self):
        try:
            return int(self.data['Nº Lista'])
        except ValueError:
            return 0

    @property
    def sign_up_date(self):
        return self.data['Fecha de matrícula']

    @property
    def sign_out_date(self):
        return self.data['Fecha de baja']

    @property
    def active(self):
        return self.sign_out_date == ''

    @property
    def pic(self):
        if (pic_path := settings.PROFILE_PICS_PATH / (self.exp + '.jpg')).exists():
            return pic_path
        elif self.gender == 'V':
            pic_path = settings.ASSETS_IMG_DIR / settings.UNKNOWN_MAN_PROFILE_PIC
        else:
            pic_path = settings.ASSETS_IMG_DIR / settings.UNKNOWN_WOMAN_PROFILE_PIC
        return pic_path

    @property
    def qr(self) -> Path:
        qr_ = qrcode.QRCode(border=0)
        qr_.add_data(settings.QR_CONTENT)
        qr_.make(fit=True)
        img = qr_.make_image()
        qr_path = tempfile.NamedTemporaryFile().name
        img.save(qr_path)
        return Path(qr_path)

    def __repr__(self):
        return self.fullname


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

    def __getitem__(self, index: int | slice) -> Student | list[Student]:
        return self.filtered_data[index]

    def all(self):
        self.read_pointer = 0
        return self

    def filter(self, **kwargs):
        self.filtered_data = copy.deepcopy(self.data)
        for key, value in kwargs.items():
            if value == [] or value is None:
                continue
            value = value if isinstance(value, list) else [value]
            self.filtered_data = [s for s in self.filtered_data if getattr(s, key) in value]
        self.read_pointer = 0
        return self

    def sort(self, *fields):
        if len(fields) > 0:
            self.filtered_data.sort(key=operator.attrgetter(*fields))
        return self

    def __repr__(self):
        return '\n'.join(str(s) for s in self.data)
