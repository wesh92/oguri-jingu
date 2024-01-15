# Oguri Jingu

<sup> オグリ-神宮 </sup>

I don't have an Oguri Cap logo yet but if you find one (and I can use it) feel free to submit!

## FOSS Toolset and Utilities (+web?) for Uma Musume

### Project Scope

Provide Tools/Utilities (and possibly some web stuff/api) for the game Uma Musume.

Nothing will be hosted here, these are simply tools for you to explore/extract data from the files.

### Directory Breakdown

`/src/` -- Main directory with subdirectories dedicated to tools and other things!

`/src/asset_extraction` -- Tools for extracting things like Character Icons, Supporter Card Icons, Textures, etc.

`/src/data/` -- When you use the `main.py` script in `asset_extraction` it will output your images in this directory.

### Contributions

I will take any help one is willing to provide. I have setup poetry for your convenience so please make sure to use that so that we're all developing on the same dependancies! With that said here are some tools you will be expected to use when contributing in python (just to keep ourselves on the same page):

| Tool                          | Link                                              |
| ----------------------------- | ------------------------------------------------- |
| Black (Formatter)             | [Link](https://github.com/psf/black)              |
| Ruff (Formatter)              | [Link](https://github.com/astral-sh/ruff)         |
| Poetry (venv coordination)    | [Link](https://python-poetry.org/)                |
| pre-commit (Git Commit Hooks) | [Link](https://pre-commit.com/)                   |

Full disclosure: I am a Backend and Data Platform Engineer. So I do not have the skills (yet!) to provide solid front ends. Anyone willing to put stuff together using these tools with a FE is totally free to do so where ever you need to! That is not to say I won't do some myself, but rather to assure you I won't ask you to remove it because of any personal sites that arise.

Below you'll also find some personal goals mixed with community suggested additions. If you are a community member and would like to request something (but cannot contribute to the code yourself) feel free to make an issue up at the top of this repo.

### Goals

| Done?              | Goal                                        | Project Link                                                                 |
| ------------------ | ------------------------------------------- | ---------------------------------------------------------------------------- |
| :x:                | Add TW extraction methods                   | ?                                                                            |
| :x:                | Add KR extraction methods                   | ?                                                                            |
| :x:                | Simpler API interface for data from the MDB | ?                                                                            |
| :x:                | Deeper search API for Horse Girls           | ?                                                                            |
| :white_check_mark: | Modernize Asset Extraction methods          | [Link](https://github.com/wesh92/oguri-jingu/tree/main/src/asset_extraction) |
| 👷 | Add text extractor for JP with better JSON structures | ? |
