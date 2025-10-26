import argparse
import contextlib
import runpy
import sys
from pathlib import Path

import pysrt
import pytest

from transcriber.transcribe import __VERSION__, FileFilter, Transcriber, main


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
        Test including files only from a specific directory and ensuring directories are ignored.
        """
        # For badness, create a dummy directory that matches the glob file pattern.
        dummy_dir_path = file_structure / "Bonsai_Tutorials" / "_Model" / "Animation" / "dummy_folder.mkv"
        dummy_dir_path.mkdir(parents=True, exist_ok=True)  # Create it as a directory
        # Run our filter.
        ff = FileFilter(file_structure, ".mp4", include_patterns=["**/_Model/Animation/*.mkv"])
        files = ff.get_matching_files()
        assert [f.name for f in files] == ["dummy test 1.mkv"]
        assert dummy_dir_path not in files  # Explicitly confirm the directory is not included

    def test_exclude_pattern(self, file_structure: Path, TEST_FILES: list[str]):
        """
        Test that exclusion patterns correctly filter files.
        """
        # For badness, create a dummy directory that matches the glob file pattern.
        dummy_dir_path = file_structure / "Bonsai_Tutorials" / "_Model" / "Animation" / "dummy_folder.mkv"
        dummy_dir_path.mkdir(parents=True, exist_ok=True)  # Create it as a directory
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
        self, mocker, mock_args: argparse.Namespace, mock_transcription_deps, file_structure: Path
    ):
        """
        Test that videos_to_text processes the correct number of files.
        """
        mock_args.input_path = str(file_structure)

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        # Mock get_matching_files to return a list of 126 dummy .mp4 files
        transcriber = Transcriber(mock_args)
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

    def test_transcribe(self, capsys, mocker, monkeypatch, file_structure: Path, mock_transcription_deps):
        """
        Test that main method calls the whisper model's transcribe method.
        """
        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.
        with contextlib.suppress(SystemExit):
            main(["--input-path", str(file_structure), "--suffix", ".mkv", "--force"])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Define paths correctly, including the 'Bonsai_Tutorials' component
        file1_path = file_structure / "Bonsai_Tutorials" / "_Model" / "Animation" / "dummy test 1.mkv"
        file1_srt = file1_path.with_suffix(".srt")
        file2_path = file_structure / "Bonsai_Tutorials" / "_Model" / "Animation" / "jpgs" / "dummy test 2.mkv"
        file2_srt = file2_path.with_suffix(".srt")

        # Set our expectations, now with full and dynamic paths for exact match.
        great_expectations = (
            f"We matched 2 files.\n"
            f"PROCESSING: {file1_path} -> {file1_srt}...\n"
            f"SUCCESS: Transcription saved to [{file1_srt}]\n"
            f"PROCESSING: {file2_path} -> {file2_srt}...\n"
            f"SUCCESS: Transcription saved to [{file2_srt}]\n"
            f"Transcription completed for all files.\n"
        )
        assert output == great_expectations

    def test_transcribe_dry_run(self, capsys, file_structure: Path, mock_transcription_deps):
        """
        Test that transcribe method doesn't call the whisper model's transcribe method
        when dry run is enabled.
        """
        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        with contextlib.suppress(SystemExit):
            main(["--input-path", str(file_structure), "--dry-run"])
        output = capsys.readouterr().out
        assert "We matched 126 files.\nDRY RUN ENABLED" in output
        assert "Transcription completed for all files" in output

    def test_interactive_prompting(
        self,
        capsys,
        mocker,
        monkeypatch,
        file_structure: Path,
        mock_input,
        mock_transcription_deps,
        english_only_models_str,
    ):
        """
        Test that interactive prompting works as expected.
        """
        # Simulate user inputs for prompts.
        input_path_str = str(file_structure)  # Capture the path string once
        inputs = iter([
            input_path_str,  # Video files input path.
            ".mkv",  # File suffix.
            "medium.en",  # Model name.
            "n",  # Force overwrite.
            "",  # Simulates hitting Enter to select the NO dry run default.
            "",  # Simulates hitting Enter to continue.
        ])

        # Use the fixture to set the inputs for builtins.input().
        mock_input(inputs)

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        # Patch pysr.SubRipFile.save to avoid actual file writing.
        mocker.patch.object(pysrt.SubRipFile, "save")  # Mock saving SRT

        with contextlib.suppress(SystemExit):
            main(args=[])
        sys.stdout.flush()
        output = capsys.readouterr().out

        # Set our expectations.
        expected = (
            f"Entering interactive mode. Please provide the required information.\n"
            f"Enter the directory with videos (default: .): {input_path_str}\n"
            f"\n"  # This newline likely comes from the print before "Current settings"
            f"Current settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mp4\n"
            f"  Model: base.en\n"
            f"  Force overwrite: No\n"
            f"  Dry run: No\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Current settings" from "You will now be prompted".
            f"You will now be prompted for any changes to these settings.\n"
            f"Enter suffix to process (or press Enter to keep '.mp4'): .mkv\n"
            f"Enter model to use (or press Enter to keep 'base.en', available {english_only_models_str}): medium.en\n"
            f"Force overwrite of existing SRT files? (y/N, default: N): n\n"
            f"Enable dry run mode? (y/N, default: N): \n"
            f"\n"  # This newline separates the last prompt from "Confirm settings".
            f"Confirm settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mkv\n"
            f"  Model: medium.en\n"
            f"  Force overwrite: No\n"
            f"  Dry run: No\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Confirm settings" from "Hit Enter to continue".
            f"Hit Enter to continue, or Ctrl-C to abort.\n"
            f"\n"  # Newline for the final confirmation input
            f"We matched 2 files.\n"
            f"PROCESSING: {file_structure}/Bonsai_Tutorials/_Model/Animation/dummy test 1.mkv -> {file_structure}/Bonsai_Tutorials/_Model/Animation/dummy test 1.srt...\n"
            f"SUCCESS: Transcription saved to [{file_structure}/Bonsai_Tutorials/_Model/Animation/dummy test 1.srt]\n"
            f"PROCESSING: {file_structure}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.mkv -> {file_structure}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.srt...\n"
            f"SUCCESS: Transcription saved to [{file_structure}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.srt]\n"
            f"Transcription completed for all files.\n"
        )
        assert expected == output

    def test_interactive_prompting_dry_run(
        self, capsys, file_structure: Path, mock_input, mock_transcription_deps, english_only_models_str
    ):
        """
        Test that interactive prompting works as expected in a dry run.
        """
        # Simulate user inputs for prompts.
        input_path_str = str(file_structure)  # Capture the path string once
        inputs = iter([
            input_path_str,  # Video files input path.
            ".mkv",  # File suffix.
            "medium.en",  # Model name.
            "n",  # Force overwrite.
            "y",  # Dry run.
            "",  # Apparently, input will use this as if Enter was pressed.
        ])

        # Use the fixture to set the inputs for builtins.input().
        mock_input(inputs)

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        with contextlib.suppress(SystemExit):
            main(args=[])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Set our expectations.
        expected = (
            f"Entering interactive mode. Please provide the required information.\n"
            f"Enter the directory with videos (default: .): {input_path_str}\n"
            f"\n"  # This newline likely comes from the print before "Current settings"
            f"Current settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mp4\n"
            f"  Model: base.en\n"
            f"  Force overwrite: No\n"
            f"  Dry run: No\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Current settings" from "You will now be prompted".
            f"You will now be prompted for any changes to these settings.\n"
            f"Enter suffix to process (or press Enter to keep '.mp4'): .mkv\n"
            f"Enter model to use (or press Enter to keep 'base.en', available {english_only_models_str}): medium.en\n"
            f"Force overwrite of existing SRT files? (y/N, default: N): n\n"
            f"Enable dry run mode? (y/N, default: N): y\n"
            f"\n"  # This newline separates the last prompt from "Confirm settings".
            f"Confirm settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mkv\n"
            f"  Model: medium.en\n"
            f"  Force overwrite: No\n"
            f"  Dry run: Yes\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Confirm settings" from "Hit Enter to continue".
            f"Hit Enter to continue, or Ctrl-C to abort.\n"
            f"\n"  # Newline for the final confirmation input
            f"We matched 2 files.\n"
            f"DRY RUN ENABLED, skipping actual transcription of [{file_structure}/Bonsai_Tutorials/_Model/Animation/dummy test 1.mkv]\n"
            f"DRY RUN ENABLED, skipping actual transcription of [{file_structure}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.mkv]\n"
            f"Transcription completed for all files.\n"
        )

        assert expected == output

    def test_interactive_prompting_force_true(
        self, capsys, mocker, file_structure: Path, mock_input, mock_transcription_deps, english_only_models_str
    ):
        """
        Test that interactive prompting correctly sets the --force option to True.
        """
        # Simulate user inputs for prompts.
        input_path_str = str(file_structure)  # Capture the path string once
        inputs = iter([
            input_path_str,  # Video files input path.
            ".mkv",  # We'll test transcription of just the two mkv files.
            "",  # Keep default model (base.en).
            "y",  # Set Force overwrite to 'y' (True).
            "n",  # Set Dry run to 'n' (False).
            "",  # Simulate hitting Enter to continue.
        ])

        # Use the fixture to set the inputs for builtins.input().
        mock_input(inputs)

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        # Patch Path.exists to always return False to give a clear path to transcription.
        mocker.patch.object(Path, "exists", return_value=False)  # Prevent skipping based on existing SRT
        # Patch pysr.SubRipFile.save to avoid actual file writing.
        mocker.patch.object(pysrt.SubRipFile, "save")  # Mock saving SRT

        with contextlib.suppress(SystemExit):
            main(args=["--interactive"])  # Explicitly enter interactive mode
        sys.stdout.flush()
        output = capsys.readouterr().out

        # More great expectations.
        great_expectations = (
            f"Entering interactive mode. Please provide the required information.\n"
            f"Enter the directory with videos (default: .): {input_path_str}\n"
            f"\n"  # This newline likely comes from the print before "Current settings"
            f"Current settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mp4\n"
            f"  Model: base.en\n"
            f"  Force overwrite: No\n"
            f"  Dry run: No\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Current settings" from "You will now be prompted".
            f"You will now be prompted for any changes to these settings.\n"
            f"Enter suffix to process (or press Enter to keep '.mp4'): .mkv\n"
            f"Enter model to use (or press Enter to keep 'base.en', available {english_only_models_str}): \n"
            f"Force overwrite of existing SRT files? (y/N, default: N): y\n"
            f"Enable dry run mode? (y/N, default: N): n\n"
            f"\n"  # This newline separates the last prompt from "Confirm settings".
            f"Confirm settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mkv\n"
            f"  Model: base.en\n"
            f"  Force overwrite: Yes\n"
            f"  Dry run: No\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Confirm settings" from "Hit Enter to continue".
            f"Hit Enter to continue, or Ctrl-C to abort.\n"
            f"\n"  # Newline for the final confirmation input
            f"We matched 2 files.\n"
            "PROCESSING: "
            f"{input_path_str}/Bonsai_Tutorials/_Model/Animation/dummy test 1.mkv -> "
            f"{input_path_str}/Bonsai_Tutorials/_Model/Animation/dummy test 1.srt...\n"
            "SUCCESS: Transcription saved to "
            f"[{input_path_str}/Bonsai_Tutorials/_Model/Animation/dummy test 1.srt]\n"
            f"PROCESSING: {input_path_str}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.mkv -> "
            f"{input_path_str}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.srt...\n"
            "SUCCESS: Transcription saved to "
            f"[{input_path_str}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.srt]\n"
            "Transcription completed for all files.\n"
        )

        assert output == great_expectations

    def test_incorrect_interactive_prompting(
        self,
        capsys,
        mocker,
        monkeypatch,
        file_structure: Path,
        mock_input,
        mock_transcription_deps,
        english_only_models_str,
    ):
        """
        Test that interactive prompting handles incorrect model input.
        While not strictly necessary, we use mock_transcription_deps here to
        ensure consistent mocking of dependencies.
        """
        # Simulate incorrect interactive user inputs for model.
        input_path_str = str(file_structure)  # Capture the path string once
        inputs = iter([
            input_path_str,  # Video files input path.
            ".mkv",  # File suffix.
            "foobar.en",  # Model name.
            "n",  # Force overwrite.
            "y",  # Dry run.
            "",  # Apparently, input will use this as if Enter was pressed.
        ])

        # Use the fixture to set the inputs for builtins.input().
        mock_input(inputs)

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        with contextlib.suppress(SystemExit):
            main(args=[])
        sys.stdout.flush()
        output = capsys.readouterr().out
        # Set our expectations.
        expected = (
            f"Entering interactive mode. Please provide the required information.\n"
            f"Enter the directory with videos (default: .): {input_path_str}\n"
            f"\n"  # This newline likely comes from the print before "Current settings"
            f"Current settings for transcribe version {__VERSION__}:\n"
            f"  Suffix: .mp4\n"
            f"  Model: base.en\n"
            f"  Force overwrite: No\n"
            f"  Dry run: No\n"
            f"  Excluded patterns: (None)\n"
            f"  Include patterns: (None)\n"
            f"\n"  # This newline separates "Current settings" from "You will now be prompted".
            f"You will now be prompted for any changes to these settings.\n"
            f"Enter suffix to process (or press Enter to keep '.mp4'): .mkv\n"
            f"Enter model to use (or press Enter to keep 'base.en', available {english_only_models_str}): foobar.en\n"
            f"Invalid model selected. Exiting...\n"
        )

        assert expected == output

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
        dummy_mp4_file = file_structure / "Bonsai_Tutorials" / "videos" / "dummy_video.mp4"
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
            f"SKIPPING: Transcription for [{dummy_mp4_file}] already exists "
            f"as [{dummy_mp4_file.with_suffix('.srt')}] (use --force to overwrite).\n"  # Added newline for consistency
            f"Transcription completed for all files.\n"
        )
        assert output == expected_skip_msg

    def test_videos_to_text_handles_indexerror_during_transcription(
        self,
        mock_args: argparse.Namespace,
        file_structure: Path,
        mocker: pytest.MonkeyPatch,
        capsys,
        mock_transcription_deps,
    ):
        """
        Test that our videos_to_text() method handles IndexError during the transcribe call and continues.
        """
        mock_args.input_path = str(file_structure)
        mock_args.force = True  # Ensure force is True so it doesn't skip due to existing file
        transcriber = Transcriber(mock_args)

        # Mock get_matching_files to return a single dummy file
        dummy_mkv_file = file_structure / "Bonsai_Tutorials" / "videos" / "other_videos" / "dummy_video.mkv"
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
        expected_error_msg = (
            f"PROCESSING: {dummy_mkv_file} -> {dummy_mkv_file.with_suffix('.srt')}...\n"
            f"ERROR: Skipping [{dummy_mkv_file}] due to [Mock index error]\n"  # Added newline
            f"Transcription completed for all files.\n"
        )
        assert output == expected_error_msg

    def test_videos_to_text_handles_empty_transcription_result(
        self,
        mock_args: argparse.Namespace,
        file_structure: Path,
        mocker: pytest.MonkeyPatch,
        mock_transcription_deps,
        capsys,
    ):
        """
        Test that our videos_to_text() method handles a None return from transcribe() gracefully.
        """
        mock_args.input_path = str(file_structure)
        mock_args.force = True  # Ensure force is True

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        transcriber = Transcriber(mock_args)

        # Mock get_matching_files to return a single dummy file
        dummy_mp4_file = file_structure / "Bonsai_Tutorials" / "videos" / "dummy_video.mp4"
        mocker.patch.object(transcriber.filter, "get_matching_files", return_value=[dummy_mp4_file])

        # Mock Path.exists to return False. Not sure why we bother.
        mocker.patch.object(Path, "exists", return_value=False)

        # Mock transcribe to return None
        mock_transcribe = mocker.patch.object(transcriber, "transcribe", return_value=None)

        # Mock pysrt.SubRipFile().save() to ensure it's not called
        mock_subs_save = mocker.patch.object(pysrt.SubRipFile, "save")

        transcriber.videos_to_text()

        # Assert that transcribe WAS called.
        mock_transcribe.assert_called_once_with(dummy_mp4_file)

        # Assert that save was NOT called.
        mock_subs_save.assert_not_called()

        # Capture output and check for the error message.
        output = capsys.readouterr().out
        expected_error_msg = (
            f"PROCESSING: {dummy_mp4_file} -> {dummy_mp4_file.with_suffix('.srt')}...\n"
            f"ERROR: Empty transcribe() return value: [{dummy_mp4_file}]\n"  # Added newline
            f"Transcription completed for all files.\n"
        )
        assert output == expected_error_msg

    def test_transcribe_handles_audio_loading_errors(
        self,
        mock_args: argparse.Namespace,
        file_structure: Path,
        mocker: pytest.MonkeyPatch,
        mock_transcription_deps,
        capsys,
    ):
        """
        Test that our transcribe() method handles exceptions during audio loading (e.g., FileNotFoundError).
        """

        # The mocking of AudioSegment and Whisper model is now handled by mock_transcription_deps.
        # Ensure specific configurations for mock_model (if yielded by fixture) needed are here.

        transcriber = Transcriber(mock_args)

        # Prepare a dummy input file path.
        non_existent_file = file_structure / "Bonsai_Tutorials" / "non_existent_video.mp4"

        # Mock AudioSegment.from_file to raise a FileNotFoundError.
        mock_from_file = mocker.patch(
            "pydub.AudioSegment.from_file", side_effect=FileNotFoundError("Mock file not found error")
        )

        # Call the transcribe method.
        result = transcriber.transcribe(non_existent_file)

        # Assert that AudioSegment.from_file was called with the correct path
        mock_from_file.assert_called_once_with(str(non_existent_file))

        # Assert that the transcribe method returned None.
        assert result is None

        # Capture output and check for the error message.
        output = capsys.readouterr().out
        expected_error_msg = f"ERROR: skipping [{non_existent_file}]: Mock file not found error\n"
        assert output == expected_error_msg

    def test_input_path(self, capsys, file_structure: Path, mock_input: argparse.Namespace, mocker):
        """
        Mock full_parser.parse_args() to return an input_path whose value
        is None.
        """
        inputs = iter([
            ".mkv",  # File suffix.
            "base.en",  # Model name.
            "n",  # Force overwrite.
            "y",  # Dry run.
            "",  # Apparently, input will use this as if Enter was pressed.
        ])

        # Use the fixture to set the inputs for builtins.input().
        mock_input(inputs)

        with contextlib.suppress(SystemExit):
            main(args=["--interactive", "--input-path", str(file_structure)])
        output = capsys.readouterr().out
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
            "Enter suffix to process (or press Enter to keep '.mp4'): .mkv\n"
            "Enter model to use (or press Enter to keep 'base.en', available base.en, "
            "medium.en, small.en, tiny.en): base.en\n"
            "Force overwrite of existing SRT files? (y/N, default: N): n\n"
            "Enable dry run mode? (y/N, default: N): y\n"
            "\n"
            "Confirm settings for transcribe version 1.0.0:\n"
            "  Suffix: .mkv\n"
            "  Model: base.en\n"
            "  Force overwrite: No\n"
            "  Dry run: Yes\n"
            "  Excluded patterns: (None)\n"
            "  Include patterns: (None)\n"
            "\n"
            "Hit Enter to continue, or Ctrl-C to abort.\n"
            "\n"
            "We matched 2 files.\n"
            f"DRY RUN ENABLED, skipping actual transcription of [{file_structure}/Bonsai_Tutorials/_Model/Animation/dummy test 1.mkv]\n"
            f"DRY RUN ENABLED, skipping actual transcription of [{file_structure}/Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.mkv]\n"
            "Transcription completed for all files.\n"
        )

        assert output == expected

    def test_suffix_none(self, capsys, file_structure: Path, mock_input: argparse.Namespace, mocker):
        """
        Mock full_parser.parse_args() to return an input_path whose value
        is None.
        """
        input_path_str = str(file_structure)
        inputs = iter([
            input_path_str,  # Video files input path.
            "",  # Empty File suffix.
            "base.en",  # Model name.
            "n",  # Force overwrite.
            "y",  # Dry run.
            "",  # Apparently, input will use this as if Enter was pressed.
        ])

        # Use the fixture to set the inputs for builtins.input().
        mock_input(inputs)

        with contextlib.suppress(SystemExit, argparse.ArgumentTypeError):
            main(args=[])
        output = capsys.readouterr().out
        expected = (
            "Entering interactive mode. Please provide the required information.\n"
            f"Enter the directory with videos (default: .): {input_path_str}\n"
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
            "Enter suffix to process (or press Enter to keep '.mp4'): \n"
            "invalid suffix: '' (must start with a '.')\n"
        )

        assert output == expected
