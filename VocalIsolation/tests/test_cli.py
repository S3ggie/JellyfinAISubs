from pathlib import Path

import pytest

from viso.cli import VisoError, default_output_path, isolate_vocals


def test_default_output_path():
    p = Path("/tmp/sample-video.mp4")
    assert default_output_path(p) == Path("/tmp/sample-video-viso.wav")


def test_missing_input_raises(tmp_path):
    missing = tmp_path / "nope.mp4"
    with pytest.raises(VisoError, match="Input file not found"):
        isolate_vocals(missing, None, "htdemucs", False)
