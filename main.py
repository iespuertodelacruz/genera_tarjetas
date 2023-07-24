import settings
from lib.render import TemplateEngine
from lib.repository import StudentRepository

students = StudentRepository()
tengine = TemplateEngine(project_dir=settings.PROJECT_DIR, school_year=settings.SCHOOL_YEAR)
tengine.render(students=students[0:100])
