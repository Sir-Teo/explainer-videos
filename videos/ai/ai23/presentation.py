"""Part23 presentation status; importing a scene must never run optional models."""
from __future__ import annotations

from explainer import tts


def narrator_presentation():
    """No implicit cache discovery or producer call, even if Qwen is installed.

    A measured narrator record needs a separately reviewed explicit provider.
    This not-run record contains no invented codes, timings or waveform results.
    """
    return {"available": False, "execution": "not_run",
            "reason": "No verified narrator-code result is selected",
            "sentence": "Every sense is a token: text, pictures and sound."}


def published_narrator_config():
    """Qwen3-TTS technical report's nominal codec configuration, not a run result."""
    return {"frame_hz": 12.5, "codebooks": 16, "codebook_size": 2048}


def narration_credit():
    """Keep the production backend's credit; identify silent QA truthfully."""
    if is_silent_qa():
        return r"Silent QA preview: \ estimated timing; \ no speech"
    return tts.narration_credit()


def is_silent_qa():
    return tts.BACKEND == "silent"


def budget_products(data):
    """A full measured budget must bind accepted data, never auto-run producers."""
    if not isinstance(data, dict) or data.get("numerical_acceptance", {}).get("status") != "passed":
        raise ValueError("Omni's measured budget requires independently accepted products")
    products = data.get("products", {})
    if set(products) != {"whisper", "codec", "vlm"} or not all(isinstance(v, dict) for v in products.values()):
        raise ValueError("Expected the accepted Whisper, codec and VLM budget products")
    return products
