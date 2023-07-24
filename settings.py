from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name
DATA_DIR = PROJECT_DIR / 'data'

TEMPLATES_DIR = config('TEMPLATES_DIR', default=PROJECT_DIR / 'templates', cast=Path)
CARDS_OUTPUT_DIR = config('CARDS_OUTPUT_DIR', default=PROJECT_DIR / 'output', cast=Path)
OUTPUT_SUFFIX = config('OUTPUT_SUFFIX', default='.pdf')
SCHOOL_YEAR = config('SCHOOL_YEAR', default='2023-2024')
CARD_TEMPLATE_NAME = config('CARD_TEMPLATE_NAME', default='card.jinja')
STUDENTS_DATA_PATH = config('STUDENTS_DATA_PATH', default=DATA_DIR / 'students.csv')
EMPTY_FIELD_PLACEHOLDER = config('EMPTY_FIELD_PLACEHOLDER', default='-')
PROFILE_PICS_PATH = config('PROFILE_PICS_PATH', default=DATA_DIR / 'pics')
