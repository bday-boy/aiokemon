"""
This file is used to scrape the PokeAPI docs page for type-hinting purposes.
Python modules are then generated and put into the endpoints directory.
The code is ugly but idc it gets the job done lmao web scraping isn't exactly
very pretty anyway

Packages this file uses: beautifulsoup4, requests
"""

import keyword
import re
from collections import deque
from pathlib import Path
from typing import Generator, List

import requests
from bs4 import BeautifulSoup

type_map = {
    'integer': 'int',
    'boolean': 'bool',
    'string': 'str'
}
non_alpha = re.compile(r'[^a-z]')
class_declaration_header = re.compile(r'class ((?:[A-Z][a-zA-Z]*)+)')
classname = re.compile(r'([A-Z][a-zA-Z]*)+')
endpoints_dir = Path('.') / 'endpoints'


def really_lazy_sort(classes: List[str]) -> List[str]:
    """Sorts a list of class declarations so that each class's dependencies
    are declared before it.
    """
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


def all_from_list(all_list: List) -> List:
    """Formats an __all__ list so it can be written into a file."""
    all_formatted = ',\n    '.join(f"'{entry}'" for entry in all_list)
    return f'\n__all__ = [\n    {all_formatted}\n]\n'


def fix_resource_class(main_class: str) -> str:
    """Inserts "(PokeAPIResource)" into the main class declaration of a
    resource.
    """
    index = class_declaration_header.search(main_class).span(0)[1]
    return f'{main_class[:index]}(PokeAPIResource){main_class[index:]}'


def fix_name(td: BeautifulSoup) -> str:
    """Parses a table cell as a class attribute. Adds a trailing underscore
    to Python keywords.
    """
    name = td.text
    if keyword.iskeyword(name):
        return f'{name}_'
    else:
        return name


def fix_type(td: BeautifulSoup) -> str:
    """Parses a table cell as a type declaration."""
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
    """Converts a single row into a name-type pair."""
    cells = row.find_all('td')
    name = fix_name(cells[0])
    type_ = fix_type(cells[2])
    return f'    {name}: {type_}'


def parse_table(table: BeautifulSoup) -> str:
    """Converts a table into a class declaration as a string."""
    table_text = [f'class {table.previous_sibling.text.split(" ")[0]}:']
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        table_text.append(parse_row(row))
    return '\n'.join(table_text)


def gen_tables(resource_header: BeautifulSoup
               ) -> Generator[BeautifulSoup, None, None]:
    """Gets all the tables in a resource section. Starts at the resource
    header and ends when no siblings or left or when another resource header
    is encountered.
    """
    node = resource_header.next_sibling
    while node and node.name != 'h3':
        if node.name == 'h4' and node.attrs.get('id'):
            node = node.next_sibling
            if node.name == 'table':
                yield node
            else:
                # PokeAPI always seems to have an h4 followed by a table, so
                # if we didn't get a table, then there's some sort of exception
                print('Some weird formatting occurred.')
                print(node.prettify())
        node = node.next_sibling


def parse_resource(resource_header: BeautifulSoup) -> str:
    """Parses all of the tables in a single resource."""
    file_text = (
        '# This file was generated automatically.\n'
        'from typing import List\n\n'
        'from aiokemon.core.api import PokeAPIResource\n'
        'from aiokemon.endpoints.utility.common_models import *\n\n\n'
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


def parse_section(section_header: BeautifulSoup) -> str:
    """Parse all of the endpoints in a given section. Each endpoint becomes
    a Python module and the section becomes a package.
    """
    pkg_name = '_'.join(section_header["id"].split('-')[:-1])
    pkg_dir = endpoints_dir / pkg_name
    if not pkg_dir.is_dir():
        pkg_dir.mkdir()

    section_classes = []
    node = section_header.next_sibling
    while node and node.name != 'h2':
        if node.name == 'h3':
            module_name = non_alpha.sub('_', node['id'].lower())
            file_text, main_class = parse_resource(node)

            # Write the class declarations to our module
            with (pkg_dir / f'{module_name}.py').open('w') as f:
                f.write(file_text)

            # Import the main class into our __init__.py file
            with (pkg_dir / '__init__.py').open('a') as f:
                f.write(
                    f'from aiokemon.endpoints.{pkg_name}.{module_name} '
                    f'import {main_class}\n'
                )
            section_classes.append(main_class)
        node = node.next_sibling

    # Import all main classes from our current package into the top-level
    # endpoints __init__.py file
    with (endpoints_dir / '__init__.py').open('a') as f:
        f.write(f'from aiokemon.endpoints.{pkg_name} import *\n')

    # Add the __all__ array to our current package's __init__.py
    with (pkg_dir / '__init__.py').open('a') as f:
        f.write(all_from_list(section_classes))

    return section_classes


def main():
    html_doc = requests.get('https://pokeapi.co/docs/v2').text
    soup = BeautifulSoup(html_doc, 'html.parser')

    if not endpoints_dir.is_dir():
        endpoints_dir.mkdir()

    section_headers = soup.find_all(
        'h2', id=re.compile('.+-section')
    )

    # Ignore Resource Lists/Pagination and Utility sections for now
    section_headers.pop(0)
    section_headers.pop(-1)

    all_resource_classes = []
    for section_header in section_headers:
        all_resource_classes.extend(parse_section(section_header))

    with (endpoints_dir / '__init__.py').open('a') as f:
        f.write(all_from_list(all_resource_classes))


if __name__ == '__main__':
    main()
