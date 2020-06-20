import xml.etree.ElementTree
import os
import pickle


def uploaded_file_check(file):
    if file.content_type != 'text/xml':
        return "Неправильный xml-файл"
    with open('main/calendar_files/temp.xml', 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    try:
        year = xml.etree.ElementTree.parse('main/calendar_files/temp.xml').getroot().attrib.get('year')
    except xml.etree.ElementTree.ParseError:
        return "Неправильный xml-файл"
    with open('main/calendar_files/presented_years.txt', 'rb+') as li:
        v = pickle.load(li)
        if int(year) in v:
            return "Такой файл уже существует"
        else:
            v.append(int(year))
            v.sort()
    with open('main/calendar_files/presented_years.txt', 'wb+') as li:
        pickle.dump(v, li)
    os.rename(r'main/calendar_files/temp.xml', r'main/calendar_files/calendar' + year + '.xml')
    return False


def handle_uploaded_file(file):
    pass


def rewrite():
    year = xml.etree.ElementTree.parse('main/calendar_files/temp.xml').getroot().attrib.get('year')
    with open('main/calendar_files/temp.xml', 'rb+') as f:
        a = f.readlines()
    with open('main/calendar_files/calendar' + year + '.xml', 'wb+') as n:
        for line in a:
            n.write(line)
    os.remove('main/calendar_files/temp.xml')
