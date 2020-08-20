# Obsidian Forward Linker

This script does the following:

- Scans your vault location recursively for .md files and builds a list of note titles
- Imports title aliases from aliases.yml in vault root
- Sorts the titles from longest to shortest
- Pulls the text from your clipboard
- Searches through that text for instances of the titles
- Replaces the text with the link (includes handling of differing case)
- Pushes the linked text back to the clipboard

## Requirements

* Python 3 + pip
* [Pyperclip](https://pypi.org/project/pyperclip/) - Note that Mac and Linux may require installation of additional modules as per docs
* [PyYAML](https://pypi.org/project/PyYAML/)

```pip install pyperclip pyyaml```

## Running

```python obs-linkr.py {path to obsidian vault root}```

## Example

Assuming you had the following pages in your Obsidian vault:

* Psychology.md
* Science.md
* Behavior.md

And the following text in your clipboard to import:

```Psychology is the Science of human behavior.```

After executing the script, it would be replaced with the following:

```[[Psychology]] is the [[Science]] of human [[Behavior|behavior]].```

## Aliases

You can use a file named aliases.yml in your vault root to broaden the title matching in your text to include aliases.

#### Format

```
Note Title:
- alias 1
- alias 2
- alias 3
```

#### Example

Assuming you had a file in your vault named ```problem solving.md```

aliases.yml:
```
problem solving:
- solving problems
- problem solve
```

Input text:
```In order to properly problem solve, you should wear your Problem Solving Hat.```

Output text:
```In order to properly [[problem solving|problem solve]], you should wear your [[problem solving|Problem Solving]] Hat.```

## Notes

This tool leverages an opinionated use case of Obsidian. Those who use literal text titles to identify their notes will find more utility than those who don't (eg. the zettelkasten folks), but using the aliases file strategically can handle a wide range of matching scenarios. If you have duplicated titles in your vault (ie. Obsidian prefixed them with a folder name due to ambiguity) you’ll only get links to the original (unqualified) page with that title.  

Spec04 wrote a python script that generates the aliases.yml file from tags within your note files: [Obsidian Alias File Generator](https://github.com/Spec04/obs_alias_generator)