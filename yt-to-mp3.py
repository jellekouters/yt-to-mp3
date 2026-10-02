#!/usr/bin/env python3
"""
yt_to_mp3.py - Download audio from a YouTube link as a 320 kbps MP3.

Requirements:
    pip install -U yt-dlp
    ffmpeg must be installed and on your PATH
        macOS:   brew install ffmpeg
        Windows: winget install ffmpeg
        Linux:   sudo apt install ffmpeg

Usage:
    python yt_to_mp3.py                     # prompts for a link
    python yt_to_mp3.py <url> [<url> ...]   # one or more links
    python yt_to_mp3.py <url> -o ~/Music    # custom output folder
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp is not installed. Run: pip install -U yt-dlp")


def download_mp3(urls, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,  # only grab the single video, even if the link is part of a playlist
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {"key": "FFmpegMetadata"},      # write title/artist tags
            {"key": "EmbedThumbnail"},      # use the video thumbnail as cover art
        ],
        "writethumbnail": True,
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(urls)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download YouTube audio as 320 kbps MP3.")
    parser.add_argument("urls", nargs="*", help="YouTube link(s)")
    parser.add_argument("-o", "--output", default="downloads", help="Output folder (default: ./downloads)")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found. Install it and make sure it's on your PATH.")

    urls = args.urls
    if not urls:
        link = input("Paste YouTube link: ").strip()
        if not link:
            sys.exit("No link given.")
        urls = [link]

    try:
        download_mp3(urls, Path(args.output).expanduser())
        print(f"\nDone. Files saved to: {Path(args.output).expanduser().resolve()}")
    except yt_dlp.utils.DownloadError as e:
        sys.exit(f"\nDownload failed: {e}")


if __name__ == "__main__":
    main()