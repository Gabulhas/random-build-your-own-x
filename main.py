import re
import sys
import random
import os
import urllib.request

plus_symbol = "[\x1b[32m+\x1b[0m]"
minus_symbol = "[\x1b[31m-\x1b[0m]"
info_symbol = "[\x1b[33m=\x1b[0m]"

arguments = sys.argv[1:]


def quit_program():
    print(info_symbol + " REQUIRED ARGUMENTS: <LANGUAGE>(exp:OCaml, Python) <R(andom) or A(ll)>")
    exit(1)


if len(arguments) < 2:
    quit_program()
if arguments[1] != "R" and arguments[1] != "A":
    quit_program()

print(
    info_symbol + "Fetching latest version of https://github.com/danistefanovic/build-your-own-x/blob/master/README"
                  ".md\n")

dir_path = os.path.dirname(os.path.realpath(__file__))

url = 'https://raw.githubusercontent.com/danistefanovic/build-your-own-x/master/README.md'
urllib.request.urlretrieve(url, os.path.join(dir_path, "source.txt"))

filepath = "source.txt"
all_languages = {}

language_regex = re.compile('(?<=\[\*\*)(.*)(?=\*\*)')

trash_chars = re.compile('\*.*\: |([\_\]])')


def pretty_print(text: str) -> str:
    return (trash_chars.sub("", str(language_regex.sub("", text.strip())))).strip()


with open(filepath, encoding='utf-8', errors='ignore') as fp:
    line = fp.readline()
    totalLines = 1
    while line:
        match_in_line = language_regex.search(line)
        if match_in_line is None:
            line = fp.readline()
            continue
        language = match_in_line.group()
        # print("Line {}:{}".format(totalLines, line.strip()))
        # print("Language {}".format(language))
        if language not in all_languages:
            all_languages[language] = []
        all_languages[language].append(line)
        totalLines += 1
        line = fp.readline()

if arguments[0] not in all_languages:
    print(minus_symbol + " Couldn't find any Tutorial for your language")
    exit(1)

if arguments[1] == "A":
    for line in all_languages[arguments[0]]:
        print(plus_symbol + " " + pretty_print(line))
elif arguments[1] == "R":
    result = all_languages[arguments[0]]
    print(plus_symbol + " " + pretty_print(result[random.randrange(0, len(result))]))
