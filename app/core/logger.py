"""Configura o logger para salvar logs em formato JSON."""

import logging

from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",  # nível mínimo do logger
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

logger = logging.getLogger("rich")
