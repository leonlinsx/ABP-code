# jetbrains Multilingual Online Translator
# pulls from reverso context site by sending a request and getting data
# uses CSS styles to pull correct words

import sys
import requests
from bs4 import BeautifulSoup

class OnlineTranslator:
    
    def __init__(self, lang_from, lang_to, word):
        self.lang = self.lang_dict()
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.word = word
        
    def main(self):
        """
        gets the lang_from, lang_to, word, opens a file to write the content to, and reads it
        :return:
        """
        # lang_from, lang_to, word = self.menu()
        data_list = self.website_get_all(self.lang_from, self.lang_to, self.word)

        with open(f"{self.word}.txt", "w", encoding="utf-8") as f:

            # since the dict is ordered, can just run through the index
            # alternative was to do this loop in website_get_all but i was lazy
            idx = 1
            for data in data_list:
                words, sentences = self.data_parse(data)

                f.write(self.format_words(self.lang[str(idx)], words))
                f.write("\n")
                f.write(self.format_sentences(self.lang[str(idx)], sentences))
                idx += 1

        # could open the file as read+write but i found this easier to understand
        # https://stackoverflow.com/questions/44901806/python-error-message-io-unsupportedoperation-not-readable
        with open(f"{self.word}.txt", "r", encoding="utf-8") as f:
            print(f.read())
        
    def menu(self):
        """
        takes user language choices, word choice, and returns string values
        keeps number input as str, but does not get the value from the dict
        :return string dict keys, word:
        """
        print("Hello, you're welcome to the translator. Translator supports:")
        # print enumerated menu of langs
        for key, value in self.lang.items():
            print(key + ". " + value.title())

        lang_from = input("Type the number of your language:\n")
        # lang_from = self.lang[lang_from] # was easier to just pull the keys since earlier methods use keys not values
        lang_to = input("Type the number of a language you want to translate to "
                        "or '0' to translate to all languages:\n")
        # lang_to = self.lang[lang_to]
        word = input("Type the word you want to translate:\n").lower()  # convert to lower just in case

        # print(f'You chose "{lang_to}" as the language to translate "{word}" to, from "{lang_from}".')

        return lang_from, lang_to, word

    def website_url(self, first_lang, sec_lang, word):
        """
        translation is from first_lang to sec_lang, params are str
        updated to use params as full language values and not dict keys

        :param first_lang:
        :param sec_lang:
        :param word:
        :return url to use:
        """
        base_url = "https://context.reverso.net/translation/"
        full_url = base_url + first_lang + "-" + sec_lang + "/" + word

        return full_url

    def website_get(self, url):
        """
        gets data from one website url based on url input
        :param url:
        :return requests data:
        """
        # need to spoof the user agent to get website to accept request
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
        # headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers)
        r.encoding = "utf-8"  # just in case needed

        # check status code
        if r.status_code == 200:
            print("200 OK")
        else:
            print(f"{r.status_code} ERROR")

        return r

    def website_get_all(self, lang_from, lang_to, word):
        """
        opens a session, and requests all data needed for all languages selected
        :param lang_from:
        :param lang_to:
        :param word:
        :return list of requests data:
        """
        # open a session to persist parameters https://requests.readthedocs.io/en/master/user/advanced/#session-objects
        s = requests.Session()
        # need to spoof the user agent to get website to accept request
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
        # headers = {"User-Agent": "Mozilla/5.0"}

        # unpack all keys if all translation selected; else just the one lang_to
        # updated to unpack all values
        if lang_to == "all":
            lang_list = list(self.lang.values())
        else:
            lang_list = [lang_to]

        r_list = []
        for lang in lang_list:
            url = self.website_url(lang_from, lang, word)  # create url for each language

            # if lang not in predefined list, exit
            if lang not in self.lang.values():
                print(f"Sorry, the program doesn't support {lang}")
                sys.exit()
            elif lang_from not in self.lang.values():
                print(f"Sorry, the program doesn't support {lang}")
                sys.exit()

            # try if word in reverso context's dictionary
            try:
                r = s.get(url, headers=headers)
                r.encoding = "utf-8"  # just in case needed

                # check for any non-working status code
                if r.status_code != 200:
                    # print(f"{r.status_code} ERROR")
                    print("Something wrong with your internet connection")
                    sys.exit()

            except:
                print(f"Sorry, unable to find {word}")
                sys.exit()

            r_list.append(r)

        return r_list

    def data_parse(self, data):
        """
        parses raw website data and returns 1) the list of words 2) list of sentences
        :param data:
        :return lists:
        """
        soup = BeautifulSoup(data.content, "html.parser")

        # https://www.w3schools.com/cssref/css_selectors.asp
        # this selects all elements under id #translations-content, with a tag, and class starting with translation
        words = soup.select('#translations-content a[class^="translation ltr dict"]')
        # this selects all elements under id #examples-content, with span tag and text class attribute
        sentences = soup.select("#examples-content span.text")

        # some alternatives
        # translations = soup.select('.translation')
        # examples = soup.select('.example > .ltr')
        # examples = list(filter(None, examples))

        no_tag_words = [word.text for word in words]
        no_tag_sentences = [sentence.text for sentence in sentences]

        clean_words = [word.replace("\n", "").strip() for word in no_tag_words]
        clean_sentences = [sentence.replace("\n", "").strip() for sentence in no_tag_sentences]

        return clean_words, clean_sentences

    def format_words(self, lang, word_list):
        """

        :param lang:
        :param word_list:
        :return formatted text:
        """
        text = f"{lang.title()} Translations:\n"
        for word in word_list:
            text += word.replace("'", "")
            text += "\n"

        return text

    def format_sentences(self, lang, sentence_list):
        """

        :param lang:
        :param sentence_list:
        :return formatted text:
        """
        text = f"{lang.title()} Examples:\n"
        for i, sentence in enumerate(sentence_list):
            text += sentence.replace('"', '')
            text += "\n"
            if i % 2 != 0:
                text += "\n"  # extra line break between setence pairs

        return text

    def lang_dict(self):
        """
        key value pairs for numerical input to url part
        :return short form to long form dict:
        """
        return {'1': 'arabic',
                '2': 'german',
                '3': 'english',
                '4': 'spanish',
                '5': 'french',
                '6': 'hebrew',
                '7': 'japanese',
                '8': 'dutch',
                '9': 'polish',
                '10': 'portuguese',
                '11': 'romanian',
                '12': 'russian',
                '13': 'turkish'
        }
    
if __name__ == "__main__":
    ot = OnlineTranslator(sys.argv[1], sys.argv[2], sys.argv[3])
    # ot = OnlineTranslator("english", "all", "hello")
    ot.main()