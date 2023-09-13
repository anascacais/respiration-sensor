# third-party
import re
from nbformat.v4 import new_markdown_cell, new_code_cell

# local
from string_aux_functions import try_search, find_str_in_list


def add_cell(content, type, nb):
    if type == 'md':
        nb['cells'].append(new_markdown_cell(content))
    else:
        nb['cells'].append(new_code_cell(content))
    return nb


def get_header_and_body(latex_lines, sod_str='% document', eod_str='% bottom banner'):
    '''
     Returns
     -------
     header: str
        Full header in string format
     body: str
        Full body in string format
     ''' 
    
    sod = find_str_in_list(sod_str, latex_lines)[0] + 1
    eod = find_str_in_list(eod_str, latex_lines[sod:])[0] + sod + 1

    header = '\n'.join(latex_lines[:sod])
    body = '\n'.join(latex_lines[sod:eod])

    return header, body


def get_banners():

    top_banner = '![scientisst-notebooks_top-banner](https://raw.githubusercontent.com/scientisst/notebooks/59632d3d477981a3b1cc12157e12bbdcdb45def8/_Resources/top-banner.png)'
    bottom_banner = '![scientisst-notebooks_bottom-banner](https://raw.githubusercontent.com/scientisst/notebooks/59632d3d477981a3b1cc12157e12bbdcdb45def8/_Resources/bottom-banner.png)'

    return top_banner, bottom_banner



def get_header_info(header):
    '''
     Returns
     -------
     header: dict
        Dictionary with the content of the header, with the keys: title, author, date creation, abstract, keywords, description, and respective values (already formatted)
     ''' 
    
    header_info = {}

    # parse info
    header_info['title'] = try_search(r'\\title{(.*)}', header)
    header_info['keywords'] = [f'`{k}`' for k in re.findall(r'\\texttt{([^}]*)}', header)]
    header_info['author'] = try_search(r'\\author{(.*)}', header)                  
    header_info['date creation'] = try_search(r'\\datecreation{(.*)}', header)
    header_info['date update'] = try_search(r'\\dateupdate{(.*)}', header)
    header_info['description'] = try_search(r'\\intro{(.*)}', header)
    header_info['materials'] = try_search(r'\\materials{(.*)}', header)

    # format info
    header_info['title'] = f'# <span style="color:#484848;"> {header_info["title"]} </span>'
    header_info['keywords'] = ', '.join(header_info['keywords'])
    header_info['author'] = f'**Contributor(s):** {header_info["author"]}'
    header_info['date creation'] = f'**Date of creation:** {header_info["date creation"]}'
    header_info['date update'] = f'**Last update:** {header_info["date update"]}'

    # return header formatted
    header_info['keywords'] = f'### <span style="color:#00aba1;"> Keywords </span>\n{header_info["keywords"]}'
    header_info['notebook info'] = f'### <span style="color:#00aba1;"> Notebook Info </span>\n{header_info["author"]}\n\n{header_info["date creation"]}\n\n{header_info["date update"]}'
    header_info['description'] = f'### <span style="color:#00aba1;"> Description </span>\n{header_info["description"]}'
    header_info['materials'] = f'### <span style="color:#00aba1;"> Materials </span>\n{header_info["materials"]}'

    return header_info
