# Obsidian Forward Linker

*Update June 2021:* A new core Obsidian plugin [Outgoing Links](https://help.obsidian.md/Plugins/Outgoing+links) introduced in [Obsidian v0.12.4](https://forum.obsidian.md/t/obsidian-release-v0-12-4/18764) covers much of the functionality of this script. It can identify potential links in a document and provide one-click linking within the app. I'll still maintain this project, but I'd urge you to evaluate the new plugin to see if that meets your needs.  

This script does the following:

- Scans your vault location recursively for .md files and builds a list of note titles
- Optionally builds a list of title aliases by scanning YAML frontmatter in notes
- Sorts the titles from longest to shortest
- Pulls the text from your clipboard
- Searches through that text for instances of the titles
- Replaces the text with the link (includes handling of differing case)
- Pushes the linked text back to the clipboard

## Requirements

* Python 3 + pip
* [Pyperclip](https://pypi.org/project/pyperclip/) - Note that Mac and Linux may require installation of additional modules as per docs
* [PyYAML](https://pypi.org/project/PyYAML/)
* [Python Frontmatter](https://pypi.org/project/python-frontmatter/)

```pip3 install pyperclip pyyaml python-frontmatter```

## Running

```python obs-linkr.py <path to obsidian vault root> [-r] [-y] [-w / -p]```  

```-r = regenerate the aliases.md file using yaml frontmatter inside vault markdown files``` 

```-y = use aliases.yml as aliases file instead of aliases.md```

```-w = only the first occurrence of a page title (or alias) in the content will be linked ('wikipedia mode')```  

```-p = only the first occurrence of a page title (or alias) in each paragraph will be linked ('paragraph mode')```

```-u = remove existing links in clipboard text before performing linking```

## Example

Assuming you had the following pages in your Obsidian vault:

* Psychology.md
* Science.md
* Behavior.md

And the following text in your clipboard to import:

```Psychology is the Science of human behavior.```

After executing the script, it would be replaced with the following:

```[[Psychology]] is the [[Science]] of human [[Behavior|behavior]].```

---
# Aliases

Aliases were introduced in Obsidian v0.9.16 and are defined in YAML frontmatter as described here: https://publish.obsidian.md/help/How+to/Add+aliases+to+note. Aliases are used when linking text so that alternate titles can link back to a central note.

### Example

problem solving.md:
```
---
aliases: ["solving problems", "problem solve"]
---

...note content here...
```

If the '-r' flag is provided on the command line, the script will generate an aliases file by searching each file in the vault for frontmatter aliases. If the '-r' flag is not passed on the command line, the existing aliases file will be used.

Adding an empty alias will prevent the title itself from being linked, yet still allow the aliases to be linked to the page.

### Example

Work.md
```
---
aliases: ["", "workplace"]
---
```

The text 'work' (case-insensitive) in this scenario will not be linked. This notation is captured in the aliases file as:

```
[[Work]]:
- 
- workplace
```

## aliases.md vs aliases.yml

By default, the script stores the parsed aliases in aliases.md at the root of the vault. You can choose to store the aliases in aliases.yml if desired by passing the '-y' flag on the commmand line. The format of both files is the same (standard YAML), except aliases.md supports wikilinks in titles (see below).

Using aliases.md provides some additional features:
- The file can be opened in Obsidian
- All aliases defined in the vault are visible in one file
- The page titles are linked for easy navigation to original alias definition, eg.:
```
[[problem solving]]:
- solving problems
- problem solve
```

When generating aliases.md, the script inserts the following text to exclude the term 'aliases' itself from being linked:
```
aliases:
- 
```

Note: It is not recommended to edit the aliases file directly since it can be overwritten by running the script.

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

```pip3 install pyperclip```

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

Linking (Shift+Ctrl+L links selected text):
```
+^l::
Clipboard=
Send ^c
RunWait, cmd.exe /c python obs-linkr.py c:\path\to\your\vault, c:\scripts\obs_tools\forward_linker, Hide
Send ^v
```

Unlinking (Shift+Ctrl+U unlinks selected text):
```
+^u::
Clipboard=
Send ^c
RunWait, cmd.exe /c python obs-unlinkr.py c:\path\to\your\vault, c:\scripts\obs_tools\forward_linker, Hide
Send ^v
```

You'll have to modify the paths to match your own, and may need to add Python to your Windows %PATH%.

---
# Notes

If you have duplicated titles in your vault (ie. Obsidian prefixed them with a folder name due to ambiguity) you’ll only get links to the original (unqualified) page with that title.  