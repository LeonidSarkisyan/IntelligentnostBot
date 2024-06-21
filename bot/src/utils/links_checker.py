import re


def check_links(input_string):
    pattern = r'https://\S+'

    matches = re.findall(pattern, input_string)

    return len(matches) == len(input_string.split())
