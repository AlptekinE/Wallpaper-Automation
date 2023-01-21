import re
from utils import Calendar_Get


def _regex_sil(regex_part):
    the_regex = re.compile("".join(["\t", regex_part, "\[[^]]*]"]))  # \[[^}]+]
    print(the_regex)
    with open('Wallpaper File Location/schedule+notes.js', 'r') as myfile:
        data = myfile.read()
        data = re.sub(the_regex, "\t\"Notes\": []", data)
        print(data)
        with open('Wallpaper File Location/schedule+notes.js', 'w') as newfile:
            newfile.write(data)


_regex_sil("\"Notes\": ")


def _regex_ekle(etkinlik):
    the_regex = re.compile("".join(["\t", "\"Notes\": []", "\[[^]]*]"]))
    with open('Wallpaper File Location/schedule+notes.js', 'r') as myfile:
        data = myfile.read()
        data = re.sub(the_regex, etkinlik, data)
        print(data)
        with open('Wallpaper File Location/schedule+notes.js', 'w') as newfile:
            newfile.write(data)


events = str(Calendar_Get._get_event())
events = "\t\"Notes\": " + events
events = events.replace("'", "\"")
events = events.replace(",", ",\n")
events = events.replace("]", "\n]")
print(events)

_regex_ekle(events)
