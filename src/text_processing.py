# Checking for predefined commands

# Opening programs - open [name from list]
# Opening books - open [name] book
# Opening chromium pages - open [name from list] page
# Googling - search [prompt]
# Updating system - update system

import re
import os

book_dict = {'deep learning' : '/home/kosenko/⬢/library/computer\\ sciences/machine\\ learning/advanced/DeepLearningBook.pdf'}

page_dict = {'github': 'https://github.com/'}

app_dict = {'chromium': 'org.chromium.Chromium',
            'okular': 'okular',
            'dolphin': 'dolphin'}

class TextModifier(object):
    def modify(self, text):
        pass


class ReplaceFromDict(TextModifier):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def modify(self, text):
        text = text.strip().lower()
        if text in self.dictionary:
            return self.dictionary[text]
        else:
            return None


class ReplaceString(TextModifier):
    def __init__(self, to_replace, replace_by):
        self.to_replace = to_replace
        self.replace_by = replace_by

    def modify(self, text):
        return text.replace(self.to_replace, self.replace_by)


command_dictionary = {
    r'\bopen\b\s*(.*)\bbook\b': ('okular {0}', (ReplaceFromDict(book_dict),)),
    r'\bopen\b\s*(.*)\bpage\b': ('org.chromium.Chromium {0}', (ReplaceFromDict(page_dict),)),
    r'\bopen\b\s*(.*)': ('{0}', (ReplaceFromDict(app_dict),)),
    r'\bsearch\b\s*(.*)': ('org.chromium.Chromium https://www.google.com/search?q={0}', (ReplaceString(' ', '+'),)),
}

class TextProcessing(object):
    def __init__(self):
        pass

    def apply_change(self, text, changer):
        if changer is None:
            return text
        if isinstance(changer, TextModifier):
            return changer.modify(text)

    def process(self, text):
        for pattern in command_dictionary.keys():
            match_open = re.search(pattern, text, re.IGNORECASE)
            if match_open:
                groups = match_open.groups()
                item = command_dictionary[pattern]
                if item is None:
                    pass
                elif isinstance(item, str):
                    command = item.format(*groups)
                    print(command)
                    os.system(command)
                elif isinstance(item, tuple):
                    changed_text = []
                    is_okay = True
                    for group, changer in zip(groups, item[1]):
                        changed = self.apply_change(group, changer)
                        if changed is not None:
                            changed_text.append(changed)
                        else:
                            is_okay = False
                            break
                    if is_okay:
                        command = item[0].format(*changed_text)
                        print(command)
                        os.system(command)
                    else:
                        print('transformation was not possible')
                break
        else:
            print('command not found')