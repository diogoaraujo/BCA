# BCA

Destacar ou anotar um texto em um arquivo PDF é uma ótima estratégia para ler e reter informações importantes. Esta técnica pode ajudar a trazer informações importantes imediatamente à atenção do leitor. Não há dúvida de que um texto destacado em amarelo provavelmente chamaria sua atenção primeiro.

A redação de um arquivo PDF permite ocultar informações confidenciais, mantendo a formatação do documento. Isso preserva informações privadas e confidenciais antes de compartilhá-las. Além disso, aumenta ainda mais a integridade e a credibilidade da organização no manuseio de informações confidenciais.

Neste tutorial, você aprenderá como redigir, enquadrar ou destacar um texto em arquivos PDF usando Python.

Fluxograma de processo para o tutorial

Neste guia, usaremos a biblioteca PyMuPDF , que é uma solução de intérprete de PDF, XPS e EBook altamente versátil e personalizável que pode ser usada em uma ampla variedade de aplicativos como renderizador, visualizador ou kit de ferramentas de PDF.

O objetivo deste tutorial é desenvolver um utilitário leve baseado em linha de comando para redigir, enquadrar ou realçar um texto incluído em um arquivo PDF ou em uma pasta contendo uma coleção de arquivos PDF. Além disso, ele permitirá que você remova os destaques de um arquivo PDF ou de uma coleção de arquivos PDF.

Vamos instalar os requisitos:

$ pip install PyMuPDF==1.18.9

Abra um novo arquivo Python e vamos começar:

# Import Libraries
from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import fitz


def extract_info(input_file: str):
    """
    Extracts file info
    """
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    output = {
        "File": input_file, "Encrypted": ("True" if pdfDoc.isEncrypted else "False")
    }
    # If PDF is encrypted the file metadata cannot be extracted
    if not pdfDoc.isEncrypted:
        for key, value in pdfDoc.metadata.items():
            output[key] = value
    # To Display File Info
    print("## File Information ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in output.items()))
    print("######################################################################")
    return True, output

extract_info()função coleta os metadados de um arquivo PDF , os atributos que podem ser extraídos são format, title, author, subject, keywords, creator, producer, creation date, modification date, trapped, encryption, e o número de páginas. Vale a pena notar que esses atributos não podem ser extraídos quando você direciona um arquivo PDF criptografado.

def search_for_text(lines, search_str):
    """
    Search for the search string within the document lines
    """
    for line in lines:
        # Find all matches within one line
        results = re.findall(search_str, line, re.IGNORECASE)
        # In case multiple matches within one line
        for result in results:
            yield result

Esta função procura uma string dentro das linhas do documento usando o re.findall()função, re.IGNORECASEé ignorar o caso durante a pesquisa.

def redact_matching_data(page, matched_values):
    """
    Redacts matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        # Redact matching values
        [page.addRedactAnnot(area, text=" ", fill=(0, 0, 0))
         for area in matching_val_area]
    # Apply the redaction
    page.apply_redactions()
    return matches_found

Esta função executa o seguinte:

    Faça um loop pelos valores correspondentes da string de pesquisa que estamos procurando.
    Edite os valores correspondentes.
    Aplique a redação na página selecionada.

Você pode alterar a cor da redação usando o fillargumento sobre o page.addRedactAnnot()método, configurando-o para (0, 0, 0)resultará em uma redação preta. Estes são valores RGB que variam de 0 a 1. Por exemplo, (1, 0, 0)resultará em uma redação vermelha e assim por diante.

def frame_matching_data(page, matched_values):
    """
    frames matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        for area in matching_val_area:
            if isinstance(area, fitz.fitz.Rect):
                # Draw a rectangle around matched values
                annot = page.addRectAnnot(area)
                # , fill = fitz.utils.getColor('black')
                annot.setColors(stroke=fitz.utils.getColor('red'))
                # If you want to remove matched data
                #page.addFreetextAnnot(area, ' ')
                annot.update()
    return matches_found

o frame_matching_data()A função desenha um retângulo vermelho (quadro) ao redor dos valores correspondentes.

Em seguida, vamos definir uma função para destacar o texto:

def highlight_matching_data(page, matched_values, type):
    """
    Highlight matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        # print("matching_val_area",matching_val_area)
        highlight = None
        if type == 'Highlight':
            highlight = page.addHighlightAnnot(matching_val_area)
        elif type == 'Squiggly':
            highlight = page.addSquigglyAnnot(matching_val_area)
        elif type == 'Underline':
            highlight = page.addUnderlineAnnot(matching_val_area)
        elif type == 'Strikeout':
            highlight = page.addStrikeoutAnnot(matching_val_area)
        else:
            highlight = page.addHighlightAnnot(matching_val_area)
        # To change the highlight colar
        # highlight.setColors({"stroke":(0,0,1),"fill":(0.75,0.8,0.95) })
        # highlight.setColors(stroke = fitz.utils.getColor('white'), fill = fitz.utils.getColor('red'))
        # highlight.setColors(colors= fitz.utils.getColor('red'))
        highlight.update()
    return matches_found

A função acima aplica o modo de realce adequado nos valores correspondentes, dependendo do tipo de realce inserido como parâmetro.

Você sempre pode alterar a cor do destaque usando o highlight.setColors()método como mostrado nos comentários.

def process_data(input_file: str, output_file: str, search_str: str, pages: Tuple = None, action: str = 'Highlight'):
    """
    Process the pages of the PDF File
    """
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    total_matches = 0
    # Iterate through pages
    for pg in range(pdfDoc.pageCount):
        # If required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        # Select the page
        page = pdfDoc[pg]
        # Get Matching Data
        # Split page by lines
        page_lines = page.getText("text").split('\n')
        matched_values = search_for_text(page_lines, search_str)
        if matched_values:
            if action == 'Redact':
                matches_found = redact_matching_data(page, matched_values)
            elif action == 'Frame':
                matches_found = frame_matching_data(page, matched_values)
            elif action in ('Highlight', 'Squiggly', 'Underline', 'Strikeout'):
                matches_found = highlight_matching_data(
                    page, matched_values, action)
            else:
                matches_found = highlight_matching_data(
                    page, matched_values, 'Highlight')
            total_matches += matches_found
    print(f"{total_matches} Match(es) Found of Search String {search_str} In Input File: {input_file}")
    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())

Relacionado: Como extrair texto de PDF em Python

O principal objetivo do process_data()função é a seguinte:

    Abra o arquivo de entrada.
    Crie um buffer de memória para armazenar temporariamente o arquivo de saída.
    Inicialize uma variável para armazenar o número total de correspondências da string que estávamos procurando.
    Itere ao longo das páginas selecionadas do arquivo de entrada e divida a página atual em linhas.
    Procure a string dentro da página.
    Aplique a ação correspondente (ou seja, "Redact", "Frame", "Highlight", etc)
    Exiba uma mensagem sinalizando o status do processo de pesquisa.
    Salve e feche o arquivo de entrada.
    Salve o buffer de memória no arquivo de saída.

Aceita vários parâmetros:

    input_file: o caminho do arquivo PDF a ser processado.
    output_file: o caminho do arquivo PDF a ser gerado após o processamento.
    search_str: A string a ser pesquisada.
    pages: As páginas a serem consideradas durante o processamento do arquivo PDF.
    action: A ação a ser executada no arquivo PDF.

Em seguida, vamos escrever uma função para remover o destaque caso queiramos:

def remove_highlght(input_file: str, output_file: str, pages: Tuple = None):
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    # Initialize a counter for annotations
    annot_found = 0
    # Iterate through pages
    for pg in range(pdfDoc.pageCount):
        # If required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        # Select the page
        page = pdfDoc[pg]
        annot = page.firstAnnot
        while annot:
            annot_found += 1
            page.deleteAnnot(annot)
            annot = annot.next
    if annot_found >= 0:
        print(f"Annotation(s) Found In The Input File: {input_file}")
    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())

O propósito do remove_highlight()função é remover os destaques (não as redações) de um arquivo PDF. Ele executa o seguinte:

    Abra o arquivo de entrada.
    Crie um buffer de memória para armazenar temporariamente o arquivo de saída.
    Itere ao longo das páginas do arquivo de entrada e verifique se as anotações são encontradas.
    Exclua essas anotações.
    Exiba uma mensagem sinalizando o status deste processo.
    Feche o arquivo de entrada.
    Salve o buffer de memória no arquivo de saída.

Agora vamos fazer uma função wrapper que usa funções anteriores para chamar a função apropriada dependendo da ação:

def process_file(**kwargs):
    """
    To process one single file
    Redact, Frame, Highlight... one PDF File
    Remove Highlights from a single PDF File
    """
    input_file = kwargs.get('input_file')
    output_file = kwargs.get('output_file')
    if output_file is None:
        output_file = input_file
    search_str = kwargs.get('search_str')
    pages = kwargs.get('pages')
    # Redact, Frame, Highlight, Squiggly, Underline, Strikeout, Remove
    action = kwargs.get('action')
    if action == "Remove":
        # Remove the Highlights except Redactions
        remove_highlght(input_file=input_file,
                        output_file=output_file, pages=pages)
    else:
        process_data(input_file=input_file, output_file=output_file,
                     search_str=search_str, pages=pages, action=action)

A ação pode ser "Redact", "Frame", "Highlight", "Squiggly", "Underline", "Strikeout", e "Remove".

Vamos definir a mesma função, mas com pastas que contêm vários arquivos PDF:

def process_folder(**kwargs):
    """
    Redact, Frame, Highlight... all PDF Files within a specified path
    Remove Highlights from all PDF Files within a specified path
    """
    input_folder = kwargs.get('input_folder')
    search_str = kwargs.get('search_str')
    # Run in recursive mode
    recursive = kwargs.get('recursive')
    #Redact, Frame, Highlight, Squiggly, Underline, Strikeout, Remove
    action = kwargs.get('action')
    pages = kwargs.get('pages')
    # Loop though the files within the input folder.
    for foldername, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            # Check if pdf file
            if not filename.endswith('.pdf'):
                continue
             # PDF File found
            inp_pdf_file = os.path.join(foldername, filename)
            print("Processing file =", inp_pdf_file)
            process_file(input_file=inp_pdf_file, output_file=None,
                         search_str=search_str, action=action, pages=pages)
        if not recursive:
            break

Esta função destina-se a processar os arquivos PDF incluídos em uma pasta específica.

Ele percorre os arquivos da pasta especificada recursivamente ou não, dependendo do valor do parâmetro recursivo e processa esses arquivos um por um.

Ele aceita os seguintes parâmetros:

    input_folder: O caminho da pasta que contém os arquivos PDF a serem processados.
    search_str: O texto a ser pesquisado para manipular.
    recursive: se esse processo deve ser executado recursivamente, fazendo um loop pelas subpastas ou não.
    action: a ação a ser executada entre a lista mencionada anteriormente.
    pages: as páginas a serem consideradas.

Antes de fazermos nosso código principal, vamos criar uma função para analisar argumentos de linha de comando:

def is_valid_path(path):
    """
    Validates the path inputted and checks whether it is a file path or a folder path
    """
    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid Path {path}")


def parse_args():
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path,
                        required=True, help="Enter the path of the file or the folder to process")
    parser.add_argument('-a', '--action', dest='action', choices=['Redact', 'Frame', 'Highlight', 'Squiggly', 'Underline', 'Strikeout', 'Remove'], type=str,
                        default='Highlight', help="Choose whether to Redact or to Frame or to Highlight or to Squiggly or to Underline or to Strikeout or to Remove")
    parser.add_argument('-p', '--pages', dest='pages', type=tuple,
                        help="Enter the pages to consider e.g.: [2,4]")
    action = parser.parse_known_args()[0].action
    if action != 'Remove':
        parser.add_argument('-s', '--search_str', dest='search_str'                            # lambda x: os.path.has_valid_dir_syntax(x)
                            , type=str, required=True, help="Enter a valid search string")
    path = parser.parse_known_args()[0].input_path
    if os.path.isfile(path):
        parser.add_argument('-o', '--output_file', dest='output_file', type=str  # lambda x: os.path.has_valid_dir_syntax(x)
                            , help="Enter a valid output file")
    if os.path.isdir(path):
        parser.add_argument('-r', '--recursive', dest='recursive', default=False, type=lambda x: (
            str(x).lower() in ['true', '1', 'yes']), help="Process Recursively or Non-Recursively")
    args = vars(parser.parse_args())
    # To Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")
    return args

Por fim, vamos escrever o código principal:

if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args = parse_args()
    # If File Path
    if os.path.isfile(args['input_path']):
        # Extracting File Info
        extract_info(input_file=args['input_path'])
        # Process a file
        process_file(
            input_file=args['input_path'], output_file=args['output_file'], 
            search_str=args['search_str'] if 'search_str' in (args.keys()) else None, 
            pages=args['pages'], action=args['action']
        )
    # If Folder Path
    elif os.path.isdir(args['input_path']):
        # Process a folder
        process_folder(
            input_folder=args['input_path'], 
            search_str=args['search_str'] if 'search_str' in (args.keys()) else None, 
            action=args['action'], pages=args['pages'], recursive=args['recursive']
        )

Agora vamos testar nosso programa:

$ python pdf_highlighter.py --help

Saída:

usage: pdf_highlighter.py [-h] -i INPUT_PATH [-a {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}] [-p PAGES]

Available Options

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input_path INPUT_PATH
                        Enter the path of the file or the folder to process
  -a {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}, --action {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}
                        Choose whether to Redact or to Frame or to Highlight or to Squiggly or to Underline or to Strikeout or to Remove
  -p PAGES, --pages PAGES
                        Enter the pages to consider e.g.: [2,4]

Antes de explorar nossos cenários de teste, deixe-me esclarecer alguns pontos:

    Para evitar encontrar o PermissionError, feche o arquivo PDF de entrada antes de executar este utilitário.
    O arquivo PDF de entrada a ser processado não deve ser um arquivo PDF digitalizado.
    A string de pesquisa está em conformidade com as regras de expressões regulares usando o re módulo . Por exemplo, definir a string de pesquisa para "organi[sz]e"correspondem a "organizar" e "organizar".

Como exemplo de demonstração, vamos destacar a palavra "BERT" no artigo BERT :

$ python Highlight-Redact-Text-PDF.py -i bca_198_28-10-20212.pdf -a Highlight -s "ALA 11"

Saída:

## Command Arguments #################################################
input_path:.\bca_198_28-10-20212.pdf
action:Highlight
pages:None
search_str:ALA 11
output_file:None
######################################################################
## File Information ##################################################
File:.\bca_198_28-10-20212.pdf
Encrypted:False
format:PDF 1.6
title:198-BCA-28102021
author:flavialemosfrles
subject:
keywords:
creator:PDFCreator Version 1.7.1
modDate:D:20211027161237-03'00'
trapped:
encryption:None
######################################################################
Deprecation: 'getText' removed from class 'Page' after v1.19 - use 'get_text'.
Deprecation: 'searchFor' removed from class 'Page' after v1.19 - use 'search_for'.
Deprecation: 'addHighlightAnnot' removed from class 'Page' after v1.19 - use 'add_highlight_annot'.
11 Match(es) Found of Search String ALA 11 In Input File: .\bca_198_28-10-20212.pdf
