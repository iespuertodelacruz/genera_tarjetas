from __future__ import annotations

import datetime

import logzero

import settings


def init_logger():
    logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )

    console_formatter = logzero.LogFormatter(fmt=logformat)
    file_formatter = logzero.LogFormatter(fmt=logformat, color=False)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
        encoding='utf-8',
    )
    return logzero.logger


def get_school_year() -> str:
    SCHOOL_YEAR_STARTING_MONTH = 9

    today = datetime.date.today()
    if SCHOOL_YEAR_STARTING_MONTH <= today.month <= 12:
        return f'{today.year}-{today.year + 1}'
    else:
        return f'{today.year-1}-{today.year}'
