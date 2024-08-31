# Checking for predefined commands

# Opening programs - open [name from list]
# Opening books - open [name] book
# Opening chromium pages - open [name from list] page
# Googling - search [prompt]
# Updating system - update system

import re
import os
import json
import sys

#book_dict = {'deep learning' : '/home/kosenko/⬢/library/computer\\ sciences/machine\\ learning/advanced/DeepLearningBook.pdf'}

#page_dict = {'github': 'https://github.com/'}

#app_dict = {'chromium': 'org.chromium.Chromium',
#            'okular': 'okular',
#            'dolphin': 'dolphin'}

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


class CommandProcessing(object):
    def __init__(self, to_execute=None, changers=None, success_msg=None, failure_msg=None):
        self.to_execute = to_execute
        self.changers = changers
        self.success_msg = success_msg
        self.failure_msg = failure_msg

    def command_from_groups(self, groups):
        if self.changers is not None:
            result_groups = []
            for changer, group in zip(self.changers, groups):
                if changer is not None:
                    changed_group = changer.modify(group)
                    if changed_group is not None:
                        result_groups.append(changed_group)
                    else:
                        return None, self.failure_msg.format(*groups)
                else:
                    result_groups.append(group)
            return self.to_execute.format(*result_groups), self.success_msg.format(*groups)
        return self.to_execute.format(*groups), self.success_msg.format(*groups)

    def command_from_groups_execute(self, groups):
        command, msg = self.command_from_groups(groups)
        if command is not None:
            os.system(command)
        return msg


#command_dictionary = {
#    r'\bopen\b\s*(.*)\bbook\b': CommandProcessing('okular {0}', (ReplaceFromDict(book_dict),), '{0} book opened', '{0} book not found'),
#    r'\bopen\b\s*(.*)\bpage\b': CommandProcessing('org.chromium.Chromium {0}', (ReplaceFromDict(page_dict),), '{0} page opened', '{0} page not found'),
#    r'\bopen\b\s*(.*)': CommandProcessing('{0}', (ReplaceFromDict(app_dict),), '{0} opened', '{0} is unknown'),
#    r'\bsearch\b\s*(.*)': CommandProcessing('org.chromium.Chromium https://www.google.com/search?q={0}', (ReplaceString(' ', '+'),), 'searching {0}'),
#}

class TextProcessing(object):
    def __init__(self, command_dict, msg_not_found = None, stop_phrases=None, msg_goodbye='goodbye'):
        if stop_phrases is None:
            stop_phrases = ['stop jarvis']
        self.command_dict = command_dict
        self.msg_not_found = msg_not_found
        self.stop_phrases = stop_phrases
        self.msg_goodbye = msg_goodbye

    def process(self, text):
        for stop_phrase in self.stop_phrases:
            if stop_phrase == text.replace('.', '').strip().lower():
                return False, self.msg_goodbye, True
        for pattern in self.command_dict.keys():
            match_open = re.search(pattern, text, re.IGNORECASE)
            if match_open:
                groups = match_open.groups()
                item = self.command_dict[pattern]
                msg = item.command_from_groups_execute(groups)
                return False, msg, False
        else:
            return True, self.msg_not_found, False


def changer_from_config(changer_config, user_dicts):
    match changer_config[0]:
        case 'ReplaceFromDict':
            if user_dicts is None:
                print('user_dicts required for specifying other dicts')
                return None
            return ReplaceFromDict(user_dicts[changer_config[1]])
        case 'ReplaceString':
            return ReplaceString(changer_config[1], changer_config[2])
        case 'None':
            return None
        case _:
            print(changer_config[0], 'is an unknown changer')
            return None


def text_processing_from_config(config_file):
    if not os.path.isfile(config_file):
        print('warning: if you need to specify commands, write them in commands.json, but it\'s not necessary if you don\'t have commands')
        return TextProcessing({})
    with open (config_file, 'r') as f:
        configs = json.load(f)
    if 'command_dict' not in configs:
        print('command_dict not found in config file')
        return None
    command_dict = configs['command_dict']
    user_dicts = configs['user_dicts'] if 'user_dicts' in configs else None
    for key in command_dict.keys():
        command_dict[key] = CommandProcessing(
            to_execute = command_dict[key]['to_execute'] if 'to_execute' in command_dict[key] else None,
            changers = [changer_from_config(c, user_dicts) for c in command_dict[key]['changers']] if 'changers' in command_dict[key] else None,
            success_msg=command_dict[key]['success_msg'] if 'success_msg' in command_dict[key] else None,
            failure_msg=command_dict[key]['failure_msg'] if 'failure_msg' in command_dict[key] else None
        )
    msg_not_found = command_dict['msg_not_found'] if 'msg_not_found' in command_dict else None
    stop_phrases = command_dict['stop_phrases'] if 'stop_phrases' in command_dict else ['stop jarvis']
    msg_goodbye = command_dict['msg_goodbye'] if 'msg_goodbye' in command_dict else 'goodbye'
    return TextProcessing(command_dict, msg_not_found, stop_phrases, msg_goodbye)


#for experiments
if __name__ == '__main__':
    processing = text_processing_from_config('../commands.json')
    processing.process('search deep learning book')