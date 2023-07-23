import csv

import settings
from lib.render import TemplateEngine

with open('data/alumnado.csv', encoding='latin-1') as f:
    reader = csv.DictReader(f, delimiter=';')
    data = list(reader)

tengine = TemplateEngine()
tengine.render('tarjetas.jinja', 'pepe.pdf', nombre='Sergio', project_dir=settings.PROJECT_DIR)
