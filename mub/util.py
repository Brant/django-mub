"""
Utility functions for MUB
"""
import os
import re


def massage_css_images_for_cache_path(css_contents, css_url):
    """
    When we cache the CSS, it changes the structure of where the images sit, 
        relative to the cache'd sheet
    """
    
    if not css_url.endswith("/"):
        css_url += "/"
    
    # remove spaces
    css_contents = css_contents.replace("url (", "url(")
    
    # regex an absolute path into URLs that qualify        
    css_contents = re.sub(r'url\(("|\')?([^"\'(https?\:)(//)])([^")]+)("|\')?\)', r'url("%s\2\3")' % css_url, css_contents)
    
    # remove any double quotes at the end of url lines
    css_contents = css_contents.replace("'\")","\")")
    
    return css_contents


def latest_timestamp(files):
    """
    Get the timestamp for the latest modified file in a list of files
    """
    latest_mod = 0
    for a_file in files:
        file_mod = os.path.getmtime(a_file)
        if file_mod > latest_mod:
            latest_mod = file_mod
    return latest_mod
