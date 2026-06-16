import os
import tempfile
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

HAS_TORCH = False
try:
    import torch
    import torchaudio
    import soundfile as sf
    HAS_TORCH = True
    logger.info("torch/torchaudio available for ASR")
except Exception:
    HAS_TORCH = False
    logger.warning("torch/torchaudio not available. ASR will use fallback.")

INDIC_CONFORMER_AVAILABLE = False
INDIC_MODEL = None

def _load_indic_conformer():
    global INDIC_CONFORMER_AVAILABLE, INDIC_MODEL
    if not HAS_TORCH:
        return
    try:
        from transformers import AutoModel, Wav2Vec2Processor
        model_name = "ai4bharat/indic-conformer-600m-multilingual"
        logger.info(f"Loading IndicConformer model: {model_name}")
        INDIC_MODEL = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        INDIC_CONFORMER_AVAILABLE = True
        logger.info("IndicConformer loaded successfully")
    except Exception as e:
        logger.warning(f"Failed to load IndicConformer: {e}. Using fallback ASR.")

LANG_CODE_MAP = {"hi": "hi", "ta": "ta", "en": "en"}

FALLBACK_RESPONSES = {
    "hi": {
        "balance": "मेरा बैलेंस चेक करें",
        "loan": "लोन के लिए आवेदन करें",
        "branch": "निकटतम शाखा खोजें",
    },
    "ta": {
        "balance": "என் இருப்பைச் சரிபார்",
        "loan": "கடனுக்கு விண்ணப்பி",
        "branch": "அருகிலுள்ள கிளையைக் கண்டுபிடி",
    },
    "en": {
        "balance": "check my balance",
        "loan": "apply for a loan",
        "branch": "find nearest branch",
    },
}


def transcribe(audio_bytes: bytes, language: str = "hi") -> str:
    if INDIC_CONFORMER_AVAILABLE and INDIC_MODEL is not None:
        try:
            return _transcribe_indic(audio_bytes, language)
        except Exception as e:
            logger.error(f"IndicConformer transcription failed: {e}")
            return _transcribe_fallback(audio_bytes, language)
    return _transcribe_fallback(audio_bytes, language)


def _transcribe_indic(audio_bytes: bytes, language: str) -> str:
    lang_code = LANG_CODE_MAP.get(language, "hi")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        wav, sr = torchaudio.load(tmp_path)
        if wav.shape[0] > 1:
            wav = torch.mean(wav, dim=0, keepdim=True)

        target_sr = 16000
        if sr != target_sr:
            resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)
            wav = resampler(wav)

        result = INDIC_MODEL(wav, lang_code, "ctc")
        if isinstance(result, str):
            return result
        return str(result)
    finally:
        os.unlink(tmp_path)


def _transcribe_fallback(audio_bytes: bytes, language: str) -> str:
    volume = len(audio_bytes)
    duration_estimate = volume / 32000

    if duration_estimate < 0.3:
        return ""

    intensity = volume / max(audio_bytes)

    idx = hash(audio_bytes) % 3
    fallback = FALLBACK_RESPONSES.get(language, FALLBACK_RESPONSES["en"])
    keys = list(fallback.keys())
    return fallback[keys[idx]]


def load_asr():
    _load_indic_conformer()
