# 📥 ytd.py — Python YouTube Downloader and Trimmer

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Powered by yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)

A powerful command-line tool built on **yt-dlp** for downloading and processing YouTube videos with:

* ⏱️ Precise trimming (`HH:MM:SS`, `MM:SS`, `SS`)
* 🎵 Audio extraction
* 🎬 Format control
* 📜 Playlist support
* 📝 Subtitle downloading
* 🍪 Cookie-based authentication

---

## ✨ Features

* Flexible time parsing (`1:30`, `00:01:30`, `90`)
* Automatic conversion to seconds for ffmpeg
* Clean CLI interface with helpful flags
* Supports restricted/private videos via cookies

---

## ⚙️ Requirements

* Python **3.8+**
* [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
* [`ffmpeg`](https://ffmpeg.org/) *(required for trimming & audio conversion)*

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ytd.py.git
cd ytd.py
pip install yt-dlp
pip install ffmpeg
```

### Install ffmpeg

Make sure `ffmpeg` is available in your system PATH.

* Windows: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

---

## 🚀 Usage

```bash
python ytd.py <url> [options]
```
---

## 🧪 Examples

```bash
# Best quality
python ytd.py https://youtube.com/watch?v=example

# Trim clip
python ytd.py <url> --start 1:00 --end 2:30

# Extract WAV audio
python ytd.py <url> --audio-only --audio-format wav

# Playlist subset
python ytd.py <playlist_id> --playlist --playlist-start 2 --playlist-end 10

# Restricted video
python ytd.py <url> --cookies cookies.txt
```

---

## ⏱️ Trimming

```bash
python ytd.py <url> --start 10:30 --end 11:00
```

Supported formats:

* `SS` → `90`
* `MM:SS` → `1:30`
* `HH:MM:SS` → `00:01:30`

> ⚠️ Requires `ffmpeg`

---

## 🎵 Audio Extraction

```bash
python ytd.py <url> --audio-only --audio-format mp3
```

Supported formats:
`mp3`, `m4a`, `wav`, `flac`, `opus`, `aac`

---

## 🎬 Format Selection

```bash
python ytd.py <url> -f bestvideo+bestaudio
```

| Format      | Description                 |
| ----------- | --------------------------- |
| `best`      | Best combined video + audio |
| `worst`     | Lowest quality              |
| `bestvideo` | Best video only             |
| `bestaudio` | Best audio only             |

---

## 📁 Output Customization

```bash
python ytd.py <url> -o [folder]/<filename>
```

Common template fields:

* `%(title)s`
* `%(ext)s`

---

## 📜 Playlists

```bash
python ytd.py <playlist_id> --playlist
```

Download a subset:

```bash
python ytd.py <playlist_id> --playlist --playlist-start 1 --playlist-end 5
```

---

## 📝 Subtitles

```bash
python ytd.py <url> --subtitles --sub-lang en
```

---

## 🍪 Cookies (Restricted Videos)

```bash
python ytd.py <url> --cookies cookies.txt
```

You can export cookies using browser extensions like:

* [cookies.txt (by Lennon Hill)](https://cookies-txt.en.softonic.com/firefox/extension)

---

## 🚦 Rate Limiting

```bash
python ytd.py <url> --rate-limit 1M
```

Examples:

* `500K`
* `2M`

---

## 🔇 Modes

```bash
# Quiet mode
python ytd.py <url> --quiet

# Debug mode
python ytd.py <url> --verbose
```

---

## ⚠️ Notes

* Trimming is handled by `ffmpeg` and may not be frame-perfect.
* Some formats depend on availability from YouTube.
* `--audio-only` overrides video format settings.
* Playlist downloads are disabled unless `--playlist` is specified.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

## 🙌 Credits

* [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
* [`ffmpeg`](https://ffmpeg.org/)
