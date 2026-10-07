"""Small language-model utilities used to generate the "real model" footage in
the LLM video: probes of GPT-2 small (``gpt2``), a minimal character-level
transformer trained from scratch (``tiny_gpt``), and a toy byte-pair encoder
(``bpe``).  Scenes never run a model; ``videos/llm/analyze.py`` caches results."""
