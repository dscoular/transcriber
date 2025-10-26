import argparse
import array
import builtins
import sys
from pathlib import Path

import numpy as np
import pytest
import whisper


@pytest.fixture(scope="session")  # Or "function", "module", "class"
def TEST_FILES():
    """
    Standard set of test files for the file structure fixture.
    """
    return [
        "Bonsai_Tutorials/001000_20250218_1337 - moving objects and setting a few preferences/001000_20250218_1337 - moving objects and setting a few preferences.mp4",
        "Bonsai_Tutorials/002000_20250218_1407 - moving, rotating, and scaling/002000_20250218_1407 - moving, rotating, and scaling.mp4",
        "Bonsai_Tutorials/003000_20250218_1437 - 3d cursor/003000_20250218_1437 - 3d cursor.mp4",
        "Bonsai_Tutorials/004000_20250218_1505 - duplicating, moving and rotating with base point/004000_20250218_1505 - duplicating, moving and rotating with base point.mp4",
        "Bonsai_Tutorials/005000_20250218_1532 - edit mode and modifying vertices/005000_20250218_1532 - edit mode and modifying vertices.mp4",
        "Bonsai_Tutorials/006000_20250218_1550 - extruding in edit mode/006000_20250218_1550 - extruding in edit mode.mp4",
        "Bonsai_Tutorials/007000_20250218_1700 - various tools in edit mode/007000_20250218_1700 - various tools in edit mode.mp4",
        "Bonsai_Tutorials/008000_20250218_1714 - quick favorites and redoing a bevel/008000_20250218_1714 - quick favorites and redoing a bevel.mp4",
        "Bonsai_Tutorials/009000_20250218_1735 - dimensioning tools/009000_20250218_1735 - dimensioning tools.mp4",
        "Bonsai_Tutorials/010000_20250218_1749 - changing view orientation/010000_20250218_1749 - changing view orientation.mp4",
        "Bonsai_Tutorials/011000_20250218_1816 - Duplicate Linked/011000_20250218_1816 - Duplicate Linked.mp4",
        "Bonsai_Tutorials/012000_20250218_1829 - Collection Instances/012000_20250218_1829 - Collection Instances.mp4",
        "Bonsai_Tutorials/013000_20250219_1239 - moving geometry's origin/013000_20250219_1239 - moving geometry's origin.mp4",
        "Bonsai_Tutorials/014000_20250219_1302 - Overview of Blender's interface/014000_20250219_1302 - Overview of Blender's interface.mp4",
        "Bonsai_Tutorials/015000_20250219_1331 - resetting scale, rotation and origin location/015000_20250219_1331 - resetting scale, rotation and origin location.mp4",
        "Bonsai_Tutorials/016000_20250219_1425 - Handy quick keys and a few gotchas/016000_20250219_1425 - Handy quick keys and a few gotchas.mp4",
        "Bonsai_Tutorials/017000_20250219_1527 - Overview of Modifiers/017000_20250219_1527 - Overview of Modifiers.mp4",
        "Bonsai_Tutorials/018000_20250219_1559 - Adding new geometry - Meshes and Curves/018000_20250219_1559 - Adding new geometry - Meshes and Curves.mp4",
        "Bonsai_Tutorials/018500_20250220_0824 - Extruding a profile along a path/018500_20250220_0824 - Extruding a profile along a path.mp4",
        "Bonsai_Tutorials/019000_20250219_1711 - Adding Text and Images on Planes/019000_20250219_1711 - Adding Text and Images on Planes.mp4",
        "Bonsai_Tutorials/020000_20250220_0924 - Adding Lights/020000_20250220_0924 - Adding Lights.mp4",
        "Bonsai_Tutorials/021000_20250220_1221 - Adding Cameras/021000_20250220_1221 - Adding Cameras.mp4",
        "Bonsai_Tutorials/022000_20250220_1310 - Adding Empties/022000_20250220_1310 - Adding Empties.mp4",
        "Bonsai_Tutorials/023000_20250220_1356 - relinking missing assets/023000_20250220_1356 - relinking missing assets.mp4",
        "Bonsai_Tutorials/024000_20250220_1526 - Prep work before adding Materials/024000_20250220_1526 - Prep work before adding Materials.mp4",
        "Bonsai_Tutorials/025000_20250220_1549 - Overview of a Material/025000_20250220_1549 - Overview of a Material.mp4",
        "Bonsai_Tutorials/026000_20250220_1621 - Changing the material values and adding a texture/026000_20250220_1621 - Changing the material values and adding a texture.mp4",
        "Bonsai_Tutorials/027000_20250220_1652 - Changing the texture's scale/027000_20250220_1652 - Changing the texture's scale.mp4",
        "Bonsai_Tutorials/028000_20250220_1714 - Applying the texture correctly on all faces/028000_20250220_1714 - Applying the texture correctly on all faces.mp4",
        "Bonsai_Tutorials/029000_20250220_1826 - Adding other PBR textures to the Material/029000_20250220_1826 - Adding other PBR textures to the Material.mp4",
        "Bonsai_Tutorials/030000_20250221_1042 - Changing texture color and contrast/030000_20250221_1042 - Changing texture color and contrast.mp4",
        "Bonsai_Tutorials/031000_20250221_1149 - Creating a new material from another/031000_20250221_1149 - Creating a new material from another.mp4",
        "Bonsai_Tutorials/032000_20250221_1209 - Applying multiple materials to an object/032000_20250221_1209 - Applying multiple materials to an object.mp4",
        "Bonsai_Tutorials/050000_20250221_1325 - Installing Bonsai - Stable Release/050000_20250221_1325 - Installing Bonsai - Stable Release.mp4",
        "Bonsai_Tutorials/051000_20250221_1356 - Installing Bonsai - Unstable Release/051000_20250221_1356 - Installing Bonsai - Unstable Release.mp4",
        "Bonsai_Tutorials/051500_20250224_1329 - Installing Bonsai - from Releases site/051500_20250224_1329 - Installing Bonsai - from Releases site.mp4",
        "Bonsai_Tutorials/052000_20250224_1116 - Starting a demo project/052000_20250224_1116 - Starting a demo project.mp4",
        "Bonsai_Tutorials/053000_20250224_1105 - Overview of the UI/053000_20250224_1105 - Overview of the UI.mp4",
        "Bonsai_Tutorials/054000_20250224_1149 - Edit mode and changing your startup file/054000_20250224_1149 - Edit mode and changing your startup file.mp4",
        "Bonsai_Tutorials/055000_20250224_1227 - Using GIT to see the DIFFs between IFC versions/055000_20250224_1227 -Using GIT to see the DIFFs between IFC versions.mp4",
        "Bonsai_Tutorials/056000_20250224_1438 - Changing the class and attributes/056000_20250224_1438 - Changing the class and attributes.mp4",
        "Bonsai_Tutorials/057000_20250224_1457 - Spatial containers and psets/057000_20250224_1457 - Spatial containers and psets.mp4",
        "Bonsai_Tutorials/058000_20250224_1630 - Introduction to Types/058000_20250224_1630 - Introduction to Types.mp4",
        "Bonsai_Tutorials/059000_20250224_1655 - Type psets and Qto's/059000_20250224_1655 - Type psets and Qto's.mp4",
        "Bonsai_Tutorials/060000_20250226_1112 - Aggregates and Linked Aggregates/060000_20250226_1112 - Aggregates and Linked Aggregates.mp4",
        "Bonsai_Tutorials/061000_20250226_1138 - Introduction to Materials and Styles/061000_20250226_1138 - Introduction to Materials and Styles.mp4",
        "Bonsai_Tutorials/062000_20250226_1218 - Applying multiple styles or materials to one object/062000_20250226_1218 - Applying multiple styles or materials to one object.mp4",
        "Bonsai_Tutorials/063000_20250226_1246 - External Styles/063000_20250226_1246 - External Styles.mp4",
        "Bonsai_Tutorials/064000_20250226_1329 - Creating a Slab/064000_20250226_1329 - Creating a Slab.mp4",
        "Bonsai_Tutorials/065000_20250226_1404 -  Modifying the slab/065000_20250226_1404 -  Modifying the slab.mp4",
        "Bonsai_Tutorials/066000_20250226_1503 - Creating the basement slab/066000_20250226_1503 - Creating the basement slab.mp4",
        "Bonsai_Tutorials/067000_20250226_1636 - Basement Walls/067000_20250226_1636 - Basement Walls.mp4",
        "Bonsai_Tutorials/068000_20250226_1709 - Pulling a material from another library/068000_20250226_1709 - Pulling a material from another library.mp4",
        "Bonsai_Tutorials/069000_20250226_1738 - Adding strip footings/069000_20250226_1738 - Adding strip footings.mp4",
        "Bonsai_Tutorials/070000_20250227_0930 - Thickened edge with custom profile/070000_20250227_0930 - Thickened edge with custom profile.mp4",
        "Bonsai_Tutorials/071000_20250228_1242 - Adding pipe segments/071000_20250228_1242 - Adding pipe segments.mp4",
        "Bonsai_Tutorials/072000_20250228_1356 - Alternate approach to a pipe/072000_20250228_1356 - Alternate approach to a pipe.mp4",
        "Bonsai_Tutorials/073000_20250228_1504 - Different way to select things and a little model clean up/073000_20250228_1504 - Different way to select things and a little model clean up.mp4",
        "Bonsai_Tutorials/074000_20250228_1616 - Wall Tools/074000_20250228_1616 - Wall Tools.mp4",
        "Bonsai_Tutorials/075000_20250303_1407 - An approach to naming wall types/075000_20250303_1407 - An approach to naming wall types.mp4",
        "Bonsai_Tutorials/076000_20250303_1451 - Creating new beam type/076000_20250303_1451 - Creating new beam type.mp4",
        "Bonsai_Tutorials/076000_20250303_1521 - Creating a recess in a wall/076000_20250303_1521 - Creating a recess in a wall.mp4",
        "Bonsai_Tutorials/077000_20250303_1601 - Working with Arrays/077000_20250303_1601 - Working with Arrays.mp4",
        "Bonsai_Tutorials/078000_20250304_1217 - Creating Parametric Stair/078000_20250304_1217 - Creating Parametric Stair.mp4",
        "Bonsai_Tutorials/079000_20250304_1357 - Creating risers by converting parametric stair to dumb geometry/079000_20250304_1357 - Creating risers by converting parametric stair to dumb geometry.mp4",
        "Bonsai_Tutorials/080000_20250304_1723 - pulling in content or assets from other files/080000_20250304_1723 - pulling in content or assets from other files.mp4",
        "Bonsai_Tutorials/081000_20250307_1247 - Walls now show their layers/081000_20250307_1247 - Walls now show their layers.mp4",
        "Bonsai_Tutorials/082000_20250307_1338 - Pull in a wall type from template file and extending to slab/082000_20250307_1338 - Pull in a wall type from template file and extending to slab.mp4",
        "Bonsai_Tutorials/083000_20250307_1451 - Creating linked aggregates for the floor assembly/083000_20250307_1451 - Creating linked aggregates for the floor assembly.mp4",
        "Bonsai_Tutorials/084000_20250310_1656 - Creating reference planes with a IfcVirtualElement/084000_20250310_1656 - Creating reference planes with a IfcVirtualElement.mp4",
        "Bonsai_Tutorials/085000_20250310_1723 - Introduction to Drawings/085000_20250310_1723 - Introduction to Drawings.mp4",
        "Bonsai_Tutorials/086000_20250310_1813 - Continue covering drawings/086000_20250310_1813 - Continue covering drawings.mp4",
        "Bonsai_Tutorials/087000_20250311_1227 - Adding section and modifying section & level annotation/087000_20250311_1227 - Adding section and modifying section & level annotation.mp4",
        "Bonsai_Tutorials/088000_20250311_1441 - Tweaking drawing styles/088000_20250311_1441 - Tweaking drawing styles.mp4",
        "Bonsai_Tutorials/089000_20250311_1540 - Orthographic & Perspective drawings/089000_20250311_1540 - Orthographic & Perspective drawings.mp4",
        "Bonsai_Tutorials/089000_20250311_1540 - Orthographic & Perspective drawings/20250311_1631.mp4",
        "Bonsai_Tutorials/090000_20250311_1700 - Creating sheets and placing drawings/090000_20250311_1700 - Creating sheets and placing drawings.mp4",
        "Bonsai_Tutorials/091000_20250312_1331 - Adding dimensions/091000_20250312_1331 - Adding dimensions.mp4",
        "Bonsai_Tutorials/092000_20250312_1454 - Intelligent tags/092000_20250312_1454 - Intelligent tags.mp4",
        "Bonsai_Tutorials/093000_20250312_1635 - Annotation tag types/093000_20250312_1635 - Annotation tag types.mp4",
        "Bonsai_Tutorials/094000_20250313_1220 - going through the various asset folders/094000_20250313_1220 - going through the various asset folders.mp4",
        "Bonsai_Tutorials/095000_20250313_1301 - Changing the default.css/095000_20250313_1301 - Changing the default.css.mp4",
        "Bonsai_Tutorials/096000_20250313_1420 - Default_css and adding new css classes via Metadata property/096000_20250313_1420 - Default_css and adding new css classes via Metadata property.mp4",
        "Bonsai_Tutorials/097000_20250313_1542 - Creating a demolition plan with CSS rules/097000_20250313_1542 - Creating a demolition plan with CSS rules.mp4",
        "Bonsai_Tutorials/098000_20250313_1802 - Clean up demolition plan/098000_20250313_1802 - Clean up demolition plan.mp4",
        "Bonsai_Tutorials/099000_20250314_1058 - Creating a new tag type/099000_20250314_1058 - Creating a new tag type.mp4",
        "Bonsai_Tutorials/100000_20250314_1321 - Importing a CAD file/100000_20250314_1321 - Importing a CAD file.mp4",
        "Bonsai_Tutorials/101000_20250314_1409 - Moving CAD import to paper space/101000_20250314_1409 - Moving CAD import to paper space.mp4",
        "Bonsai_Tutorials/102000_20250314_1430 - Import background image/102000_20250314_1430 - Import background image.mp4",
        "Bonsai_Tutorials/103000_20250317_1052 - Importing & modifying online BIM assets/103000_20250317_1052 - Importing & modifying online BIM assets.mp4",
        "Bonsai_Tutorials/104000_20250408_1311 - A workaround with geometry based types/104000_20250408_1311 - A workaround with geometry based types.mp4",
        "Bonsai_Tutorials/105000_20250408_1443 - A workaround when duplicating a type with a void/105000_20250408_1443 - A workaround when duplicating a type with a void.mp4",
        "Bonsai_Tutorials/106000_20250408_1526 - Modifying the size of a geometry based type/106000_20250408_1526 - Modifying the size of a geometry based type.mp4",
        "Bonsai_Tutorials/107000_20250411_1149 - Modeling in 2nd floor structure/107000_20250411_1149 - Modeling in 2nd floor structure.mp4",
        "Bonsai_Tutorials/108000_20250414_1207 - Railings - parametric and arrayed/108000_20250414_1207 - Railings - parametric and arrayed.mp4",
        "Bonsai_Tutorials/109000_20250415_1325 - Representation contexts as it relates to a door/109000_20250415_1325 - Representation contexts as it relates to a door.mp4",
        "Bonsai_Tutorials/110000_20250418_1054 - Refresher on using filters, default.css and using Metadata/110000_20250418_1054 - Refresher on using filters, default.css and using Metadata.mp4",
        "Bonsai_Tutorials/111000_20250418_1140 - Quickly flipping btwn drawings and working with doors/111000_20250418_1140 - Quickly flipping btwn drawings and working with doors.mp4",
        "Bonsai_Tutorials/112000_20250418_1503 - Working with Git submodules and syncing OD_Texture library/112000_20250418_1503 - Working with Git submodules and syncing OD_Texture library.mp4",
        "Bonsai_Tutorials/113000_20250418_1626 - Purging unused materials and styles from the file/113000_20250418_1626 - Purging unused materials and styles from the file.mp4",
        "Bonsai_Tutorials/114000_20250418_1640 - Creating a working drawing style/114000_20250418_1640 - Creating a working drawing style.mp4",
        "Bonsai_Tutorials/115000_20250507_1048 - Update on changes to model/115000_20250507_1048 - Update on changes to model.mp4",
        "Bonsai_Tutorials/116000_20250507_1246 - Creating and editing roofs - 2 ways/116000_20250507_1246 - Creating and editing roofs - 2 ways.mp4",
        "Bonsai_Tutorials/117000_20250515_1158 - Intelligent text leaders and managing drawings not on sheets/117000_20250515_1158 - Intelligent text leaders and managing drawings not on sheets.mp4",
        "Bonsai_Tutorials/118000_20250515_1255 - Copying annotation from one drawing to another/118000_20250515_1255 - Copying annotation from one drawing to another.mp4",
        "Bonsai_Tutorials/119000_20250515_1651 - Creating IfcSpaces/119000_20250515_1651 - Creating IfcSpaces.mp4",
        "Bonsai_Tutorials/120000_20250519_1124 - Using space tags/120000_20250519_1124 - Using space tags.mp4",
        "Bonsai_Tutorials/121000_20250519_1627 - Creating schedules/121000_20250519_1627 - Creating schedules.mp4",
        "Bonsai_Tutorials/122000_20250520_1011 - Creating a custom property with a property template/122000_20250520_1011 - Creating a custom property with a property template.mp4",
        "Bonsai_Tutorials/123000_20250522_1356 - More about schedules/123000_20250522_1356 - More about schedules.mp4",
        "Bonsai_Tutorials/124000_20250522_1549 - Intro to Git and creating a floor outline with surrounding walls/124000_20250522_1549 - Intro to Git and creating a floor outline with surrounding walls.mp4",
        "Bonsai_Tutorials/125000_20250522_1658 - Modifying title sheets and drawing titles/125000_20250522_1658 - Modifying title sheets and drawing titles.mp4",
        "Bonsai_Tutorials/126000_20250523_1122 - Starting the site modeling/126000_20250523_1122 - Starting the site modeling.mp4",
        "Bonsai_Tutorials/127000_20250523_1509 - More site modification/127000_20250523_1509 - More site modification.mp4",
        "Bonsai_Tutorials/128000_20250529_1545 - Model updates in prep for site layout/128000_20250529_1545 - Model updates in prep for site layout.mp4",
        "Bonsai_Tutorials/129000_20250529_1627 - Laying out the site with housing types/129000_20250529_1627 - Laying out the site with housing types.mp4",
        "Bonsai_Tutorials/130000_20250530_1436 - Creating the site plan/130000_20250530_1436 - Creating the site plan.mp4",
        "Bonsai_Tutorials/131000_20250630_1310 - Style drawings based on the material's category and layer's material name/131000_20250630_1310 - Style drawings based on the material's category and layer's material name.mp4",
        "Bonsai_Tutorials/132000_20250701_1108 - Bringing objects to the front in drawings and using a faux intelligent tag/132000_20250701_1108 - Bringing objects to the front in drawings and using a faux intelligent tag.mp4",
        "Bonsai_Tutorials/133000_20250701_1241 - Using pre-made SVG patterns from the web/133000_20250701_1241 - Using pre-made SVG patterns from the web.mp4",
        "Bonsai_Tutorials/134000_20250701_1353 - Adding external SVG files to sheets/134000_20250701_1353 - Adding external SVG files to sheets.mp4",
        "Bonsai_Tutorials/135000_20250701_1440 - Modifying the site's topography/135000_20250701_1440 - Modifying the site's topography.mp4",
        "Bonsai_Tutorials/136000_20250711_1223 - Adding Entourage/136000_20250711_1223 - Adding Entourage.mp4",
        "Bonsai_Tutorials/137000_20250909_1001 - Creating a new drawing pattern/137000_20250909_1001 - Creating a new drawing pattern.mp4",
        "Bonsai_Tutorials/_Model/Animation/final video.mp4",
        "Bonsai_Tutorials/_Model/sheets/jpgs/output.mp4",
        # Outliers for testing.
        "Bonsai_Tutorials/_Model/Animation/dummy test 1.mkv",
        "Bonsai_Tutorials/_Model/Animation/jpgs/dummy test 2.mkv",
    ]


class NoMoreTestInputsError(Exception):
    """
    Raised when the simulated input stream is exhausted.

    Args:
        message (str): Custom error message.
    """

    def __init__(self, message="No more input values available"):
        super().__init__(message)


class MockInputNotInitialisedError(RuntimeError):
    """
    Raised when the mock_input fixture's callable is used before inputs have been set.
    """

    def __init__(self, message: str = "Mock input not initialised. Call mock_input_callable(inputs_iter) first."):
        super().__init__(message)


@pytest.fixture
def file_structure(tmp_path: Path, TEST_FILES: [str]) -> Path:
    """Creates a standard directory and file structure for testing."""
    for test_file in TEST_FILES:
        file_path = tmp_path / test_file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
    return tmp_path


@pytest.fixture
def english_only_models_list() -> []:
    """
    Define English-only Whisper models to use in expected output.
    """
    english_only_models = [model for model in whisper._MODELS if model.endswith(".en")]
    return sorted(english_only_models)


@pytest.fixture
def english_only_models_str(english_only_models_list) -> str:
    """
    Define English-only Whisper models to use in expected output.
    """
    return ", ".join(sorted(english_only_models_list))


@pytest.fixture
def help_text(english_only_models_list, english_only_models_str) -> str:
    """Returns the expected help text for the CLI."""
    return (
        "usage: transcribe.py [-h] [--dry-run] [--include [INCLUDE ...]]\n"
        "                     [--exclude [EXCLUDE ...]] [--force]\n"
        "                     [--input-path INPUT_PATH] [--suffix SUFFIX]\n"
        f"                     [--model {{{','.join(english_only_models_list)}}}]\n"
        "                     [--interactive] [--version]\n"
        "\n"
        "Transcribe audio files using a pre-trained model.\n"
        "\n"
        "options:\n"
        "  -h, --help            show this help message and exit\n"
        "  --dry-run, -n         Try a dry run without any actual transcription.\n"
        "  --include [INCLUDE ...]\n"
        "                        A list of files or rglob patterns to include when\n"
        "                        processing. Defaults to **/*.mp4.\n"
        "  --exclude [EXCLUDE ...]\n"
        "                        A list of files or rglob patterns to exclude from\n"
        "                        processing (overrides the include list).\n"
        "  --force               Force overwrite of existing output SRT files.\n"
        "  --input-path INPUT_PATH\n"
        "                        Directory containing input audio files (required in\n"
        "                        non-interactive mode).\n"
        "  --suffix SUFFIX       Suffix of audio files to process (default: .mp4).\n"
        f"  --model {{{','.join(english_only_models_list)}}}\n"
        "                        Pre-trained model to use (default: base.en, available\n"
        f"                        {english_only_models_str}).\n"
        "  --interactive         Run in interactive mode, prompting for missing\n"
        "                        arguments.\n"
        "  --version, -v         Show program's version number and exit.\n"
    )


@pytest.fixture
def mock_args(tmp_path: Path):
    """
    Provides a mock argparse.Namespace object with standard arguments.

    Options:
        --dry-run: If set to True, the transcriber will simulate actions without making changes.
        --include: List of glob patterns to include specific files.
        --exclude: List of glob patterns to exclude specific files.
        --force: If set to True, existing transcription files will be overwritten.
        --input-path: Path to the directory containing video files to transcribe.
        --suffix: Suffix for the video files to transcribe.
        --model: Whisper model to use for transcription.
        --interactive: If set to True, enables interactive mode for user prompts.
        --version: If set to True, displays the version information and exit.
    Note: No options triggers interactive mode by default.
    Args:
        tmp_path (Path): Temporary directory path provided by pytest.
    """
    # Ensure dry_run is part of the mock arguments object
    return argparse.Namespace(
        dry_run=False,
        include=None,
        exclude=None,
        force=False,
        input_path=str(tmp_path),
        suffix=".mp4",
        model="base.en",
        interactive=False,
        version=False,
    )


@pytest.fixture
def clean_transcriber_module():
    """
    Fixture to ensure transcriber.transcribe is removed from sys.modules
    before running tests that use runpy.run_module.
    """
    module_name = "transcriber.transcribe"
    # Store original state
    original_module = sys.modules.pop(module_name, None)
    # Allow the test to run
    yield
    # Restore original state after test, if it existed
    if original_module:
        sys.modules[module_name] = original_module
    # runpy will add it back, so no need to clean up after test if it was runpy's doing


@pytest.fixture
def mock_input(monkeypatch):
    """
    Fixture to mock builtins.input for interactive tests.

    This fixture creates a callable that allows tests to supply a sequence of inputs.
    It uses:
    - =nonlocal=: To create a writable closure, allowing inner functions to modify
                  =input_iterator= from the fixture's scope.
    - =yield=: To define setup (before =yield=) and teardown (after =yield=) logic
               for the fixture, effectively returning a callable for test use.

    Example:
        >>> mock_input_callable = mock_input()
        >>> mock_input_callable(iter(['input1', 'input2', ...]))
        >>> # then proceed with your test that calls input()
    """
    original_input = builtins.input
    input_iterator = None  # Will be set by the test

    def _mocked_input(prompt=""):
        nonlocal input_iterator  # Allows modification of input_iterator from outer scope
        # Are we in the python debugger?
        if prompt.startswith("(Pdb)"):
            return original_input(prompt)  # allow pdb to work
        else:
            # For application prompts, print them using our mock's mechanism
            if prompt:  # Only print if there's actually a prompt string
                sys.stdout.write(prompt)
                sys.stdout.flush()  # Ensure the prompt is written immediately

            if input_iterator is None:
                raise MockInputNotInitialisedError
            try:
                user_input = next(input_iterator)  # Get the user's simulated input
                sys.stdout.write(user_input + "\n")  # Mimic user typing and pressing Enter
                sys.stdout.flush()
            except StopIteration as e:
                raise NoMoreTestInputsError from e
            else:
                return user_input  # Return the input to the application

    # This is the callable that the test will receive from the fixture.
    # It allows the test to pass its specific inputs to the fixture.
    def _set_inputs(inputs_iter):
        nonlocal input_iterator  # Allows modification of input_iterator from outer scope
        input_iterator = inputs_iter
        monkeypatch.setattr(builtins, "input", _mocked_input)
        return _mocked_input  # Return the actual mocked function if needed, though usually not

    yield _set_inputs  # Yields the callable for tests to use; everything after this is teardown

    # Teardown: Restore original builtins.input after the test is done.
    monkeypatch.setattr(builtins, "input", original_input)


@pytest.fixture
def mock_transcription_deps(mocker, monkeypatch):
    """
    Fixture to mock the primary dependencies for the transcription process:
    pydub.AudioSegment.from_file and whisper.load_model.
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
    mocker.patch("pydub.AudioSegment.from_file", return_value=fake_segment)
    # Using mocker.patch here is generally preferred over monkeypatch.setattr
    # because mocker automatically handles cleanup at the end of the test.

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

    # If your tests ever need to inspect mock_model or fake_transcription,
    # you could yield them as a tuple:
    # yield mock_model, fake_transcription
    # For now, simply yielding None (or just 'yield') is sufficient as the mocks are set globally.
    yield
