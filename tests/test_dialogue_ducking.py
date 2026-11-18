import pytest
from audio import dialogue_ducking as mod

CASES = [
    ("duck_reduce", "m.duck_gain(1.0, 0.5, 0.3) == approx(0.7)"),
    ("duck_zero", "m.duck_gain(1.0, 0.0, 0.3) == approx(1.0)"),
    ("indoor_label", "m.indoor_group(True) == 'indoor'"),
    ("outdoor_label", "m.indoor_group(False) == 'outdoor'"),
    ("delay_half", "m.fixed_delay(480, 48000) == approx(0.01)"),
    ("frames_48", "m.timecode_to_frames(2.0, 24) == 48"),
    ("phoneme_ratio", "m.phoneme_alignment(10, 20) == approx(2.0)"),
    ("preset_en", "m.load_preset('en') == 'reverb_en'"),
    ("route_dialogue", "m.bus_route('dialogue') == 'dialogue'"),
    ("route_narration", "m.bus_route('narration') == 'narration'"),
    ("channels_unique", "m.subtitle_channels(['en', 'en', 'zh']) == ['en', 'zh']"),
    ("pause_zero", "m.pause_sync(5.0, True) == 0"),
    ("pause_keep", "m.pause_sync(5.0, False) == 5.0"),
    ("rate_mix", "m.unify_rate(44100, 48000) == 48000"),
    ("duck_full", "m.duck_gain(1.0, 1.0, 1.0) == approx(0.0)")
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
