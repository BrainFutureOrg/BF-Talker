# Description
Brain Future Talker is a simple voice assistant which can answer your questions and execute commands. Question answering is powered by LLM, while commands are executed only on pattern match specified by user, to prevent surprise actions.
# Before usage
Requirements for this project are listed in ```requirements.txt```. First start of assistant may be slow because of weight downloading.
# Usage
## Default
Run ```main.py```. Configuration files are not required. Say "Hey, Jarvis", ask questions, receive answers. To stop assistant, instead of question say "Stop Jarvis".
## Add your configs
Add configuration json file. By default code tries to find ```config.json``` in project directory, but you can specify different path with ```-c```/```--config``` flag. Allowed entries are:
- ```use_hey_Jarvis``` : y/n - whether to use wake word detection (to make assistant less resource consuming by starting on "Hey, Jarvis") or no;
- ```commands_json``` : path - path to json with command configs.
## Add your commands
Add json file structure described below. By default code tries to find ```commands.json``` in project directory, but you can specify your path in ```config.json``` as ```commands_json``` entry. File entries:
- ```command_dict``` : dict of dicts - required entry, specifies all commands which can be executed by program. Entries from dict must have regex as key (which is matched and groups of text are extracted from users speech) and command properties dict as value which must have following entries:
    - ```to_execute``` : command to run in terminal, with ```{number}``` placeholders to insert specific extracted groups;
    - ```changers``` : list of changers of length same as group number, each changer is a list having class name and additional strings. Class name can be:
        - ```ReplaceFromDict``` - replaces group with entry from dict. Second element from list must be name of custom dict (described below);
        - ```ReplaceString``` - replaces all occurances of one substring with other in group. Next two elements in list must be string to replace and string that is a replacement;
        - ```None``` - no change occurs;
    - ```success_msg``` : message to output on successful command identification, with ```{number}``` placeholders to insert specific extracted groups;
    - ```failure_msg``` : message to output on failed command identification, with ```{number}``` placeholders to insert specific extracted groups;
- ```user_dicts``` : dict of dicts for every user-specified dict, for example for ```ReplaceFromDict```, this entry is not required if you don't specify any additional dicts.
- ```stop_phrases``` : list of phrases in lowercase - list of phrases on which assistant stops;
- ```msg_not_found``` : string - message to output on no regex match;
- ```msg_goodbye``` : string - message to output on stop phrase before exiting.
# Inner working
Assistant has following components:
- Wake word detectionCode waits until user says "Hello, Jarvis" (if user didn't disable it in config). We used [openWakeWord](https://github.com/dscripka/openWakeWord);
- Text-to-speech translates user utterance into string. We used [Whisper](https://github.com/openai/whisper);
- Regex match is used for deciding what command to execute. Commands are specified by user to prevent surprises;
- Asking question to LLM happens if no match happened on previous step. We used [LLaMA](https://github.com/abetlen/llama-cpp-python);
- Speech-to-text creates audio from whatever text was created on previous steps. We used [gTTS](https://github.com/pndurette/gTTS).