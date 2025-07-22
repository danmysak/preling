from typing import Annotated

from typer import Argument, Option

from preling.app.app import app

__all__ = [
    'study',
]


@app.command()
def study(
        model: Annotated[
            str,
            Option(
                '--model',
                envvar='PRELING_MODEL',
                help='GPT model for grammar evaluation.',
            ),
        ],
        tts_model: Annotated[
            str,
            Option(
                '--tts-model',
                envvar='PRELING_TTS_MODEL',
                help='Text‑to‑speech model.',
            ),
        ],
        api_key: Annotated[
            str,
            Option(
                '--api-key',
                envvar='PRELING_API_KEY',
                help='OpenAI API key.',
            ),
        ],
        language: Annotated[
            str,
            Argument(
                help='Language code previously initialised with `preling init`.',
            ),
        ],
        audio: Annotated[
            bool,
            Option(
                '--audio',
                help='Play audio in addition to printing text.',
            ),
        ] = False,
        audio_only: Annotated[
            bool,
            Option(
                '--audio-only',
                help='Play audio without displaying the text.',
            ),
        ] = False,
) -> None:
    """Launch an interactive study session."""
    print(f'Studying {language}: audio={audio}, audio_only={audio_only}, '
          f'model={model}, tts_model={tts_model}, api_key={api_key}...')
