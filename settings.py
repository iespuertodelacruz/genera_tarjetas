from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

TEMPLATES_DIR = config('TEMPLATES_DIR', default=PROJECT_DIR / 'templates', cast=Path)
CARDS_OUTPUT_DIR = config('CARDS_OUTPUT_DIR', default=PROJECT_DIR / 'output', cast=Path)
OUTPUT_SUFFIX = config('OUTPUT_SUFFIX', default='.pdf')
