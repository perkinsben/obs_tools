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
    # find instances of the title where it's not surrounded by [] or other letters
    m = re.search('(?<!([\[\w\|]))' + re.escape(title.lower()) + '(?!([\|\]\w]))', txt.lower(), 1) # get 1 match at a time
    if (m):
        # get the original text to link
        txt_to_link = txt[m.start():m.end()]
        #print(txt_to_link)
        # handle aliases
        if (title in page_aliases): title = page_aliases[title]
        # handle the display text if it doesn't match the page title
        if (txt_to_link != title): title = title + '|' + txt_to_link
        # create the link and update our text
        updated_txt = txt[:m.start()] + '[[' + title + ']]' + txt[m.end():]
    
    #print(updated_txt)
    return updated_txt

# the regex to identify links is smart enough that it can detect whether text
# being linked has [[, ]] or | adjacent to it and skip, but there are cases that it
# can't detect (eg. given the following page titles: "Learning", "Great Learning Plan")
# and text "see my Great Learning Plan", the script (by default) would link as:
# "see my [[Great [[Learning]] Plan]]"
# because "Learning" looks to the tool to be a unique term (no [[, ]] or | adjacent)
# we use the following method to scrub any instances of these from our document
# due to the matching algorithm, this is the best/easiest way to accomplish this
def scrub_nested_links(txt):
    updated_txt = txt
    
    # find all instances of [[
    for m in re.finditer("\[\[", updated_txt):
        # where is the next ]]?
        next_closing_index = updated_txt.find("]]", m.end())
        # where is the next [[?
        next_opening_index = updated_txt.find("[[", m.end())    
        
        # if there is another [[ that appears before the next ]], we need to scrub the nested link
        if (next_opening_index > -1) and (next_opening_index < next_closing_index):         
            print("scrubbing link " + updated_txt[m.start():next_closing_index + 2] + "...")
            # snip out the bad link
            nested_link = updated_txt[next_opening_index + 2:next_closing_index]
            # handle piped display syntax if present
            if ("|" in nested_link): nested_link = nested_link[nested_link.index("|") + 1:]            
            # update our text with the nested link scrubbed
            updated_txt = updated_txt[:next_opening_index] + nested_link + updated_txt[next_closing_index + 2:]
            # recursively call this method until there are no more nested links
            updated_txt = scrub_nested_links(updated_txt)
    
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

# iterate through our page titles
for page_title in page_titles:
    # if we have a case-insenitive title match...
    if page_title.lower() in clip_low:        
        # track whether we still have unlinked references to process
        unlinked_refs_remain = True
        
        # track whether we have linked the term
        matched_one = False
        
        # keep attempting to match titles until we're done
        while unlinked_refs_remain:
            updated_txt = link_title(page_title, clip_txt)            
            # we can tell whether we're finished by testing whether
            # the linking process changed the updated text length
            if len(updated_txt) == len(clip_txt):                
                unlinked_refs_remain = False
            else:
                clip_txt = updated_txt
                if not matched_one:
                    print("linked %s" % page_title)
                    matched_one = True                

        # lowercase our updated text for the next round of search
        clip_low = clip_txt.lower()        

# we might have some incorrect nested matches - let's scrub them
clip_txt = scrub_nested_links(clip_txt)

# send the linked text to the clipboard            
pyperclip.copy(clip_txt)
#print(clip_txt)
print('----------------------')
print('linked text copied to clipboard')