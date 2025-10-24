## Getting Started

This project uses **`uv`** for dependency management and **`pyenv`** to ensure you're using the correct Python version. Follow the steps below for your operating system to quickly set up the environment and start developing.

---

### 1. Install System Prerequisites

First, you need to install **`direnv`**, **`pyenv`**, **`uv`**, and **`ffmpeg`**.

#### 🍎 **macOS**

On MacOS, the easiest way to install these tools is using **Homebrew**. If you don't have Homebrew, install it first by following the instructions on the [Homebrew website](https://brew.sh/).

```bash
# Install direnv for managing per directory environment variables
$ brew install direnv

# Install pyenv for managing Python versions
$ brew install pyenv

# Install uv (the package manager)
$ brew install uv

# Install FFmpeg for audio/video processing
$ brew install ffmpeg
```

**Note:** You must complete the **`pyenv`** shell configuration steps printed after installation (e.g., adding `eval "$(pyenv init -)"` to your shell config file like `~/.zshrc`).

**Note:** You must use **`"direnv allow"`** when you change into the **transcribe** directory so that it can set the environment variables it needs to using the **`.envrc`** file.

#### 🐧 **Ubuntu** (and WSL2)

Install the prerequisites using the **Advanced Package Tool (`apt`)**.

```bash
$ sudo apt update
$ sudo apt install -y make build-essential libssl-dev zlib1g-dev \\
           libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \\
           libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev

# Install pyenv, uv, and ffmpeg
$ curl https://pyenv.run | bash
$ curl -LsSf https://astral.sh/uv/install.sh | bash
$ sudo apt install -y direnv
$ sudo apt install -y ffmpeg
```

**Note:** After running the **`pyenv`** installation script, you must add the initialization commands (printed to your console) to your shell's configuration file (`~/.bashrc` or `~/.zshrc`) and then restart your terminal.

**Note:** You must use **`"direnv allow"`** when you change into the **transcribe** directory so that it can set the environment variables it needs to using the **`.envrc`** file.

#### 🪟 **Windows**

For a smooth development experience, the recommended approach is to use the **Windows Subsystem for Linux (WSL2)** and follow the **Ubuntu** instructions above.

---

### 2. Project Setup

The project uses a **`Makefile`** to simplify setup. Once your prerequisites are installed, you can set up the entire environment with a single command.

#### **Step 2.1: Install Python and Create the Environment**

The following command will automatically:
1.  Use `pyenv` to install the required Python version.
2.  Use `uv` to create the virtual environment (`.venv`).
3.  Use `uv` to install all project dependencies.
4.  Install **`pre-commit`** hooks.

```bash
# This command runs `pyenv install` and then `uv sync`
$ make install
```

#### **Step 2.2: Activate the Environment**

You can manually activate the virtual environment every time you open a new terminal to work on the project however, **`direnv`** should do this for you automatically based on our **`.envrc`** file.

Here are the commands to activate your virtual python environment manually.

```bash
# For macOS/Ubuntu/WSL
$ source .venv/bin/activate
# For native Windows (cmd or PowerShell)
# .venv\\Scripts\\activate
```

---

### 3. Make Commands

The project uses `make` targets to standardize common tasks. Ensure your virtual environment is **active** before running these commands.

| Command | Description |
| :--- | :--- |
| `make install` | **Setup:** Install the virtual environment, dependencies, and pre-commit hooks. |
| `make check` | **Quality:** Run code quality tools (linters/formatters, dependency checks, and type-checking). |
| `make test` | **Quality:** Run the automated tests using `pytest`. |
| `make docs-test` | **Quality:** Test if documentation can be built without warnings or errors. |
| `make build` | **Distribution:** Build the distributable wheel (`.whl`) and source archive (`.tar.gz`) files in the `dist/` directory. |
| `make clean-build` | **Cleanup:** Remove build artifacts from the `dist/` directory. |
| `make docs` | **Documentation:** Build the documentation and serve it locally (usually at `http://127.0.0.1:8000`). |
| `make man` | **Documentation:** Display the `transcribe` scripts `--help` output in the form of a `man` page. |
| `make transcribe` | **Execution:** Interactively run the main application to transcribe video files to SRT subtitle files. |
| `make help` | **Help:** Display this help message with descriptions for all targets. |

---

#### 3.1. Reading the Command "man" page.

To see the options that you can give the `transcribe.py` script simple run the following:

```bash
# 1. Run the "man" target.
$ make man
```

This will display the following "man" page:

```bash
$ make man
usage: transcribe.py [-h] [--dry-run] [--include [INCLUDE ...]] [--exclude [EXCLUDE ...]] [--force] [--input-path INPUT_PATH] [--suffix SUFFIX] [--model {tiny.en,base.en,small.en,medium.en}] [--interactive] [--version]

Transcribe audio files using a pre-trained model.

options:
  -h, --help            show this help message and exit
  --dry-run, -n         Try a dry run without any actual transcription.
  --include [INCLUDE ...]
                        A list of files or rglob patterns to include when processing. Defaults to **/*.mp4.
  --exclude [EXCLUDE ...]
                        A list of files or rglob patterns to exclude from processing (overrides the include list).
  --force               Force overwrite of existing output SRT files.
  --input-path INPUT_PATH
                        Directory containing input audio files (required in non-interactive mode).
  --suffix SUFFIX       Suffix of audio files to process (default: .mp4).
  --model {tiny.en,base.en,small.en,medium.en}
                        Pre-trained model to use (default: base.en, available ['tiny.en', 'base.en', 'small.en', 'medium.en']).
  --interactive         Run in interactive mode, prompting for missing arguments.
  --version, -v         Show program's version number and exit.
```

Giving no arguments will cause the command to run in "interactive" mode, prompting you for any information you need.
Supplying the arguments on the command-line gives you more control.
You can override the interactive mode's defaults by supplying the `--interactive` option combined with the command options you want to override.

#### 3.2. Running the Transcriber using "make"

To run the main functionality of the project, use the dedicated "transcribe" target:

```bash
# 1. Run the interactive transcriber tool
$ make transcribe
```
This will display the current transcription defaults and prompt you interactively for any defaults you want to change. See the next section for more details and an example.

##### 3.2.1 Interacting with the Transcriber

The `Makefile` **transcribe** target actually calls our script with the following arguments
The **`uv run`** part ensures that we are running under the correct python environment:

```make
transcribe:
    @uv run python src/transcriber/transcribe.py --interactive --exclude \
	"_Model/sheets/jpgs/output.mp4" \
	"_Model/OD_Textures/Open Source/AmbientCG/space-generation-success.mp4" \
	"_Model/OD_Textures/Open Source/AmbientCG/space-generation-fail.mp4" \
	"_Model/Animation/final video.mp4"
```

This `Makefile` target causes the script to run interactively but also excludes some of the mp4 videos,
typically found in the **Bonsai_Tutorials** directory, which have no audio to transcribe.

In *interactive mode* the script displays the current settings and then gives you
the opportunity to override some of these defaults (the non-interactive mode lets you override
anything with command-line options).

Here is my attempt to use the `Makefile` to run our script and tweak it to use
some non-defaults i.e.

- my preferred path (`~/projects/Bonsai_Tutorials`)
- the largest **Whisper** model available (`medium.en` instead of the default smallest model,`base.en`).

Okay, let's run **`make transcribe`**:

```bash
$ make transcribe
Entering interactive mode. Please provide the required information.
Enter the directory with videos (default: .):
```

The first thing the script needs to know is where the video files live.
We do not want the default (the current working directory) so we'll enter
the location of our videos as being `~/projects/Bonsai_Tutorials`:

```bash
Enter the directory with videos (default: .): ~/projects/Bonsai_
```

The script then shows the current default settings and prompts you to see if you want to override the current defaults:

```bash
Current settings for transcribe version 1.0.0:
  Suffix: .mp4
  Model: base.en
  Force overwrite: No
  Dry run: No
  Excluded patterns: (_Model/sheets/jpgs/output.mp4, _Model/OD_Textures/Open Source/AmbientCG/space-generation-success.srt, _Model/OD_Textures/Open Source/AmbientCG/space-generation-fail.srt, _Model/Animation/final video.srt)
  Include patterns: (None)
You will now be prompted for any changes to these settings.
Enter suffix to process (or press Enter to keep '.mp4'):
```
We'll take the default **`suffix`** by hitting the `Enter` (or `Return`) key.

Next, we are prompted to enter the **Whisper** model we want to use, the default is the smallest (**`base.en`**), which gives great results, but we will go with the largest model instead (**`medium,en`**). To be honest, the smallest model's results are pretty similar.

We'll take the default for "Force overwrite" (No), this stops the script overwriting any existing **`.srt`** files).
We'll also take the default for "Enable dry run mode" (No), this means the script will actually perform the transcription instead of just printing what it would have done.

```bash
Enter model to use (or press Enter to keep 'base.en', available tiny.en, base.en, small.en, medium.en): medium.en
Force overwrite of existing SRT files? (y/N, default: N):
Enable dry run mode? (y/N, default: N):
```
At this point, the script will output a summary of your choices and ask you to confirm if you want to proceed.

```bash
Confirm settings for transcribe version 1.0.0:
  Suffix: .mp4
  Model: medium.en
  Force overwrite: No
  Dry run: No
  Excluded patterns: (_Model/sheets/jpgs/output.mp4, _Model/OD_Textures/Open Source/AmbientCG/space-generation-success.srt, _Model/OD_Textures/Open Source/AmbientCG/space-generation-fail.srt, _Model/Animation/final video.srt)
  Include patterns: (None)

Hit Enter to continue, or Ctrl-C to abort.
```

The script waits for you to confirm either by hitting the `Enter` (or `Return`) key or cancel by hitting `Ctrl-C`.

We hit `Enter` and, as the CPU or GPU starts to glow white hot, we eventually get SRT subtitle text files as siblings to all the `.mp4` files we recursively found in our `Bonsai_Tutorials`.

You should see quite a bit of output as the script processes each video.

## Example of How I use the SRT files.

To find a critical explanation, now that I have all the transcriptions available as `.srt` SRT subtitle text files, I can simply use any text searching tool I want to find the topic I'm interested in:

```bash
$ find Bonsai_Tutorials -name \*.srt -exec grep -i 'profiles' {} \; -print
Go down to our profiles
Bonsai_Tutorials/077000_20250303_1601 - Working with Arrays/077000_20250303_1601 - Working with Arrays.srt
And I'm going to create a custom profile from that. So go down to our profiles and click on this object to pick it up.
Bonsai_Tutorials/077000_20250303_1601 - Working with Arrays/077000_20250303_1601 - Working with Arrays.base.srt
also you can purge unused profiles and sorry unused types as well but I'm not
Bonsai_Tutorials/113000_20250418_1626 - Purging unused materials and styles from the file/113000_20250418_1626 - Purging unused materials and styles from the file.srt
And there's also you can purge unused profiles and sorry unused types as well.
Bonsai_Tutorials/113000_20250418_1626 - Purging unused materials and styles from the file/113000_20250418_1626 - Purging unused materials and styles from the file.base.srt
To those profiles and layer sets.
Bonsai_Tutorials/093000_20250312_1635 - Annotation tag types/093000_20250312_1635 - Annotation tag types.base.srt
material was already signed to that to those profiles and layer sets.
Bonsai_Tutorials/093000_20250312_1635 - Annotation tag types/093000_20250312_1635 - Annotation tag types.srt
Click on this dropdown, you can see all the different types of profiles that IFC offers.
Bonsai_Tutorials/069000_20250226_1738 - Adding strip footings/069000_20250226_1738 - Adding strip footings.base.srt
Click on this drop down you can see all the different types of profiles that IFC offers
Bonsai_Tutorials/069000_20250226_1738 - Adding strip footings/069000_20250226_1738 - Adding strip footings.srt
You can pull in, you know, I've seen materials, profiles, and types.
Bonsai_Tutorials/080000_20250304_1723 - pulling in content or assets from other files/080000_20250304_1723 - pulling in content or assets from other files.srt
And you can pull in, I've seen materials, profiles and types.
Bonsai_Tutorials/080000_20250304_1723 - pulling in content or assets from other files/080000_20250304_1723 - pulling in content or assets from other files.base.srt
We're going to go to profiles and we're going to use this arbitrary, closed profile
Bonsai_Tutorials/070000_20250227_0930 - Thickened edge with custom profile/070000_20250227_0930 - Thickened edge with custom profile.base.srt
We're going to go to profiles and we're going to use this arbitrary closed profile def.
Bonsai_Tutorials/070000_20250227_0930 - Thickened edge with custom profile/070000_20250227_0930 - Thickened edge with custom profile.srt
The cabinets here are kind of just generic, massing cabinets. They're actually extruded profiles
Bonsai_Tutorials/124000_20250522_1549 - Intro to Git and creating a floor outline with surrounding walls/124000_20250522_1549 - Intro to Git and creating a floor outline with surrounding walls.base.srt
They're actually extruded profiles if I tab into them.
Bonsai_Tutorials/124000_20250522_1549 - Intro to Git and creating a floor outline with surrounding walls/124000_20250522_1549 - Intro to Git and creating a floor outline with surrounding walls.srt
```

Armed with these clues, I can then use `vlc`, or some equivalent video player, and I can find the exact section of the video I need to watch.

You can also use the timings in the SRT file to find the time the phrase occurred.

Any advice for improvement much appreciated...

AtDhVaAnNkCsE

Doug Scoular
dscoular@gmail.com
2025/10/23
