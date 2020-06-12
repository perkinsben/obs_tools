# pip install pyperclip
import pyperclip
import sys
import os
import re

page_titles = []
obsidian_home = ''

def link_title(title, txt):
    updated_txt = txt
    # find instances of the title where it's not surrounded by [] or other letters
    m = re.search('(?<!([\[\w\|]))' + re.escape(title.lower()) + '(?!([\]\w]))', txt.lower(), 1) # get 1 match at a time
    if (m):
        # get the original text to link
        txt_to_link = txt[m.start():m.end()]
        #print(txt_to_link)
        # handle the display casing if it doesn't match
        if (txt_to_link != title): title = title + '|' + txt_to_link
        # create the link and update our text
        updated_txt = txt[:m.start()] + '[[' + title + ']]' + txt[m.end():]
    
    #print(updated_txt)
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

# sort from longest to shortest page titles so that we don't
# identify scenarios where a page title is a subset of another
page_titles = sorted(page_titles, key=lambda x: len(x), reverse=True)
print('----------------------')

## iterate through our page titles
for page_title in page_titles:
    # if we have a case-insenitive title match...
    if page_title.lower() in clip_low:        
        print('found %s in text' % page_title)
        # track whether we still have unlinked references to process
        unlinked_refs_remain = True
        
        # keep attempting to match titles until we're done
        while unlinked_refs_remain:
            updated_txt = link_title(page_title, clip_txt)            
            # we can tell whether we're finished by testing whether
            # the linking process changed the updated text length
            if len(updated_txt) == len(clip_txt):
                unlinked_refs_remain = False
            else:
                clip_txt = updated_txt

        # lowercase our updated text for the next round of search
        clip_low = clip_txt.lower()        

# send the linked text to the clipboard            
pyperclip.copy(clip_txt)
#print(clip_txt)
print('----------------------')
print('linked text copied to clipboard')