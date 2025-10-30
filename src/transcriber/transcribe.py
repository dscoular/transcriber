#!/usr/bin/env python
"""
Transcribe video files to SRT subtitle text files using a pre-trained model.

**Author:** Doug Scoular<br>
**Date:**   2025-09-16<br>
**Email:**  dscoular@gmail.com<br>

**License:** MIT

The main class that does all the work is **Transcribe** it employs
an instance of the **FileFilter** class to find the video files it is going to
process and turn into SRT subtitle text files.

**Requirements:** *(see pyproject.toml for versions)*:

- whisper (openai/whisper)
- pysrt
- numpy
- AudioSegment (pydub)
- ffmpeg (for audio decoding, must be installed separately into the Operating System)
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pysrt
import whisper
from pydub import AudioSegment

__VERSION__ = "1.0.0"


class FileFilter:
    """
    A class which recursively searches the given input_path filtering files it finds
    based on a matching filename "suffix" e.g. .mp4 combined with "include" and "exclude"
    rglob patterns.

    Examples:
        >>> # Instantiating our FileFilter instance and obtaining matching files.
        >>> filter = FileFilter(Path('.'),
        ...                     '.mp4',
        ...                     include_patterns=['**/*.mp4'],
        ...                     exclude_patterns=['**/exclude_this.mp4'])
        >>> matching_files = filter.get_matching_files()
        >>> for file in matching_files:
        >>>     print(file)
        foo.mp4
        bar.mp4

    Args:
        input_path (Path): The root directory to scan for files.
        suffix (Optional[str]): The file suffix to filter by (defaults to '.mp4').
        include_patterns (Optional[list[str]]): List of glob patterns to include.
        exclude_patterns (Optional[list[str]]): List of glob patterns to exclude.
    """

    def __init__(
        self,
        input_path: Path,
        suffix: str | None = ".mp4",
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ):
        self.input_path = input_path.resolve()
        self.suffix = suffix
        # If the user provides no include patterns, the default is to find
        # all files with the given suffix, recursively.
        # First, remove any empty, duplicate patterns. Our argument parsing should have already handled this,
        self.include_patterns = sorted({pattern for pattern in include_patterns or [] if pattern})
        self.exclude_patterns = sorted({pattern for pattern in exclude_patterns or [] if pattern})
        # Use the default include pattern if none provided.
        self.include_patterns = include_patterns or [f"**/*{self.suffix}"]
        # If no exclude patterns are provided, default to an empty list.
        self.exclude_patterns = exclude_patterns or []

    def get_matching_files(self) -> list[Path]:
        """
        Recursively Scans the self.input_path directory using
        rglob patterns and returns a list of all files that match our
        FileFilter instance's criteria (suffix, include_patterns and
        exclude_patterns).

        Returns:
            A sorted list of Path objects matching the filter criteria.
        """
        included_files: set[Path] = set()
        for pattern in self.include_patterns:
            # Path.glob with '**' handles recursive search automatically.
            # This correctly interprets patterns like '**/*.mkv'.
            for file in self.input_path.glob(pattern):
                if file.is_file():
                    included_files.add(file)

        excluded_files: set[Path] = set()
        for pattern in self.exclude_patterns:
            for file in self.input_path.glob(pattern):
                if file.is_file():
                    excluded_files.add(file)

        # The final set of files is the difference between the two sets.
        matching_files = sorted(included_files - excluded_files)

        print(f"We matched {len(matching_files)} files.")
        if excluded_files:
            print("The following files were explicitly excluded by your exclude rules:")
            for excluded_file in sorted(excluded_files):
                print(f"  EXCLUDED: [{excluded_file}]")

        return matching_files


class Transcriber:
    """
    A class to handle transcription of video files to SRT subtitle text files
    using an OpenAI/Whisper pre-trained model. Takes our parsed command-line
    arguments to instantiate an instance which we can then use to
    transcribe videos to text.

    Examples:
        >>> # Manually create our arguments namespace.
        >>> my_args = argparse.Namespace(input_path='/tmp/Bonsai_Tutorials')
        >>> my_args.model = 'base.en' # Choose the smallest transcription model.
        >>> my_args.force = True  # Force overwriting existing ".srt" files.
        >>> my_args.suffix = '.mp4'  # Only consider ".mp4" files.
        >>> # Include "rglob" patterns we are interested in.
        >>> my_args.include = ['**/001000_20250218_1337 - moving objects and setting a few preferences.mp4']
        >>> # Exclude "rglob" patterns we don't want to process.
        >>> my_args.excluded = ['**/skip_this.mp4']
        >>> my_args.dry_run = False  # Actually process the files.
        >>> my_args.interactive = False #  Don't interactively prompt the user.
        >>> # Instantiate our Transcriber instance with our arguments.
        >>> transcriber = Transcriber(my_args)
        >>> # Start the transcription process.
        >>> transcriber.videos_to_text()
        We matched 1 files.
        PROCESSING: /tmp/Bonsai_Tutorials/001000_20250218_1337 - moving objects and setting a few preferences/001000_20250218_1337 - moving objects and setting a few preferences.mp4 -> /tmp/Bonsai_Tutorials/001000_20250218_1337 - moving objects and setting a few preferences/001000_20250218_1337 - moving objects and setting a few preferences.srt...
        SUCCESS: Transcription saved to [/tmp/Bonsai_Tutorials/001000_20250218_1337 - moving objects and setting a few preferences/001000_20250218_1337 - moving objects and setting a few preferences.srt]
        Transcription completed for all files.

    Args:
        args: Parsed command-line arguments.
    """  # noqa: E501

    # Instance variables with types (Python 3.6+ allows this)
    force: bool
    input_path: Path
    model: Any  # The whisper model type is not explicitly defined.
    suffix: str
    filter: FileFilter

    def __init__(self, args: argparse.Namespace) -> None:
        self.input_path = Path(args.input_path).expanduser()
        self.force = args.force
        self.model = args.model
        self.suffix = args.suffix
        self.dry_run = args.dry_run
        self.filter = FileFilter(self.input_path, self.suffix, args.include, args.exclude)

    def transcribe(self, input_file: Path) -> dict[str, Any] | None:
        """
        Transcribe the audio from the given video input file and returns a dictionary of
        transcribed text and other relevant metadata. We return None if the transcription fails.

        Examples:
            >>> # Transcribe our video to our dictionary of subtitle metadata.
            >>> srt_metadata = transcriber.transcribe("/path/to/video.mp4")
            >>> pp srt_metadata
            {
              'language': 'en',
              'segments': [{'avg_logprob': -0.18892038023317015,
               'compression_ratio': 1.5515463917525774,
               'end': 6.28,
               'id': 0,
               'no_speech_prob': 0.09762045741081238,
               'seek': 0,
               'start': 0.0,
               'temperature': 0.0,
               'text': ' Welcome to Vanilla Blender. I figured before we get into Bonsai we can go'
               ...
            }

        Args:
            input_file: The root directory to scan for files.
        Returns:
            A dictionary with a dictionary of transcription results, or None on failure.
        """
        try:
            # pydub will internally use ffmpeg if it's available
            # It will try to decode the MP4 directly.
            # You might need to specify the format if pydub can't guess from the extension.
            audio_segment: Any = AudioSegment.from_file(str(input_file))

            # Crucially, ensure the audio is 16kHz, mono
            # Whisper typically expects 16kHz mono float32
            audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)

            audio_data: np.ndarray = np.frombuffer(audio_segment.get_array_of_samples(), dtype=np.int16)

            # Convert to float32 and normalize
            audio_data_float: np.ndarray = audio_data.astype(np.float32) / 32768.0

            # Use whisper's transcribe method to get the transcription model.
            model = whisper.load_model(self.model)
            result: dict[str, Any] = model.transcribe(audio_data_float, fp16=False)
        except (FileNotFoundError, ValueError, TypeError) as e:
            # Catch known potential errors.
            print(f"ERROR: skipping [{input_file}]: {e}")
            return None  # Skip this file on known errors.
        # Return our transcribe() result.
        return result

    def videos_to_text(self) -> None:
        """
        Convert video files in the input path to audio and transcribe them to SRT text files
        based on the arguments given when we instantiated our Transcriber class.
        """
        # Enumerate our input files.
        for input_filename in sorted(self.filter.get_matching_files()):
            if self.dry_run:
                print(f"DRY RUN ENABLED, skipping actual transcription of [{input_filename}]")
                continue
            # Are we likely to overwrite an existing .srt file?
            output_srt_file = input_filename.with_suffix(".srt")
            if not self.force and output_srt_file.exists():
                print(
                    f"SKIPPING: Transcription for [{input_filename}] already exists "
                    f"as [{output_srt_file}] (use --force to overwrite)."
                )
                continue

            print(f"PROCESSING: {input_filename} -> {output_srt_file}...")
            transcription: dict[str, Any] | None = None
            try:
                transcription = self.transcribe(input_filename)
            except IndexError as err:
                print(f"ERROR: Skipping [{input_filename}] due to [{err}]")
                continue
            if transcription:
                # Create a SubRipFile object to hold the subtitles.
                subs = pysrt.SubRipFile()
                for i, segment in enumerate(transcription["segments"]):
                    start_time_ms = int(segment["start"] * 1000)
                    end_time_ms = int(segment["end"] * 1000)
                    text = segment["text"].strip()

                    # Create SubRipTime objects.
                    start_time = pysrt.SubRipTime(milliseconds=start_time_ms)
                    end_time = pysrt.SubRipTime(milliseconds=end_time_ms)

                    # Create a SubRipItem and add it to the file.
                    sub = pysrt.SubRipItem(index=i + 1, start=start_time, end=end_time, text=text)
                    subs.append(sub)

                # Save the SRT file.
                subs.save(output_srt_file, encoding="utf-8")

                print(f"SUCCESS: Transcription saved to [{output_srt_file}]")
            else:
                print(f"ERROR: Empty transcribe() return value: [{input_filename}]")

        print("Transcription completed for all files.")


def validate_dot_suffix(value: str) -> str:
    """
    A custom argparse type that ensures the value is a string
    starting with a dot '.'.

    Args:
        value: The input string to validate.

    Returns:
        The validated suffix string.

    Raises:
        argparse.ArgumentTypeError: If the value is invalid.
    """
    if not isinstance(value, str) or not value.startswith("."):
        # This specific exception is caught by argparse and printed
        # to the user as a clean error message.
        print(f"invalid suffix: '{value}' (must start with a '.')")
        raise argparse.ArgumentTypeError()
    return value


def parse_and_prompt_arguments(args: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments and prompt for a subset of missing ones if in interactive mode.
    We don't bother prompting for "include" or "exclude" arguments since we would encourage
    you to learn to use the command-line arguments for more advance usage.

    Args:
        args: List of command-line arguments to parse.


    Returns:
        The parsed command-line arguments.

    Raises:
        SystemExit: If version is requested or invalid input is provided.

    """
    # Define the full set of arguments
    full_parser = argparse.ArgumentParser(description="Transcribe audio files using a pre-trained model.")
    full_parser.add_argument(
        "--dry-run", "-n", action="store_true", help="Try a dry run without any actual transcription."
    )
    full_parser.add_argument(
        "--include",
        type=str,
        nargs="*",
        help="A list of files or rglob patterns to include when processing. Defaults to **/*.mp4.",
    )
    full_parser.add_argument(
        "--exclude",
        type=str,
        nargs="*",
        help="A list of files or rglob patterns to exclude from processing (overrides the include list).",
    )
    full_parser.add_argument("--force", action="store_true", help="Force overwrite of existing output SRT files.")
    full_parser.add_argument(
        "--input-path", type=str, help="Directory containing input audio files (required in non-interactive mode)."
    )
    full_parser.add_argument(
        "--suffix", type=validate_dot_suffix, default=".mp4", help="Suffix of audio files to process (default: .mp4)."
    )
    # List of available Whisper models
    english_only_models_list = sorted([model for model in whisper._MODELS if model.endswith(".en")])
    english_only_models_str = ", ".join(english_only_models_list)
    full_parser.add_argument(
        "--model",
        type=str,
        default="base.en",
        choices=english_only_models_list,
        help=f"Pre-trained model to use (default: base.en, available {english_only_models_str}).",
    )
    full_parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode, prompting for missing arguments."
    )
    full_parser.add_argument("--version", "-v", action="store_true", help="Show program's version number and exit.")

    # First pass: Check for --interactive flag or no arguments
    first_parser = argparse.ArgumentParser(add_help=False)
    first_parser.add_argument("--interactive", action="store_true")
    first_args, unknown_args = first_parser.parse_known_args(args)

    # Case 1: No arguments supplied OR --interactive flag is present.
    if not unknown_args or first_args.interactive:
        # Parse arguments provided on the command line first
        # This will set the values for any args that *were* provided,
        # and leave others as their default or None.
        parsed_args = full_parser.parse_args(args=unknown_args)
        if parsed_args.version:
            # Special handling for version in interactive mode.
            print(f"transcribe version: {__VERSION__}")
            sys.exit()

        # Now enter interactive mode.
        print("Entering interactive mode. Please provide the required information.")

        # Prompt for missing arguments.
        if parsed_args.input_path is None:
            input_path = input("Enter the directory with videos (default: .): ").strip() or "."
            parsed_args.input_path = input_path

        # Enumerate include/exclude patterns to remove empties and duplicates.
        parsed_args.exclude = sorted({pattern for pattern in parsed_args.exclude or [] if pattern})
        parsed_args.include = sorted({pattern for pattern in parsed_args.include or [] if pattern})

        # The other arguments have defaults, but you can still ask for
        # confirmation or allow changes.
        print(f"\nCurrent settings for transcribe version {__VERSION__}:")
        print(f"  Suffix: {parsed_args.suffix}")
        print(f"  Model: {parsed_args.model}")
        print(f"  Force overwrite: {'Yes' if parsed_args.force else 'No'}")
        print(f"  Dry run: {'Yes' if parsed_args.dry_run else 'No'}")
        print(f"  Excluded patterns: ({', '.join(parsed_args.exclude) if parsed_args.exclude else 'None'})")
        print(f"  Include patterns: ({', '.join(parsed_args.exclude) if parsed_args.include else 'None'})")
        print("\nYou will now be prompted for any changes to these settings.")

        # Prompt for changes to defaulted arguments.
        # Ask the user if they want to change the suffix.
        suffix = input(f"Enter suffix to process (or press Enter to keep '{parsed_args.suffix}'): ").strip()
        # No suffix given, use our default.
        if not suffix:
            suffix = ".mp4"
        parsed_args.suffix = validate_dot_suffix(suffix)
        # Ask the user if they want to change the Whisper model.
        model = input(
            f"Enter model to use (or press Enter to keep '{parsed_args.model}', available {english_only_models_str}): "
        ).strip()
        parsed_args.model = model or "base.en"
        # Perform validation on interactive model input, ignoring case.
        if parsed_args.model not in english_only_models_list:
            print("Invalid model selected. Exiting...")
            sys.exit(1)  # Barf...
        # Ask the user if they want to force overwriting of existing SRT files.
        force = (
            input(f"Force overwrite of existing SRT files? (y/N, default: {'Y' if parsed_args.force else 'N'}): ")
            .strip()
            .lower()
        )
        if force == "y":
            parsed_args.force = True
        # Ask the user if they want to perform a "dry run" where no SRT files are written.
        dry_run = input(f"Enable dry run mode? (y/N, default: {'Y' if parsed_args.dry_run else 'N'}): ").strip().lower()
        if dry_run == "y":
            parsed_args.dry_run = True

        # Confirm the user's changes.
        print(f"\nConfirm settings for transcribe version {__VERSION__}:")
        print(f"  Suffix: {parsed_args.suffix}")
        print(f"  Model: {parsed_args.model}")
        print(f"  Force overwrite: {'Yes' if parsed_args.force else 'No'}")
        print(f"  Dry run: {'Yes' if parsed_args.dry_run else 'No'}")
        print(f"  Excluded patterns: ({', '.join(parsed_args.exclude) if parsed_args.exclude else 'None'})")
        print(f"  Include patterns: ({', '.join(parsed_args.exclude) if parsed_args.include else 'None'})")
        print("\nHit Enter to continue, or Ctrl-C to abort.")
        input()

        return parsed_args

    else:
        # Case 2: Arguments supplied, and not interactive mode.
        parsed_args = full_parser.parse_args(unknown_args)
        # Special handling for version in non-interactive mode.
        if parsed_args.version:
            print(f"transcribe version: {__VERSION__}")
            sys.exit()
        return parsed_args


def main(args: list[str] | None = None) -> None:
    """
    Main function to run the transcriber.

    Args:
        args (Optional[list[str]]): List of command-line arguments to parse.
    """
    # Parse command-line arguments, prompting if needed.
    parsed_args: argparse.Namespace = parse_and_prompt_arguments(args)
    # Create a Transcriber instance and run the transcription.
    transcriber: Transcriber = Transcriber(parsed_args)
    # Start the transcription process.
    transcriber.videos_to_text()


# Entry point for script execution.
if __name__ == "__main__":
    main()
