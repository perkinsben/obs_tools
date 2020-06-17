# Obsidian Forward Linker

This script does the following:

- Scans your vault location recursively for .md files and builds a list of note titles
- Imports title aliases from aliases.yml in vault root
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