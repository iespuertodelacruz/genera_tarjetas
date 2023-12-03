from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name
DATA_DIR = PROJECT_DIR / 'data'

TEMPLATES_DIR = config('TEMPLATES_DIR', default=PROJECT_DIR / 'templates', cast=Path)
CARDS_OUTPUT_DIR = config('CARDS_OUTPUT_DIR', default=PROJECT_DIR / 'output', cast=Path)

OUTPUT_SUFFIX = config('OUTPUT_SUFFIX', default='.pdf')
SCHOOL_YEAR = config('SCHOOL_YEAR', default='2023-2024')
CARDS_TEMPLATE_NAME = config('CARDS_TEMPLATE_NAME', default='cards.jinja')
STUDENTS_DATA_PATH = config('STUDENTS_DATA_PATH', default=DATA_DIR / 'students.csv', cast=Path)
CARDS_OUTPUT_PATH = config('CARDS_OUTPUT_PATH', default=CARDS_OUTPUT_DIR / 'cards.pdf', cast=Path)
EMPTY_FIELD_PLACEHOLDER = config('EMPTY_FIELD_PLACEHOLDER', default='-')
PROFILE_PICS_DIR = config('PROFILE_PICS_DIR', default=DATA_DIR / 'pics')

ASSETS_DIR = config('ASSETS_DIR', default=PROJECT_DIR / 'assets')
ASSETS_CSS_DIR = config('ASSETS_CSS_DIR', default=ASSETS_DIR / 'css')
ASSETS_FONTS_DIR = config('ASSETS_FONTS_DIR', default=ASSETS_DIR / 'fonts')
ASSETS_IMG_DIR = config('ASSETS_IMG_DIR', default=ASSETS_DIR / 'img')

UNKNOWN_MAN_PROFILE_PIC = config('UNKNOWN_MAN_PROFILE_PIC', default='avatar-man.jpg')
UNKNOWN_WOMAN_PROFILE_PIC = config('UNKNOWN_WOMAN_PROFILE_PIC', default='avatar-woman.jpg')

QR_CONTENT = config('QR_CONTENT', default='https://linktr.ee/iespuertodelacruz')

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)

CHECKING_EXCLUDED_FIELDS = config(
    'CHECKING_EXCLUDED_FIELDS', default='Pasaporte,Fecha de baja', cast=config.list
)

PRINCE_PATH = config('PRINCE_PATH', default='prince')
