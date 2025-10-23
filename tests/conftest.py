import argparse
from pathlib import Path

import pytest


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


@pytest.fixture
def help_text() -> str:
    """Returns the expected help text for the CLI."""
    return (
        "usage: transcribe.py [-h] [--dry-run] [--include [INCLUDE ...]]\n"
        "                     [--exclude [EXCLUDE ...]] [--force]\n"
        "                     [--input-path INPUT_PATH] [--suffix SUFFIX]\n"
        "                     [--model {tiny.en,base.en,small.en,medium.en}]\n"
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
        "  --model {tiny.en,base.en,small.en,medium.en}\n"
        "                        Pre-trained model to use (default: base.en, "
        "available\n"
        "                        ['tiny.en', 'base.en', 'small.en', 'medium.en']).\n"
        "  --interactive         Run in interactive mode, prompting for missing\n"
        "                        arguments.\n"
        "  --version, -v         Show program's version number and exit.\n"
    )


@pytest.fixture
def file_structure(tmp_path: Path, TEST_FILES: [str]) -> Path:
    """Creates a standard directory and file structure for testing."""
    for test_file in TEST_FILES:
        file_path = tmp_path / test_file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
    return tmp_path


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
def mock_whisper_loader(mocker: pytest.MonkeyPatch):
    mock_model = mocker.MagicMock()
    mock_model.transcribe.return_value = {"segments": [{"start": 0, "end": 1, "text": "test"}]}
    return mocker.patch("transcriber.transcribe.whisper.load_model", return_value=mock_model)
