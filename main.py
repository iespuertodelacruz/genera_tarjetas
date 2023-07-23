import csv

import settings
from lib.render import TemplateEngine

with open('data/alumnado.csv', encoding='latin-1') as f:
    reader = csv.DictReader(f, delimiter=';')
    data = list(reader)

tengine = TemplateEngine(project_dir=settings.PROJECT_DIR)
tengine.render('tarjetas.jinja', nombre='Sergio')
