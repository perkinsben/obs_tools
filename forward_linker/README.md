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

```python obs-linkr.py <path to obsidian vault root> [-w / -p]```  

```-w = only the first occurrence of a page title (or alias) in the content will be linked ('wikipedia mode')```  

```-p = only the first occurrence of a page title (or alias) in each paragraph will be linked ('paragraph mode')```

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

You can also use aliases.yml to exclude linking of pages by adding a blank alias entry for the title:

```
Note Title to Ignore:
-
- alias 1
- alias 2
```

Note that aliases are still matched (if provided), even when the title page is excluded.

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

---
# Obsidian Unlinker

This is a small utility to remove links in a block of text. It operates on the text in your clipboard. It is intended to work as a companion to the linker script that can quickly unlink blocks of text that are 'overlinked'.

It scrubs links of the type:
- ```[[this]] becomes this```
- ```[[Great Page|that]] becomes that```

It does not touch links of the type:
- ```![[untouchable]]```
- ```![this link](is safe)```
- ```[so is](this one)```

## Requirements

* Python 3 + pip
* [Pyperclip](https://pypi.org/project/pyperclip/) - Note that Mac and Linux may require installation of additional modules as per docs

```pip install pyperclip```

## Running

```python obs-unlinkr.py```  

## Example

Assuming you had the following text in your clipboard:

```[[Psychology]] is the [[Science]] of human [[Behavior|behavior]]. ![[Great Quote]]```

After executing the script, it would be replaced with the following:

```Psychology is the Science of human behavior. ![[Great Quote]]```

---
# AutoHotKey Integration

These scripts can integrate nicely with [AutoHotKey](https://www.autohotkey.com/) for Windows.

Linking (Ctrl+L links selected text):
```
^l::
Clipboard=
Send ^c
RunWait, cmd.exe /c python obs-linkr.py c:\path\to\your\vault, c:\scripts\obs_tools\forward_linker, Hide
Send ^v
```

Unlinking (Ctrl+U unlinks selected text):
```
^u::
Clipboard=
Send ^c
RunWait, cmd.exe /c python obs-unlinkr.py c:\path\to\your\vault, c:\scripts\obs_tools\forward_linker, Hide
Send ^v
```

You'll have to modify the paths to match your own, and may need to add Python to your Windows %PATH%.