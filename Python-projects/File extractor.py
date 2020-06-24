# extracts all html files from a directory, opens them, gets the text body, and compiles everything into a txt file
# also gets the most frequent words and their count
from bs4 import BeautifulSoup
from collections import Counter
import os, glob

dir_path = 'C:\\Users\\Leon\\Desktop\\posts' # path of posts
result_file = open("results.txt", "wb")  # write, binary
os.chdir(dir_path)  

# https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/
# os.path.join to get all files in that dir with *.html; glob to find the files
for file_name in glob.glob(os.path.join(dir_path, "*.html")):
	with open(file_name, encoding="utf-8") as html_file:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# use bs4 to parse the html doc, get the readable text
# then write to result_file
		soup = BeautifulSoup(html_file, "html.parser")
		text_body = soup.get_text()
		result_file.write(text_body.encode('utf-8'))
result_file.close()

# get the top 100 words, and their count, in 2 separate lists
with open(os.path.join(dir_path, "results.txt"), encoding="utf-8") as file:
	text = file.read().split()
	word_counts = Counter(text)
	top_list = dict(word_counts.most_common(100))
	(keys, values) = zip(*top_list.items())
	print(keys)
	print(values)


