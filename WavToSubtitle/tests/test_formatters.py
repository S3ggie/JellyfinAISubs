from wavsub.cli import Segment, fmt_lrc_timestamp, fmt_srt_timestamp, segments_to_lrc, segments_to_srt


def test_srt_timestamp():
    assert fmt_srt_timestamp(65.432) == "00:01:05,432"


def test_lrc_timestamp():
    assert fmt_lrc_timestamp(65.43) == "[01:05.43]"


def test_segments_to_srt():
    s = [Segment(0.0, 1.2, "Hello"), Segment(1.2, 2.4, "world")]
    out = segments_to_srt(s)
    assert "1\n00:00:00,000 --> 00:00:01,200\nHello" in out
    assert "2\n00:00:01,200 --> 00:00:02,400\nworld" in out


def test_segments_to_lrc():
    s = [Segment(0.0, 1.2, "Hello"), Segment(1.2, 2.4, "world")]
    out = segments_to_lrc(s)
    assert "[00:00.00]Hello" in out
    assert "[00:01.20]world" in out
