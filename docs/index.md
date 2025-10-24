# transcriber

[![Release](https://img.shields.io/github/v/release/dscoular/transcriber)](https://img.shields.io/github/v/release/dscoular/transcriber)
[![Build status](https://img.shields.io/github/actions/workflow/status/dscoular/transcriber/main.yml?branch=main)](https://github.com/dscoular/transcriber/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/dscoular/transcriber)](https://img.shields.io/github/commit-activity/m/dscoular/transcriber)
[![License](https://img.shields.io/github/license/dscoular/transcriber)](https://img.shields.io/github/license/dscoular/transcriber)


## Description

A python script which uses [Open AI Whisper](https://github.com/openai/whisper) to transcribe videos and outputs SRT subtitle text files.

SRT subtitle text files are describribed by this Wikipedia entry:

- [SubRip](https://en.wikipedia.org/wiki/SubRip)

This **`transcribe`** script is intended to be used, primarily, with the [Bonsai Tutorials](https://hub.openingdesign.com/OpeningDesign/Bonsai_Tutorials#readme) video collection
to create SRT subtitle text files for the tutorial videos.

Since there were so many videos it became difficult to remember which one contained
a valuable explanation and exactly when in the video that explanation occurred.

I found the [OpenAI Whisper](https://github.com/openai/whisper) python library and set about using it to
transcribe the videos to SRT subtitle text files (thanks to the [pydub](https://github.com/jiaaro/pydub)
and [pysrt](https://github.com/byroot/pysrt) modules).

I used [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) to try to ensure I had
the basis of a modern python project.

## Prerequisites

You can either use the included **`Dockerfile`** and the **`docker`** command to make use of this script (simpler)
or use python's [uv](https://docs.astral.sh/uv/) to manage the script's dependencies (a little more involved).

See the [🚀 Getting Started](getting-started.md) document for more details.

## Notes

*Each matching video found in the target directory will have an `.srt` file created as a sibling. This makes it easy for video players to match the video with the subtitles.*
