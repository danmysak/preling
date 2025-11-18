import io
import mimetypes
from random import choice
import struct
import wave

from google import genai
from google.genai import types
import pyaudio

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


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Convert raw audio data to WAV format."""
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters['bits_per_sample']
    sample_rate = parameters['rate']
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        chunk_size,
        b'WAVE',
        b'fmt ',
        16,
        1,
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b'data',
        data_size,
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    """Parse bits per sample and rate from an audio MIME type string."""
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(';')
    for param in parts:
        param = param.strip()
        if param.lower().startswith('rate='):
            try:
                rate_str = param.split('=', 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith('audio/L'):
            try:
                bits_per_sample = int(param.split('L', 1)[1])
            except (ValueError, IndexError):
                pass

    return {'bits_per_sample': bits_per_sample, 'rate': rate}


def read(text: str, language: str, model: str, api_key: str) -> None:
    """Read the given text using Gemini's TTS service."""
    client = genai.Client(api_key=api_key)

    contents = [
        types.Content(
            role='user',
            parts=[
                types.Part.from_text(text=f'Read the following text in {language}: {text}'),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=['audio'],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=choice(VOICES),
                ),
            ),
        ),
    )

    audio_chunks = []
    mime_type = None

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        if (
            chunk.candidates[0].content.parts[0].inline_data
            and chunk.candidates[0].content.parts[0].inline_data.data
        ):
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            if mime_type is None:
                mime_type = inline_data.mime_type
            audio_chunks.append(inline_data.data)

    if audio_chunks:
        raw_audio = b''.join(audio_chunks)
        
        file_extension = mimetypes.guess_extension(mime_type)
        if file_extension is None:
            wav_data = convert_to_wav(raw_audio, mime_type)
        else:
            wav_data = raw_audio
        with wave.open(io.BytesIO(wav_data), 'rb') as wf:
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
