# -*- coding: utf-8 -*-
"""
Text preprocessing module.


"""

import docx2txt
import re
import networkx as nx
import matplotlib
from nltk.corpus import wordnet as wn

def extract_exercices(from_file=None):
    """
    This function take a word docx file, extract all the content of the exercices
    and return the list of the exercices
    - from_file is a string which represents the relative path of the docx file.
    """
    #Get the content of the file in String format
    file_text = docx2txt.process(from_file)
    #Create the pattern which we use to extract the exercices
    pattern = re.compile(r'Exercice \d')
    #Split the content and return a list
    exercices_raw = re.split(pattern, file_text)
    #Use list comprehension to throw away indesirable sentences.
    exo_list = [sent for sent in exercices_raw if sent != '']
    return exo_list


def get_text(file):
    """Read text from a file, normalizing whitespace and stripping HTML markup."""
    text = open(file).read()
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub('\s+', ' ', text)
    return text

def lexical_diversity(text):
    """
    Calculate the lexical diversity of the text or corpus. It consists of divided the
    length of the set of the corpus over the real lenght of the corpus. 
    """
    return len(set(text)) / len(text)

def percentage(count, total):
    """
    Compute the percentage of the use of a specific word in the corpus
    """
    return 100 * count / total

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def accuracy(reference, test):
    """
    Calculate the fraction of test items that equal the corresponding reference items.

    Given a list of reference values and a corresponding list of test values,
    return the fraction of corresponding values that are equal.
    In particular, return the fraction of indexes
    {0<i<=len(test)} such that C{test[i] == reference[i]}.

        >>> accuracy(['ADJ', 'N', 'V', 'N'], ['N', 'N', 'V', 'ADJ'])
        0.5

    :param reference: An ordered list of reference values
    :type reference: list
    :param test: A list of values to compare against the corresponding
        reference values
    :type test: list
    :return: the accuracy score
    :rtype: float
    :raises ValueError: If reference and length do not have the same length
    """

    if len(reference) != len(test):
        raise ValueError("Lists must have the same length.")
    num_correct = 0
    for x, y in zip(reference, test):
        if x == y:
            num_correct += 1
    return float(num_correct) / len(reference)


def traverse(graph, start, node):
    graph.depth[node.name] = node.shortest_path_distance(start)
    for child in node.hyponyms():
        graph.add_edge(node.name, child.name) [1]
        traverse(graph, start, child) [2]

def hyponym_graph(start):
    G = nx.Graph() [3]
    G.depth = {}
    traverse(G, start, start)
    return G

def graph_draw(graph):
    nx.draw_graphviz(graph,
         node_size = [16 * graph.degree(n) for n in graph],
         node_color = [graph.depth[n] for n in graph],
         with_labels = False)
    matplotlib.pyplot.show()