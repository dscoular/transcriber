import argparse
import array
import builtins
import contextlib
import runpy
import sys
from pathlib import Path

import numpy as np
import pysrt
import pytest
from pydub import AudioSegment

from transcriber.transcribe import __VERSION__, FileFilter, Transcriber, main


# Place this at the top of your tests/test_transcribe.py or a shared test utilities file
class NoMoreTestInputsError(Exception):
    """Raised when the simulated input stream is exhausted."""

    def __init__(self, message="No more input values available"):
        super().__init__(message)


class TestFileFilter:
    """
    Tests for the glob-based FileFilter class.
    """

    def test_default_include_finds_all_suffix(self, file_structure: Path, TEST_FILES: list[str]):
        """
        Test the default behavior: finds all '.mp4' files recursively.
        """
        ff = FileFilter(file_structure, ".mp4")
        files = ff.get_matching_files()
        assert sorted([f.name for f in files]) == sorted([
            Path(file).name for file in TEST_FILES if file.endswith(".mp4")
        ])

    def test_explicit_recursive_include(self, file_structure: Path):
        """
        Test user-provided recursive glob like '**/*.mkv'.
        """
        ff = FileFilter(file_structure, ".mkv", include_patterns=["**/*.mkv"])
        files = ff.get_matching_files()
        assert sorted([f.name for f in files]) == ["dummy test 1.mkv", "dummy test 2.mkv"]

    def test_specific_include_pattern(self, file_structure: Path):
        """
        Test including files only from a specific directory.
        """
        ff = FileFilter(file_structure, ".mp4", include_patterns=["**/_Model/Animation/*.mkv"])
        files = ff.get_matching_files()
        assert [f.name for f in files] == ["dummy test 1.mkv"]

    def test_exclude_pattern(self, file_structure: Path, TEST_FILES: list[str]):
        """
        Test that exclusion patterns correctly filter files.
        """
        ff = FileFilter(file_structure, ".mp4", exclude_patterns=["**/*.mkv"])
        files = ff.get_matching_files()
        assert sorted([f.name for f in files]) == sorted([
            Path(file).name for file in TEST_FILES if file.endswith(".mp4")
        ])

    def test_exclude_overrides_include(self, file_structure: Path):
        """
        Test that exclusion rules always take precedence.
        """
        ff = FileFilter(
            file_structure,
            ".mp4",
            include_patterns=["**/*.mp4"],
            exclude_patterns=["**/final video.mp4"],
        )
        files = ff.get_matching_files()
        assert "final video.mp4" not in sorted([f.name for f in files])


class TestTranscriber:
    """
    Tests for the Transcriber class and main function.
    """

    def test_videos_to_text_processes_files(
        self, mock_args: argparse.Namespace, mock_whisper_loader, file_structure: Path, mocker: pytest.MonkeyPatch
    ):
        """
        Test that videos_to_text processes the correct number of files.
        """
        mock_args.input_path = str(file_structure)
        transcriber = Transcriber(mock_args)

        # Mock the instance's transcribe method to check the loop logic
        mocker.patch.object(transcriber, "transcribe", return_value={"segments": []})

        transcriber.videos_to_text()

        # Should be called for the 126 .mp4 files found by the filter
        assert transcriber.transcribe.call_count == 126

    @pytest.mark.parametrize("option", ("-h", "--help"))
    def test_help(self, capsys, option, help_text, monkeypatch, clean_transcriber_module):
        """
        Test that help option displays the correct help text.
        """
        # Act like we're running from command line.
        monkeypatch.setattr(sys, "argv", ["transcribe.py", option])
        with contextlib.suppress(SystemExit):
            # Run module as __main__
            runpy.run_module("transcriber.transcribe", run_name="__main__")

        output = capsys.readouterr().out
        # Did we get the expected help text?
        assert output == help_text

    @pytest.mark.parametrize("option", ("-v", "--version"))
    def test_version(self, capsys, option, monkeypatch, clean_transcriber_module):
        """
        Test that version option displays the correct version text.
        """
        # Act like we're running from command line.
        monkeypatch.setattr(sys, "argv", ["transcribe.py", option])
        with contextlib.suppress(SystemExit):
            # Run module as __main__
            runpy.run_module("transcriber.transcribe", run_name="__main__")
        output = capsys.readouterr().out
        # Did we get the expected version text?
        assert output == f"transcribe version: {__VERSION__}\n"

    def test_bad_suffix(self, capsys, monkeypatch, clean_transcriber_module):
        """
        Test that a bad suffix, like one without a leading dot, is handled properly.
        """
        # Act like we're running from command line.
        monkeypatch.setattr(sys, "argv", ["transcribe.py", "--suffix", "mp4"])
        with contextlib.suppress(SystemExit):
            # Run module as __main__
            runpy.run_module("transcriber.transcribe", run_name="__main__")
        output = capsys.readouterr().out
        # Did we get the expected version text?
        assert output == "invalid suffix: 'mp4' (must start with a '.')\n"

    def test_version_overrides_interactive(self, capsys, monkeypatch, clean_transcriber_module):
        """
        Test that version option prints and exits overriding the interactive option.
        """
        # Act like we're running from command line.
        monkeypatch.setattr(sys, "argv", ["transcribe.py", "--version", "--interactive"])
        with contextlib.suppress(SystemExit):
            # Run module as __main__
            runpy.run_module("transcriber.transcribe", run_name="__main__")
        output = capsys.readouterr().out
        # Did we get the expected version text?
        assert output == f"transcribe version: {__VERSION__}\n"

    def test_transcribe(self, capsys, mocker, monkeypatch, file_structure: Path):
        """
        Test that main method calls the whisper model's transcribe method.
        """
        # sample int16 data
        samples = np.array([0, 1000, -1000, 32767, -32768], dtype=np.int16)
        arr = array.array("h", samples.tolist())  # 'h' = signed short (int16)

        # fake AudioSegment instance
        fake_segment = mocker.MagicMock()
        fake_segment.set_frame_rate.return_value = fake_segment
        fake_segment.set_channels.return_value = fake_segment
        fake_segment.get_array_of_samples.return_value = arr

        # patch AudioSegment.from_file to return fake_segment.
        monkeypatch.setattr(AudioSegment, "from_file", lambda _: fake_segment)

        # Create our fake return value for the transcribe method.
        fake_transcription = {
            "segments": [
                {"start": 0.0, "end": 5.0, "text": "This is a test transcription."},
                {"start": 5.0, "end": 10.0, "text": "The transcription should be realistic."},
            ]
        }
        # Create a return value for the mock model's transcribe method.
        mock_model = mocker.Mock()
        mock_model.transcribe.return_value = fake_transcription

        # Patch the whisper.load_model to return our mock model.
        mocker.patch("whisper.load_model", return_value=mock_model)

        with contextlib.suppress(SystemExit):
            main(["--input-path", str(file_structure), "--suffix", ".mkv", "--force"])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Set our expectations.
        expected = "We matched 2 files.\nPROCESSING"
        great_expectations = ("test 1.mkv", "test 2.mkv", "test 1.srt", "test 2.srt")
        assert all(file in output for file in great_expectations)
        assert expected in output
        assert "Transcription completed for all files" in output

    def test_transcribe_dry_run(self, capsys, mocker, monkeypatch, file_structure: Path):
        """
        Test that transcribe method doesn't call the whisper model's transcribe method
        when dry run is enabled.
        """
        # sample int16 data
        samples = np.array([0, 1000, -1000, 32767, -32768], dtype=np.int16)
        arr = array.array("h", samples.tolist())  # 'h' = signed short (int16)

        # fake AudioSegment instance
        fake_segment = mocker.MagicMock()
        fake_segment.set_frame_rate.return_value = fake_segment
        fake_segment.set_channels.return_value = fake_segment
        fake_segment.get_array_of_samples.return_value = arr

        # patch AudioSegment.from_file to return fake_segment.
        # mocker.patch("transcriber.transcribe.AudioSegment.from_file", return_value=fake_segment)
        monkeypatch.setattr(AudioSegment, "from_file", lambda _: fake_segment)

        with contextlib.suppress(SystemExit):
            main(["--input-path", str(file_structure), "--dry-run"])
        output = capsys.readouterr().out
        assert "We matched 126 files.\nDRY RUN ENABLED" in output
        assert "Transcription completed for all files" in output

    def test_interactive_prompting(self, capsys, mocker, monkeypatch, file_structure: Path):
        """
        Test that interactive prompting works as expected.
        """
        # Simulate user inputs for prompts.
        inputs = iter([
            str(file_structure),  # Video files input path.
            ".mkv",  # File suffix.
            "medium.en",  # Model name.
            "n",  # Force overwrite.
            "",  # Simulates hitting Enter to select the NO dry run default.
            "",  # Simulates hitting Enter to continue.
        ])

        original_input = builtins.input

        def fake_input(prompt=""):
            if prompt.startswith("(Pdb)"):
                return original_input(prompt)  # allow pdb to work
            else:
                try:
                    return next(inputs)
                except StopIteration as e:
                    # Handle the case where inputs is exhausted
                    raise NoMoreTestInputsError from e

        # When input() is called use our fake_input function
        # which returns predefined responses and allows pdb to function.
        monkeypatch.setattr(builtins, "input", fake_input)

        # sample int16 data
        samples = np.array([0, 1000, -1000, 32767, -32768], dtype=np.int16)
        arr = array.array("h", samples.tolist())  # 'h' = signed short (int16)

        # fake AudioSegment instance
        fake_segment = mocker.MagicMock()
        fake_segment.set_frame_rate.return_value = fake_segment
        fake_segment.set_channels.return_value = fake_segment
        fake_segment.get_array_of_samples.return_value = arr

        # patch AudioSegment.from_file to return fake_segment.
        # mocker.patch("transcriber.transcribe.AudioSegment.from_file", return_value=fake_segment)
        monkeypatch.setattr(AudioSegment, "from_file", lambda _: fake_segment)

        # Create our fake return value for the transcribe method.
        fake_transcription = {
            "segments": [
                {"start": 0.0, "end": 5.0, "text": "This is a test transcription."},
                {"start": 5.0, "end": 10.0, "text": "The transcription should be realistic."},
            ]
        }
        # Create a return value for the mock model's transcribe method.
        mock_model = mocker.Mock()
        mock_model.transcribe.return_value = fake_transcription

        # Patch the whisper.load_model to return our mock model.
        mocker.patch("whisper.load_model", return_value=mock_model)
        with contextlib.suppress(SystemExit):
            main(args=[])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Set our expectations.
        expected = (
            "Entering interactive mode. Please provide the required information.\n"
            "\n"
            "Current settings for transcribe version 1.0.0:\n"
            "  Suffix: .mp4\n"
            "  Model: base.en\n"
            "  Force overwrite: No\n"
            "  Dry run: No\n"
            "  Excluded patterns: (None)\n"
            "  Include patterns: (None)\n"
            "\n"
            "You will now be prompted for any changes to these settings.\n"
            "\n"
            "Confirm settings for transcribe version 1.0.0:\n"
            "  Suffix: .mkv\n"
            "  Model: medium.en\n"
            "  Force overwrite: No\n"
            "  Dry run: No\n"
            "  Excluded patterns: (None)\n"
            "  Include patterns: (None)\n"
            "\n"
            "Hit Enter to continue, or Ctrl-C to abort.\n"
            "We matched 2 files.\n"
            "PROCESSING"
        )
        great_expectations = ("test 1.mkv", "test 2.mkv", "test 1.srt", "test 2.srt")
        assert all(file in output for file in great_expectations)
        assert expected in output
        assert "Transcription completed for all files" in output

    def test_interactive_prompting_dry_run(self, capsys, mocker, monkeypatch, file_structure: Path):
        """
        Test that interactive prompting works as expected in a dry run.
        """
        # Simulate user inputs for prompts.
        inputs = iter([
            str(file_structure),  # Video files input path.
            ".mkv",  # File suffix.
            "medium.en",  # Model name.
            "n",  # Force overwrite.
            "y",  # Dry run.
            "",  # Apparently, input will use this as if Enter was pressed.
        ])

        original_input = builtins.input

        def fake_input(prompt=""):
            if prompt.startswith("(Pdb)"):
                return original_input(prompt)  # allow pdb to work
            else:
                try:
                    return next(inputs)
                except StopIteration as e:
                    # Handle the case where inputs is exhausted
                    raise NoMoreTestInputsError from e

        # When input() is called use our fake_input function
        # which returns predefined responses and allows pdb to function.
        monkeypatch.setattr(builtins, "input", fake_input)

        with contextlib.suppress(SystemExit):
            main(args=[])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Set our expectations.
        expected = (
            "Entering interactive mode. Please provide the required information.\n"
            "\n"
            "Current settings for transcribe version 1.0.0:\n"
            "  Suffix: .mp4\n"
            "  Model: base.en\n"
            "  Force overwrite: No\n"
            "  Dry run: No\n"
            "  Excluded patterns: (None)\n"
            "  Include patterns: (None)\n"
            "\n"
            "You will now be prompted for any changes to these settings.\n"
            "\n"
            "Confirm settings for transcribe version 1.0.0:\n"
            "  Suffix: .mkv\n"
            "  Model: medium.en\n"
            "  Force overwrite: No\n"
            "  Dry run: Yes\n"
            "  Excluded patterns: (None)\n"
            "  Include patterns: (None)\n"
            "\n"
            "Hit Enter to continue, or Ctrl-C to abort.\n"
            "We matched 2 files.\n"
            "DRY RUN ENABLED, skipping actual transcription of "
        )
        expected_file_1 = "test 1.mkv]\n"
        expected_file_2 = "test 2.mkv]\n"

        assert expected in output
        assert expected_file_1 in output
        assert expected_file_2 in output
        assert "Transcription completed for all files" in output

    def test_incorrect_interactive_prompting(self, capsys, mocker, monkeypatch, file_structure: Path):
        """
        Test that interactive prompting handles incorrect model input.
        """
        # Simulate incorrect interactive user inputs for model.
        inputs = iter([
            str(file_structure),  # Video files input path.
            ".mkv",  # File suffix.
            "foobar.en",  # Model name.
            "n",  # Force overwrite.
            "y",  # Dry run.
            "",  # Apparently, input will use this as if Enter was pressed.
        ])

        original_input = builtins.input

        def fake_input(prompt=""):
            if prompt.startswith("(Pdb)"):
                return original_input(prompt)  # allow pdb to work
            else:
                try:
                    return next(inputs)
                except StopIteration as e:
                    # Handle the case where inputs is exhausted
                    raise NoMoreTestInputsError from e

        # When input() is called use our fake_input function
        # which returns predefined responses and allows pdb to function.
        monkeypatch.setattr(builtins, "input", fake_input)
        with contextlib.suppress(SystemExit):
            main(args=[])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Set our expectations.
        expected = (
            "Entering interactive mode. Please provide the required information.\n"
            "\n"
            "Current settings for transcribe version 1.0.0:\n"
            "  Suffix: .mp4\n"
            "  Model: base.en\n"
            "  Force overwrite: No\n"
            "  Dry run: No\n"
            "  Excluded patterns: (None)\n"
            "  Include patterns: (None)\n"
            "\n"
            "You will now be prompted for any changes to these settings.\n"
            "Invalid model selected. Exiting...\n"
        )
        assert expected in output

    def test_videos_to_text_skips_existing_files(
        self, mock_args: argparse.Namespace, file_structure: Path, mocker: pytest.MonkeyPatch, capsys
    ):
        """
        Test that our videos_to_text() method skips transcription if output SRT already exists and force is False.
        """
        mock_args.input_path = str(file_structure)
        mock_args.force = False  # Ensure force is False
        transcriber = Transcriber(mock_args)

        # Mock get_matching_files to return a single dummy file
        dummy_mp4_file = file_structure / "videos" / "dummy_video.mp4"
        mocker.patch.object(transcriber.filter, "get_matching_files", return_value=[dummy_mp4_file])

        # Mock Path.exists for the expected SRT file to return True
        # This will make output_srt_file.exists() return True
        mocker.patch.object(Path, "exists", return_value=True)

        # Mock the transcribe method to ensure it's NOT called
        mock_transcribe = mocker.patch.object(transcriber, "transcribe")

        transcriber.videos_to_text()

        # Assert that transcribe was NOT called
        mock_transcribe.assert_not_called()

        # Capture output and check for the skipping message
        output = capsys.readouterr().out
        expected_skip_msg = (
            f"SKIPPING: Transcription for [{dummy_mp4_file}] already exists as [{dummy_mp4_file.with_suffix('.srt')}]"
        )
        assert expected_skip_msg in output
        assert "Transcription completed for all files." in output

    def test_videos_to_text_handles_indexerror_during_transcription(
        self, mock_args: argparse.Namespace, file_structure: Path, mocker: pytest.MonkeyPatch, capsys
    ):
        """
        Test that our videos_to_text() method handles IndexError during the transcribe call and continues.
        """
        mock_args.input_path = str(file_structure)
        mock_args.force = True  # Ensure force is True so it doesn't skip due to existing file
        transcriber = Transcriber(mock_args)

        # Mock get_matching_files to return a single dummy file
        dummy_mkv_file = file_structure / "videos" / "other_videos" / "dummy_video.mkv"
        mocker.patch.object(transcriber.filter, "get_matching_files", return_value=[dummy_mkv_file])

        # Mock Path.exists to return False, so it tries to transcribe
        mocker.patch.object(Path, "exists", return_value=False)

        # Mock the transcribe method to raise IndexError
        mock_transcribe = mocker.patch.object(transcriber, "transcribe", side_effect=IndexError("Mock index error"))

        # Mock pysrt.SubRipFile().save() to ensure it's not called
        mock_subs_save = mocker.patch.object(pysrt.SubRipFile, "save")

        transcriber.videos_to_text()

        # Assert that transcribe WAS called
        mock_transcribe.assert_called_once_with(dummy_mkv_file)

        # Assert that save was NOT called
        mock_subs_save.assert_not_called()

        # Capture output and check for the error message
        output = capsys.readouterr().out
        expected_error_msg = f"ERROR: Skipping [{dummy_mkv_file}] due to [Mock index error]"
        assert expected_error_msg in output
        assert "Transcription completed for all files." in output

    def test_videos_to_text_handles_empty_transcription_result(
        self, mock_args: argparse.Namespace, file_structure: Path, mocker: pytest.MonkeyPatch, capsys
    ):
        """
        Test that our videos_to_text() method handles a None return from transcribe() gracefully.
        """
        mock_args.input_path = str(file_structure)
        mock_args.force = True  # Ensure force is True
        transcriber = Transcriber(mock_args)

        # Mock get_matching_files to return a single dummy file
        dummy_mp4_file = file_structure / "videos" / "dummy_video.mp4"
        mocker.patch.object(transcriber.filter, "get_matching_files", return_value=[dummy_mp4_file])

        # Mock Path.exists to return False
        mocker.patch.object(Path, "exists", return_value=False)

        # Mock transcribe to return None
        mock_transcribe = mocker.patch.object(transcriber, "transcribe", return_value=None)

        # Mock pysrt.SubRipFile().save() to ensure it's not called
        mock_subs_save = mocker.patch.object(pysrt.SubRipFile, "save")

        transcriber.videos_to_text()

        # Assert that transcribe WAS called
        mock_transcribe.assert_called_once_with(dummy_mp4_file)

        # Assert that save was NOT called
        mock_subs_save.assert_not_called()

        # Capture output and check for the error message
        output = capsys.readouterr().out
        expected_error_msg = f"ERROR: Empty transcribe() return value: [{dummy_mp4_file}]"
        assert expected_error_msg in output
        assert "Transcription completed for all files." in output
