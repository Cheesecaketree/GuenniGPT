#!/usr/bin/env python
"""
https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b

Remove emoji from a text file and print it to stdout.
Usage
-----
    python remove-emoji.py input.txt > output.txt
"""
import re
import sys

# https://stackoverflow.com/a/49146722/330558
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

