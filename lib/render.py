import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import jinja2

import settings


class TemplateEngine:
    def __init__(
        self,
        templates_dir: Path = settings.TEMPLATES_DIR,
        output_dir: Path = settings.CARDS_OUTPUT_DIR,
    ):
        loader = jinja2.FileSystemLoader(templates_dir)
        self.env = jinja2.Environment(loader=loader)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render(
        self,
        template_name: str,
        output_filename: str = '',
        output_suffix: str = settings.OUTPUT_SUFFIX,
        **args,
    ) -> None:
        template = self.env.get_template(template_name)
        rendered_template_path = NamedTemporaryFile().name
        rendered_template = template.render(**args)
        with open(rendered_template_path, 'w') as f:
            f.write(rendered_template)
        output_filename = output_filename or template_name.split('.')[0] + output_suffix
        rendered_pdf_path = self.output_dir / output_filename
        cmd = f'prince {rendered_template_path} -o {rendered_pdf_path}'
        subprocess.run(shlex.split(cmd))
