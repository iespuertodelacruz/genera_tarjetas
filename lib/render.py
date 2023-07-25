import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import jinja2
from logzero import logger

import settings


class TemplateEngine:
    def __init__(
        self,
        templates_dir: Path = settings.TEMPLATES_DIR,
        output_dir: Path = settings.CARDS_OUTPUT_DIR,
        **env_vars,
    ):
        loader = jinja2.FileSystemLoader(templates_dir)
        self.env = jinja2.Environment(loader=loader)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.env_vars = env_vars

    def render(
        self,
        template_name: str = settings.CARDS_TEMPLATE_NAME,
        output_path: Path = settings.CARDS_OUTPUT_PATH,
        **args,
    ) -> None:
        template = self.env.get_template(template_name)
        rendered_template_path = NamedTemporaryFile().name
        logger.debug(f'Renderizando plantilla desde {template_name}')
        rendered_template = template.render(**(self.env_vars | args))
        with open(rendered_template_path, 'w') as f:
            f.write(rendered_template)
        rendered_file_path = output_path
        cmd = f'prince {rendered_template_path} -o {rendered_file_path}'
        logger.debug(f'Escribiendo salida a {rendered_file_path}')
        subprocess.run(shlex.split(cmd))
