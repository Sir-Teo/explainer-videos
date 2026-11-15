"""Cold clip lookup must resolve the computation, not depend on prebuilt audio."""
from types import SimpleNamespace
import pytest
from explainer.music.sound import clip_loader

@pytest.mark.parametrize('name,aliases,item', [
    ('tone.example', {}, 'tone'),
    ('next.example', {'next': 'nextpart'}, 'nextpart'),
])
def test_cold_lookup_computes_then_reuses_clip(name, aliases, item):
    stored = {}
    calls = []
    payload = object()
    def compute(key):
        calls.append(key)
        stored[name] = payload
    cache = SimpleNamespace(load=compute)
    store = SimpleNamespace(has=lambda key: key in stored, load=stored.__getitem__)
    clip = clip_loader(cache, store, item_aliases=aliases)
    assert clip(name) is payload
    assert clip(name) is payload
    assert calls == [item]


def test_missing_clip_error_names_actual_computation():
    cache = SimpleNamespace(load=lambda key: None)
    store = SimpleNamespace(has=lambda key: False)
    clip = clip_loader(cache, store, item_aliases={'next': 'nextpart'})
    with pytest.raises(FileNotFoundError, match='--force nextpart'):
        clip('next.example')
