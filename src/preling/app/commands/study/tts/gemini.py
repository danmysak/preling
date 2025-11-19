import io
import os
from random import choice
import wave

from google.cloud import texttospeech
from google.oauth2 import service_account
import pyaudio

from preling.utils.typer import typer_raise

__all__ = [
    'read',
]

VOICES = [
    'Achernar',
    'Achird',
    'Algenib',
    'Algieba',
    'Alnilam',
    'Aoede',
    'Autonoe',
    'Callirrhoe',
    'Charon',
    'Despina',
    'Enceladus',
    'Erinome',
    'Fenrir',
    'Gacrux',
    'Iapetus',
    'Kore',
    'Laomedeia',
    'Leda',
    'Orus',
    'Puck',
    'Pulcherrima',
    'Rasalgethi',
    'Sadachbia',
    'Sadaltager',
    'Schedar',
    'Sulafat',
    'Umbriel',
    'Vindemiatrix',
    'Zephyr',
    'Zubenelgenubi',
]


def read(text: str, locale: str | None, model: str, api_key: str) -> None:
    """Read the given text using Google Cloud TTS with Gemini voices."""
    if locale is None:
        typer_raise('TTS Locale must be specified for Gemini voices.')

    if not os.path.isfile(api_key):
        typer_raise('For Google Cloud TTS, the API key must be a path to a service account JSON file.')

    client = texttospeech.TextToSpeechClient(
        credentials=service_account.Credentials.from_service_account_file(api_key),
    )

    synthesis_input = texttospeech.SynthesisInput(
        text=text,
        prompt='Read exactly as written at a normal pace.',
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code=locale,
        name=choice(VOICES),
        model_name=model,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    with wave.open(io.BytesIO(response.audio_content), 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )

        chunk_size = 1024
        data = wf.readframes(chunk_size)
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)

        stream.stop_stream()
        stream.close()
        p.terminate()
