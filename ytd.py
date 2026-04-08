#!/usr/bin/env python3
import argparse
from yt_dlp import YoutubeDL

#Time helper function
def hms_to_seconds(time_str):
    parts = list(map(int, time_str.split(":")))
    
    if len(parts) == 3:  # HH:MM:SS
        h, m, s = parts
    elif len(parts) == 2:  # MM:SS
        h = 0
        m, s = parts
    elif len(parts) == 1:  # SS
        h = 0
        m = 0
        s = parts[0]
    else:
        raise ValueError("Invalid time format")

    return h * 3600 + m * 60 + s


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos using yt-dlp with optional trimming and format control.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""

Examples:
  # Download best quality
  python ytd.py <url>
  
  # Download with cookie for restricted videos
  python ytd.py <url> -cookies <cookies>.txt (Use an extension such as cookies.txt by Lennon Hill to download youtube cookies into a cookies.txt file)

  # Trim from 10:30 to 11:00
  python ytd.py <url> --start 10:30 --end 11:00

  # Download audio only as mp3 ("best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", or "wav")
  python ytd.py <url> --audio-only --audio-format mp3

  # Custom output filename and format (3gp, aac, flv, m4a, mp3, mp4, ogg, wav, webm)
  python ytd.py <url> --output my_video.mp4 --format bestvideo+bestaudio
  
  Other options include:
  
  best: Select the best quality format represented by a single file with video and audio.
  worst: Select the worst quality format represented by a single file with video and audio.
  bestvideo: Select the best quality video-only format (e.g. DASH video). May not be available.
  worstvideo: Select the worst quality video-only format. May not be available.
  bestaudio: Select the best quality audio only-format. May not be available.
  worstaudio: Select the worst quality audio only-format. May not be available.

  # Download a playlist
  python ytd.py <playlist_url> --playlist

  # Add subtitles
  python ytd.py <url> --subtitles
        """
    )

    parser.add_argument("url", help="YouTube URL to download")
    
    # Trimming options
    parser.add_argument("--start", type=str, metavar="TIME",
                    help="Start time (HH:MM:SS, MM:SS, or SS)")
    parser.add_argument("--end", type=str, metavar="TIME",
                    help="End time (HH:MM:SS, MM:SS, or SS)")

    # Output options
    parser.add_argument("-o", "--output", default="%USERPROFILE%\Videos\%(title)s.%(ext)s",
                        help="Output filename template (default: video title)")
    parser.add_argument("-f", "--format", default="mp4",
                        help="Format selector (default: mp4")

    # Audio options
    parser.add_argument("--audio-only", action="store_true",
                        help="Download audio only")
    parser.add_argument("--audio-format", default="mp3",
                        choices=["mp3", "m4a", "wav", "flac", "opus", "aac"],
                        help="Audio format when using --audio-only (default: mp3)")

    # Playlist options
    parser.add_argument("--playlist", action="store_true",
                        help="Allow playlist downloads (single video by default)")
    parser.add_argument("--playlist-start", type=int, metavar="N",
                        help="Playlist index to start at")
    parser.add_argument("--playlist-end", type=int, metavar="N",
                        help="Playlist index to end at")

    # Subtitle options
    parser.add_argument("--subtitles", action="store_true",
                        help="Download subtitles if available")
    parser.add_argument("--sub-lang", default="en",
                        help="Subtitle language code (default: en)")

    # Misc options
    parser.add_argument("--no-overwrites", action="store_true",
                        help="Do not overwrite existing files")
    parser.add_argument("--rate-limit", metavar="RATE",
                        help="Download speed limit, e.g. 500K or 2M")
    parser.add_argument("--cookies", metavar="FILE",
                        help="Path to cookies file for age-restricted or private videos")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress output except errors")
    parser.add_argument("--verbose", action="store_true",
                        help="Print verbose debug info")

    return parser.parse_args()


def build_opts(args):
    ydl_opts = {
        "format": args.format,
        "outtmpl": args.output,
        "nooverwrites": args.no_overwrites,
        "quiet": args.quiet,
        "verbose": args.verbose,
        "noplaylist": not args.playlist,
    }

    # Trimming via ffmpeg
    if args.start is not None or args.end is not None:
        ffmpeg_args = []
        if args.start is not None:
            ffmpeg_args += ["-ss", str(args.start)]
        if args.end is not None:
            ffmpeg_args += ["-to", str(args.end)]
        ydl_opts["external_downloader"] = "ffmpeg"
        ydl_opts["external_downloader_args"] = ffmpeg_args

    # Audio-only mode
    if args.audio_only:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": args.audio_format,
            "preferredquality": "192",
        }]

    # Playlist range
    if args.playlist_start:
        ydl_opts["playliststart"] = args.playlist_start
    if args.playlist_end:
        ydl_opts["playlistend"] = args.playlist_end

    # Subtitles
    if args.subtitles:
        ydl_opts["writesubtitles"] = True
        ydl_opts["subtitleslangs"] = [args.sub_lang]

    # Rate limit
    if args.rate_limit:
        ydl_opts["ratelimit"] = args.rate_limit

    # Cookies
    if args.cookies:
        ydl_opts["cookiefile"] = args.cookies

    return ydl_opts


def main():
    args = parse_args()

    if args.start:
        args.start = hms_to_seconds(args.start)
    if args.end:
        args.end = hms_to_seconds(args.end)

    ydl_opts = build_opts(args)

    print(f"Downloading: {args.url}")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])


if __name__ == "__main__":
    main()
