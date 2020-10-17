# pip install pyperclip pyyaml
import pyperclip
import yaml
import sys
import os
import re

page_titles = []
page_aliases = {}
obsidian_home = ''

def link_title(title, txt):
    updated_txt = txt
    # find instances of the title where it's not surrounded by [], | or other letters
    matches = re.finditer('(?<!([\[\w\|]))' + re.escape(title.lower()) + '(?!([\|\]\w]))', txt.lower())
    offset = 0 # track the offset of our matches (start index) due to document modifications
    
    for m in matches:
        # get the original text to link
        txt_to_link = updated_txt[m.start() + offset:m.end() + offset]
        
        # where is the next ]]?
        next_closing_index = updated_txt.find("]]", m.end() + offset)
        # where is the next [[?
        next_opening_index = updated_txt.find("[[", m.end() + offset)   
        
        # only proceed to link if our text is not already enclosed in a link
        if (next_opening_index == -1) or (next_opening_index < next_closing_index):
            updated_title = title
            # handle aliases
            if (title in page_aliases): updated_title = page_aliases[title]
            # handle the display text if it doesn't match the page title
            if (txt_to_link != updated_title): updated_title += '|' + txt_to_link
            # create the link and update our text
            updated_txt = updated_txt[:m.start() + offset] + '[[' + updated_title + ']]' + updated_txt[m.end() + offset:]
            # change our offset due to modifications to the document
            offset = offset + (len(updated_title) + 4 - len(txt_to_link)) # pairs of double brackets adds 4 chars
            
    return updated_txt

# validate obsidian vault location
if (len(sys.argv) > 1):
    obsidian_home = sys.argv[1]
    if not os.path.isdir(obsidian_home):
        print('folder specified is not valid')
        exit()
else:
    print("usage - python obs-link.py [path to obsidian vault]")
    exit()

# get text from clipboard
clip_txt = pyperclip.paste()
print('--- clipboard text ---')
print(clip_txt)
print('----------------------')

# make a copy of it and lowercase it for search purposes
clip_low = clip_txt.lower()

# get a directory listing of obsidian *.md files
# use it to build our list of titles
for root, dirs, files in os.walk(obsidian_home):
    for file in files:
        if file.endswith('.md'):
            page_title = re.sub(r'\.md$', '', file)
            print(page_title)
            page_titles.append(page_title)

# we'll also check for an aliases file and load that
# we pivot (invert) the dict for lookup purposes
aliases_file = obsidian_home + "/aliases.yml"
if os.path.isfile(aliases_file):
    with open(aliases_file, 'r') as stream:
        try:
            aliases = yaml.full_load(stream)
            
            for title in aliases:
                #print(title)
                if aliases[title]:                  
                    for alias in aliases[title]:
                        if alias:
                            page_aliases[alias] = title
                        else:
                            # empty entry will signal to ignore page title in matching
                            print("Empty alias (will be ignored): " + title)
                            if title in page_titles:
                                page_titles.remove(title)
                #print(page_aliases)
        except yaml.YAMLError as exc:
            print(exc)
            exit()

# append our aliases to the list of titles
for alias in page_aliases:
    page_titles.append(alias)

# sort from longest to shortest page titles so that we don't
# identify scenarios where a page title is a subset of another
page_titles = sorted(page_titles, key=lambda x: len(x), reverse=True)
print('----------------------')

## iterate through our page titles
for page_title in page_titles:
    # if we have a case-insenitive title match...
    if page_title.lower() in clip_low:        
        updated_txt = link_title(page_title, clip_txt)            
        # we can tell whether we've matched the term if
        # the linking process changed the updated text length
        if len(updated_txt) != len(clip_txt):
            clip_txt = updated_txt
            print("linked %s" % page_title)

        # lowercase our updated text for the next round of search
        clip_low = clip_txt.lower()        

# send the linked text to the clipboard            
pyperclip.copy(clip_txt)
#print(clip_txt)
print('----------------------')
print('linked text copied to clipboard')