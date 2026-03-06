from __future__ import annotations

from pathlib import Path

import wavsub.cli as cli_mod


class _Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def _base_args(tmp_path: Path, input_name: str = "input.wav") -> _Args:
    input_file = tmp_path / input_name
    input_file.write_bytes(b"RIFF....WAVEfmt ")
    return _Args(
        input_file=str(input_file),
        format="both",
        model="small",
        device="auto",
        language=None,
        output_base=None,
    )


def test_main_writes_srt_and_lrc(monkeypatch, tmp_path):
    args = _base_args(tmp_path)

    def fake_parse_args():
        return args

    def fake_transcribe(input_file, model, device, language):
        assert input_file.name == "input.wav"
        assert model == "small"
        assert device == "auto"
        assert language is None
        return [
            cli_mod.Segment(0.0, 1.23, "hello"),
            cli_mod.Segment(1.5, 2.5, "world"),
        ]

    monkeypatch.setattr(cli_mod.argparse.ArgumentParser, "parse_args", staticmethod(fake_parse_args))
    monkeypatch.setattr(cli_mod, "transcribe", fake_transcribe)

    rc = cli_mod.main()
    assert rc == 0

    assert (tmp_path / "input.srt").exists()
    assert (tmp_path / "input.lrc").exists()


def test_main_format_srt_only(monkeypatch, tmp_path):
    args = _base_args(tmp_path, "speech.wav")
    args.format = "srt"

    monkeypatch.setattr(cli_mod.argparse.ArgumentParser, "parse_args", staticmethod(lambda: args))
    monkeypatch.setattr(
        cli_mod,
        "transcribe",
        lambda **_: [cli_mod.Segment(0.0, 1.0, "line")],
    )

    rc = cli_mod.main()
    assert rc == 0
    assert (tmp_path / "speech.srt").exists()
    assert not (tmp_path / "speech.lrc").exists()


def test_main_transcribe_failure_returns_nonzero(monkeypatch, tmp_path):
    args = _base_args(tmp_path, "bad.wav")

    monkeypatch.setattr(cli_mod.argparse.ArgumentParser, "parse_args", staticmethod(lambda: args))

    def fail(**_):
        raise cli_mod.WavSubError("boom")

    monkeypatch.setattr(cli_mod, "transcribe", fail)

    rc = cli_mod.main()
    assert rc == 1
    assert not (tmp_path / "bad.srt").exists()
    assert not (tmp_path / "bad.lrc").exists()
