# transcriber

[![Release](https://img.shields.io/github/v/release/dscoular/transcriber)](https://img.shields.io/github/v/release/dscoular/transcriber)
[![Build status](https://img.shields.io/github/actions/workflow/status/dscoular/transcriber/main.yml?branch=main)](https://github.com/dscoular/transcriber/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/dscoular/transcriber)](https://img.shields.io/github/commit-activity/m/dscoular/transcriber)
[![License](https://img.shields.io/github/license/dscoular/transcriber)](https://img.shields.io/github/license/dscoular/transcriber)

A python script which uses whisper to transcribe videos and outputs SRT subtitle text files.

- **Github repository**: <https://github.com/dscoular/transcriber/>
- **Documentation** <https://dscoular.github.io/transcriber/>

# UV or Docker - that is the question.

If you have `uv` in your `PATH` and `ffmpeg` installed in your operating system, you should
be able to do the following to install and use this package.

1. `make` - runs the default target of `make help` to show help on all the `make` targets.
2. `make install` - installs the virtual environment and pre-commit hooks.
3. `make check` - **optional**, runs the code quality tools.
4. `make test` - **optional**, runs unit tests.
5. `make docs-test` - **optional**, generate HTML documents in the `site` directory.
6. `make transcribe` - by default, this converts the videos in the input path to `.srt` subtitle text files.

Doug Scoular
dscoular@gmail.com
