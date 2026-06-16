import os
import io
import tempfile
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False
    logger.warning("gTTS not available. TTS will be disabled.")

AUDIO_CACHE_DIR = Path(__file__).resolve().parent.parent / "audio"
AUDIO_CACHE_DIR.mkdir(exist_ok=True)

def _cache_key(text: str, lang: str) -> str:
    import hashlib
    h = hashlib.md5(f"{lang}:{text}".encode()).hexdigest()
    return f"tts_{h}.mp3"


def text_to_speech(text: str, lang: str = "hi") -> Optional[bytes]:
    cache_file = AUDIO_CACHE_DIR / _cache_key(text, lang)

    if cache_file.exists():
        logger.debug(f"TTS cache hit: {cache_file}")
        with open(cache_file, "rb") as f:
            return f.read()

    if not HAS_GTTS:
        logger.warning("gTTS not installed, returning None")
        return None

    try:
        tts_lang_map = {"hi": "hi", "ta": "ta", "en": "en"}
        tts_lang = tts_lang_map.get(lang, "hi")

        tts = gTTS(text=text, lang=tts_lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_bytes = fp.getvalue()

        with open(cache_file, "wb") as f:
            f.write(audio_bytes)

        return audio_bytes
    except Exception as e:
        logger.error(f"TTS failed: {e}")
        return None
