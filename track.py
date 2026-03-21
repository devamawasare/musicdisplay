from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    title: str
    artist: str | None = None
    album: str | None = None
    cover_bytes: bytes | None = None
