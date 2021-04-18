# pip3 install pyperclip
import pyperclip
import re

def unlink_text(txt):
    # keep track of the location in our text as we process it
    index = 0

    while True:
        # where is the next [[?
        next_opening_index = txt.find("[[", index)
        # where is the next ]]?
        next_closing_index = txt.find("]]", index)
        
        # if we don't find matching brackets, break
        match_exists = (next_opening_index > -1) and (next_closing_index > -1)
        if not match_exists: break
        
        # if there is a match, but there is an exclamation point 
        # (embed syntax) in front, move our index ahead and continue
        if (next_opening_index > 0 and txt[next_opening_index - 1] == '!'):
            index = next_closing_index + 2
            continue
        
        # grab the text between the square brackets
        txt_between = txt[next_opening_index + 2:next_closing_index]
        index = next_closing_index - 2 # move index to end of matched brackets
        
        # handle links with different display text
        if ('|' in txt_between):
            txt_remaining = txt_between[txt_between.find("|") + 1:] 
            # adjust our index to handle the text being removed
            index = index - (len(txt_between) - len(txt_remaining))
            txt_between = txt_remaining
        
        # update our text
        txt = txt[0:next_opening_index] + txt_between + txt[next_closing_index + 2:]
    
    return txt

def main():
    # get text from clipboard
    clip_txt = pyperclip.paste()
    print(clip_txt)
    print('----------------------')

    unlinked_txt = unlink_text(clip_txt)

    # send the linked text to the clipboard
    pyperclip.copy(unlinked_txt)
    print(unlinked_txt)
    print('----------------------')
    print('unlinked text copied to clipboard')

if __name__ == "__main__":
    main()