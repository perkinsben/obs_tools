# Obsidian Forward Linker

This script does the following:

- Scans your vault location recursively for .md files and builds a list of note titles
- Sorts the titles from longest to shortest
- Pulls the text from your clipboard
- Searches through that text for instances of the titles
- Replaces the text with the link (includes handling of differing case)
- Pushes the linked text back to the clipboard

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