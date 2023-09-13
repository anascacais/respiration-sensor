# third-party
import re

# local 
from string_aux_functions import try_search

def parse_text_formatting(test_string):

    bold_items = re.findall(r'\\textbf{([^}]*)}', test_string)
    for bold_item in bold_items:
        test_string = test_string.replace(f'\\textbf{{{bold_item}}}', f'**{bold_item}**')

    italic_items = re.findall(r'\\textit{([^}]*)}', test_string)
    for italic_item in italic_items:
        test_string = test_string.replace(f'\\textit{{{italic_item}}}', f'*{italic_item}*')

    texttt_items = re.findall(r'\\texttt{([^}]*)}', test_string)
    for texttt_item in texttt_items:
        test_string = test_string.replace(f'\\texttt{{{texttt_item}}}', f'`{texttt_item}`')

    test_string = test_string.replace('\\_', '_')

    return test_string

def parse_enumerate(test_string): # TODO: substitutes by itemize
    '''
     Returns
     -------
     test_string: str
        Original string with itemize format removed
     '''

    test_string = test_string.replace('\\begin{enumerate}', '')
    test_string = test_string.replace('\\end{enumerate}', '')
    test_string = test_string.replace('\\item', '- ')

    return test_string


def parse_itemize(test_string):
    '''
    Returns
    -------
    test_string: str
    Original string with itemize format removed
    '''
    
    test_string = test_string.replace('\\begin{itemize}', '')
    test_string = test_string.replace('\\end{itemize}', '')
    test_string = test_string.replace('\\item', '- ')

    return test_string

def parse_sections(test_string):

    section_titles = re.findall(r'\\section{([^}]*)}', test_string)
    for i,title in enumerate(section_titles):
        test_string = test_string.replace(f'\\section{{{title}}}', f'# <span style="color:#00aba1;"> {i+1}. {title.strip()} </span>')


    subsection_titles = re.findall(r'\\subsection{([^}]*)}', test_string)
    for i,title in enumerate(subsection_titles):
        test_string = test_string.replace(f'\\subsection{{{title}}}', f'## <span style="color:#484848;"> {title.strip()}  </span>')

    
    subsubsection_titles = re.findall(r'\\subsubsection{([^}]*)}', test_string)
    for i,title in enumerate(subsubsection_titles):
        test_string = test_string.replace(f'\\subsection{{{title}}}', f'##### <div style="color:#484848"> {title.strip()} </div>')

    return test_string



def parse_code(test_string):
    
    code_items = re.findall(r'\\begin{lstlisting}\[language=C\+\+\]([^?!]*)\\end{lstlisting}', test_string)

    for code_item in code_items:
        test_string = test_string.replace(f'\\begin{{lstlisting}}[language=C++]{code_item}\\end{{lstlisting}}', f'```\n{code_item}\n```')
    
    return test_string


def parse_figures(test_string):

    figures = re.findall(r'\\begin{figure}([^?]*)\\end{figure}', test_string)

    for i, figure in enumerate(figures):
        caption = try_search(r'\\caption{([^}]*)}', figure)
        figure_path = try_search(r'\\includegraphics\[width=\d{0,2}\.\d{0,2}\\linewidth\]{([^?!]*.png|jpg|pdf|jpeg)}', figure)
        # 
        #\\includegraphics\[width=\d\.\d\\linewidth\]{([^?!]*.png|jpg|pdf|jpeg)}

        test_string.replace(
            f'\\begin{{figure}}{figure}\\end{{figure}}',
            f'<img src="{figure_path}" width="500" border="0"> <p style="color:#484848;text-align:center"> <i> Figure {i+1}: {caption} </i> </p>'
        )
        
    return test_string



def parse_quotes(test_string):
    '''
    Returns
    -------
    test_string: str
    Original string with quote format removed
    '''

    test_string = test_string.replace('\emojiflash', '⚡')
    test_string = test_string.replace('\emojiwarning', '⚠️')
    test_string = test_string.replace('\emojiwrite', '✏️')

    quotes = re.findall(r'\\begin{quote}([^?!]*)\\end{quote}', test_string)
    for quote in quotes:
        new_quote = quote.replace('\n', '\n> ')
        test_string = test_string.replace(f'\\begin{{quote}}{quote}\\end{{quote}}', f'{new_quote}')

    return test_string


def remove_comments(test_string):

    return re.sub(r'^%.*\n?', '', test_string, flags=re.MULTILINE)