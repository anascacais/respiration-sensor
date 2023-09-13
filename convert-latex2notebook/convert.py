# built-in
import os

# third-party
from nbformat.v4 import new_notebook
import nbformat

# local
from cell_contents import add_cell, get_banners, get_header_and_body, get_header_info
from latex_parsing import remove_comments, parse_itemize, parse_enumerate, parse_sections, parse_text_formatting, parse_code, parse_quotes

###################################################################################

file_name = 'B011 Working with Arduino and Digital Interfaces'
latex_folder_dir = f'/Users/anasofiacc/Downloads/{file_name}'

with open(os.path.join(latex_folder_dir, 'main.tex')) as f:
    latex_lines = [line.strip() for line in f.readlines()]

nb = new_notebook() 

top_banner, bottom_banner = get_banners()
add_cell(top_banner, 'md', nb)

###################################################################################

header, body = get_header_and_body(latex_lines, sod_str='% document', eod_str='% bottom banner')

header = parse_itemize(header)
header = parse_enumerate(header)

header_info = get_header_info(header)

add_cell(header_info['title'], 'md', nb)
add_cell(header_info['keywords'], 'md', nb)
add_cell(header_info['notebook info'], 'md', nb)
add_cell(header_info['description'], 'md', nb)
add_cell(header_info['materials'], 'md', nb)
add_cell('***', 'md', nb)


body = remove_comments(body)

body = parse_text_formatting(body)
body = parse_itemize(body)
body = parse_enumerate(body)
body = parse_sections(body)
# body = parse_figures(body)
body = parse_quotes(body)
body = parse_code(body)

body_items = body.split('```')
for i, item in enumerate(body_items):
    if i % 2 == 0:
        add_cell(item, 'md', nb)
    else:
        add_cell(item, 'code', nb)


###################################################################################

add_cell('***', 'md', nb)
add_cell(bottom_banner, 'md', nb)

# save the notebook to a file
with open('test_notebook.ipynb', 'w') as f:
	nbformat.write(nb, f)