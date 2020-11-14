# Jetbrains text-based browser course
# pulls data from an input site with requests
# parses the data with beautifulsoup

import sys, os
import requests
import re

from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore, Style

class Browser:

    def __init__(self, dir):
        # directory for saved tabs
        if not os.path.exists(dir):
            os.mkdir(dir)
        self.dir = dir
        # for browser history
        self.curr_pg = None
        self.pg_history = deque()

        self.main()

    def main(self):
        while True:
            text = input()
            if text == "exit":
                self.exit()
            # when the user types back, you should output the page that was before the current one.
            elif text == "back":
                if self.pg_history:
                    content = self.website_output(self.pg_history.pop())
                    print(content)
                    continue
                else:
                    continue

            protocol, domain, top = self.website_parse(text)

            # check if the string corresponds to the name of any file with a web page you saved before.
            # If it does, print the content of this file.
            # os.listdir only lists the filenames, not the full path
            # e.g. ['bloomberg', 'nytimes']
            if domain in os.listdir(self.dir):
                self.file_output(domain, self.dir)
                continue
            # elif check if valid url with >= one dot
            # if valid url, print content and save it to file in directory
            elif self.website_check(domain, top):
                content = self.website_output(protocol, domain, top)
                print(content)
                self.website_to_file(domain, content, self.dir)
            else:
                print("Error: Incorrect URL")
                continue

            # if there's a current page from loop before this, add to stack
            # then update to the current page for this loop
            # note we do this with "lag of one" since have to see if user entered "back"
            if self.curr_pg:
                self.pg_history.append(self.curr_pg)
            self.curr_pg = content

    # takes a string url and returns it split into three parts
    # we have 3 capturing groups, for (1) http, (2) domain w/o .com, and (3) .com
    # e.g. https://bloomberg.com becomes bloomberg
    # https://stackoverflow.com/questions/569137/how-to-get-domain-name-from-url
    def website_parse(self, text):
        regex = re.compile(r"(http:\/\/|https:\/\/)?(.*)(\.com|\.net|\.org|\.info|\.coop|\.int)")
        matches = regex.findall(text)

        if matches:
            return matches[0][0], matches[0][1], matches[0][2]
        else:
            return "", text, ""

    # takes protocol, domain, top-level domain
    # get info from the combined url
    # returns the content in UTF-8 encoding
    # https://2.python-requests.org/en/master/user/quickstart/
    def website_output(self, protocol, domain, top):
        # add protocol if none, concatenate full url
        if not protocol:
            protocol = "https://"
        full_url = protocol + domain + top

        try:
            r = requests.get(full_url)
            r.encoding = "UTF-8"

            # unsure why .content and not .text, think it's because html parsing
            soup = BeautifulSoup(r.content, 'html.parser')

            content = ""
            wanted_tags = ('p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6')
            for tag in wanted_tags:
                all_tags = soup.find_all(tag)
                for i in range(len(all_tags)):
                    text = f"{all_tags[i].get_text().strip()} + \n"
                    # only blue if is a link
                    if tag == "a":
                        content += Fore.BLUE + text
                    else:
                        content += Style.RESET_ALL + text

            # deprecated due to new stage reqs
            # returns all the text in a document or beneath a tag, as a single Unicode string
            return content

        except requests.exceptions.ConnectionError:
            print("Error: Incorrect URL")

    # check if user entered valid url and return boolean
    # since we're using the regex, it needs to have both domain and top-level domain
    # the protocol is optional
    # e.g. bloomberg is invalid, bloomberg.com is valid,
    # http://bloomberg is invalid, http://bloomberg.com is valid
    def website_check(self, domain, top):
        if domain and top:
            return True
        else:
            return False

    # takes domain w/o top-level, content and saves to file in the passed directory
    # already split the domain from the parser above
    # This way, the file for the page bloomberg.com will be named bloomberg
    # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
    def website_to_file(self, domain, content, dir):
        file_name = os.path.join(dir, domain)
        with open(file_name, "w") as f:
            f.write(content)

    # takes a filename (not a path), dir and prints the content
    def file_output(self, file_name, dir):
        file_name = os.path.join(dir, file_name)
        with open(file_name, "r") as f:
            print(f.read())

    def exit(self):
        sys.exit()

if __name__ == "__main__":

    dir = sys.argv[1]
    Browser(dir)

