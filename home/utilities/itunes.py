# -*- coding: utf-8 -*-
import re
import json
import codecs

__author__ = 'Jon Nappi'


def replace_trailing_commas(match_obj):
    """Replace commas in matched regexes"""
    print(match_obj)
    return match_obj.group(0).replace(',', '')


def create_dict(match_obj):
    return '{%s}' % match_obj.group('body')


def create_key(match_obj):
    return '"%s":' % match_obj.group('body')


def create_int(match_obj):
    return '%s,' % match_obj.group('body')


def create_date(match_obj):
    return '"%s",' % match_obj.group('body')


def create_string(match_obj):
    print('create_string')
    return '"%s",' % match_obj.group('body').replace('"', '\"')


def create_bool(match_obj):
    return '%s,' % match_obj.group('body')


def main():
    xml = ''
    with codecs.open('/Users/Jon/Desktop/iTunes Music Library.xml', 'r', 'utf-8') as f:
        xml = f.read()
    xml = '\n'.join(xml.split('\n')[3:-2])

    comma_pattern = r'[,]\n\s*}'
    dict_pattern = r'<dict>(?P<body>.*)</dict>'
    key_pattern = r'<key>(?P<body>.*)</key>'
    int_pattern = r'<integer>(?P<body>.*)</integer>'
    date_pattern = r'<date>(?P<body>.*)</date>'
    string_pattern = r'<string>(?P<body>.*)</string>'
    bool_pattern = r'<(?P<body>true|false)/>'
    patterns = [(dict_pattern, create_dict),
                (key_pattern, create_key), (int_pattern, create_int),
                (date_pattern, create_date), (string_pattern, create_string),
                (bool_pattern, create_bool),
                (comma_pattern, replace_trailing_commas)]

    for pattern, function in patterns:
        xml = re.sub(pattern, function, xml)
    xml = xml.replace('<dict>', '{').replace('</dict>', '},')
    xml = xml.replace(',\n\t\t}', '\n\t\t}')
    with codecs.open('/Users/Jon/Desktop/iTunes Music Library.json', 'w', 'utf-8') as f:
        f.write(xml)
    xml_dict = json.loads(xml)
    print(len(xml_dict))


if __name__ == '__main__':
    main()
