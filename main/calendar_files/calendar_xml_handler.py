import xml.etree.ElementTree


def calendar_xml_handler(theyear):
    days = xml.etree.ElementTree.parse(f'main/calendar_files/calendar{theyear}.xml').getroot().find('days')
    v = []
    for _ in range(len(days)):
        v.append(days[_].attrib)
    return v


