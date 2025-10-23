# transcriber

[![Release](https://img.shields.io/github/v/release/dscoular/transcriber)](https://img.shields.io/github/v/release/dscoular/transcriber)
[![Build status](https://img.shields.io/github/actions/workflow/status/dscoular/transcriber/main.yml?branch=main)](https://github.com/dscoular/transcriber/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/dscoular/transcriber)](https://img.shields.io/github/commit-activity/m/dscoular/transcriber)
[![License](https://img.shields.io/github/license/dscoular/transcriber)](https://img.shields.io/github/license/dscoular/transcriber)


## Description

A python script which uses whisper to transcribe videos and outputs SRT files.

This script is intended to be used, primarily, with the [Bonsai Tutorials](https://hub.openingdesign.com/OpeningDesign/Bonsai_Tutorials#readme) video collection
to create SRT subtitle text files.

Since there were so many videos it became difficult to remember which one contained
a valuable explanation and exactly when in the video that explanation occurred.

I found the [OpenAI Whisper](https://github.com/openai/whisper) python library and set about using it to
transcribe the videos to SRT subtitle text files (thanks to the [pydub
(AudioSegment)](https://github.com/jiaaro/pydub), [[pysrt](https://github.com/byroot/pysrt)) and
[pysrt](https://github.com/byroot/pysrt)) modules.

I used [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) to try to ensure I had
the basis of a modern python project.

## Prerequisites

You must have the python's uv, make and ffmpeg installed on your system. See the [🚀 Getting Started](starting.md) document for more details.

## Notes

The `.srt` files we produce will be created recursively as siblings of your existing video files.
