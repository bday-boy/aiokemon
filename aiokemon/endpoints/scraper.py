# Packages this file uses: beautifulsoup4, requests
import keyword
import os
import re
from collections import deque
from typing import Generator, List

import requests
from bs4 import BeautifulSoup

type_map = {
    'integer': 'int',
    'boolean': 'bool',
    'string': 'str'
}
non_alpha = re.compile(r'[^a-z]')
class_declaration_header= re.compile(r'class ((?:[A-Z][a-zA-Z]*)+)')
classname = re.compile(r'([A-Z][a-zA-Z]*)+')


def really_lazy_sort(classes: List[str]) -> List[str]:
    # Get set of all classes used in each class
    classes_in_classes = deque(
        (class_, set(classname.findall(class_)))
        for class_ in classes
    )

    # Now pick up one class at a time and check if any other class declarations
    # contain that class. If none do, append it to sorted_classes. If any do,
    # add it back to the queue. Repeat this until the queue is empty.
    sorted_classes = []
    while classes_in_classes:
        is_depended_on = False
        class_decl, cur_set = classes_in_classes.popleft()
        cur_class = class_declaration_header.search(class_decl).group(1)
        for class_info in classes_in_classes:
            _, class_set = class_info
            if cur_class in class_set:
                is_depended_on = True
                break
        if is_depended_on:
            classes_in_classes.append((class_decl, cur_set))
        else:
            sorted_classes.append(class_decl)
    sorted_classes.reverse()
    return sorted_classes


def fix_resource_class(class_decl: str) -> str:
    index = class_declaration_header.search(class_decl).span(0)[1]
    return f'{class_decl[:index]}(PokeAPIResource){class_decl[index:]}'


def fix_name(td: BeautifulSoup) -> str:
    name = td.text
    if keyword.iskeyword(name):
        return f'{name}_'
    else:
        return name


def fix_type(td: BeautifulSoup) -> str:
    i = td.find('i')
    if i is None:
        return td.text
    main_type = i.text.split(' ')[0]
    main_type = type_map.get(main_type, main_type)
    if td.text.startswith('list '):
        return f'List[{main_type}]'
    else:
        return main_type


def parse_row(row: BeautifulSoup) -> str:
    cells = row.find_all('td')
    name = fix_name(cells[0])
    type_ = fix_type(cells[-1])
    return f'    {name}: {type_}'


def parse_table(table: BeautifulSoup) -> str:
    table_text = [f'class {table.previous_sibling.text.split(" ")[0]}:']
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        table_text.append(parse_row(row))
    return '\n'.join(table_text)


def gen_tables(resource_header: BeautifulSoup) -> Generator[BeautifulSoup, None, None]:
    node = resource_header.next_sibling
    while node and node.name != 'h3':
        if node.name == 'h4' and node.attrs.get('id'):
            node = node.next_sibling
            if node.name == 'table':
                yield node
            else:
                print('Some weird formatting occurred.')
                print(node.prettify())
        node = node.next_sibling


def parse_resource(resource_header: BeautifulSoup) -> str:
    file_text = (
        '# This file was generated automatically.\n'
        'from typing import List\n\n'
        'from aiokemon.core.api import PokeAPIResource\n'
        'from aiokemon.endpoints.common import *\n\n\n'
    )
    class_declarations = []
    for table in gen_tables(resource_header):
        class_declarations.append(parse_table(table))
    resource_class = class_declarations.pop(0)
    class_declarations = really_lazy_sort(class_declarations)
    file_text += (
        '\n\n\n'.join(class_declarations)
        + ('\n\n\n' if class_declarations else '')
        + fix_resource_class(resource_class)
        + '\n'
    )
    main_class = class_declaration_header.search(resource_class).group(1)
    return file_text, main_class


def parse_section(section_header: BeautifulSoup) -> None:
    dir_name = '_'.join(section_header["id"].split('-')[:-1])
    cur_dir = os.path.join('.', 'scraper', dir_name)
    if not os.path.isdir(cur_dir):
        os.mkdir(cur_dir)
    
    node = section_header.next_sibling
    while node and node.name != 'h2':
        if node.name == 'h3':
            file_name = non_alpha.sub('_', node['id'].lower())
            file_text, main_class = parse_resource(node)
            with open(os.path.join(cur_dir, f'{file_name}.py'), 'w') as f:
                f.write(file_text)
            with open(os.path.join(cur_dir, '__init__.py'), 'a') as f:
                f.write(
                    f'from aiokemon.endpoints.{dir_name}.{file_name} '
                    f'import {main_class}\n'
                )
        node = node.next_sibling
    
    with open(os.path.join('.', 'scraper', '__init__.py'), 'a') as f:
        f.write(f'from aiokemon.endpoints.{dir_name} import *\n')


def main():
    html_doc = requests.get('https://pokeapi.co/docs/v2').text
    soup = BeautifulSoup(html_doc, 'html.parser')

    if not os.path.isdir('./scraper'):
        os.mkdir('./scraper')

    # Ignore Resource Lists/Pagination section for now
    section_headers = soup.find_all(
        'h2', id=re.compile('(?<!resource-listspagination)-section')
    )

    for section_header in section_headers:
        parse_section(section_header)


if __name__ == '__main__':
    main()
