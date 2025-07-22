from pathlib import Path
from typing import Annotated

from typer import Argument

from preling.app.app import app

__all__ = [
    'init',
]


@app.command()
def init(
        language: Annotated[
            str,
            Argument(help='Language code supported by spaCy (e.g., "en", "fr", "uk").'),
        ],
        corpus: Annotated[
            Path,
            Argument(
                dir_okay=False,
                exists=True,
                readable=True,
                resolve_path=True,
                help='Plain‑text file containing one sentence per line.',
            ),
        ],
) -> None:
    """Initialise PreLing for a new language."""
    print(f"Initialising language '{language}' with corpus '{corpus}'...")
