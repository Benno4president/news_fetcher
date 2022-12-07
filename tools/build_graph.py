import networkx as nx
import csv
import pandas as pd
from spacy.lang.en import English


"""
https://github.com/jacomyma/mapping-controversies/blob/main/notebooks/Documents_with_text_to_word_list.ipynb

https://github.com/jacomyma/mapping-controversies/blob/main/notebooks/Words_and_documents_with_text_to_network.ipynb
"""

def doc_2_wordlist(df: pd.DataFrame, text_key: str):
    doc_df = df.copy()
    doc_index = {}
    # Tokenizer (extract words)
    NLP = English()
    count=1
    print("Extracting words from "+str(len(doc_df.index))+" documents. This might take a while...")
    for index, row in doc_df.iterrows():
        text = row[text_key]
        if count % 10 == 0:
            print("Text extracted from "+str(count)+" documents out of "+str(len(doc_df.index))+". Continuing...")
        count += 1

        tokens = NLP(text)
        words = {}
        for token in tokens:
            if not token.is_stop and token.is_alpha:
                t = token.text
                if t not in words:
                    words[t] = {'W-text': t, 'W-count':0}
                words[t]['W-count'] += 1
        doc_index[index] = words


    doc_notxt_df = doc_df.drop(columns=[text_key])
    word_index = {}
    for index, row in doc_notxt_df.iterrows():
        for wsign in doc_index[index]:
            w = doc_index[index][wsign]
            if wsign not in word_index:
              word_index[wsign] = {'text': w['W-text'], 'count-occurences-total':0, 'count-documents':0}
            word_index[wsign]['count-occurences-total'] += w['W-count']
            word_index[wsign]['count-documents'] += 1

    word_df = pd.DataFrame(word_index.values())
    return word_df


def text_2_network_graph(text_df:pd.DataFrame, id_key:str, text_key:str, word_df:pd.DataFrame, word_key:str):
    # Delete documents that contain none of the words?
    discard_unrelated_documents = True

    # Get a set of the words
    words = set()
    for index, row in word_df.iterrows():
      words.add(row[word_key])

    # Init data for output
    network_doc_set = set()
    network_word_set = set()
    network_edge_list = []

    # Search words in documents
    for index, row in text_df.iterrows():
        print(index, end='\r')
        if type(row[text_key]) == str:
            text = row[text_key].lower()
            count_per_word = {}
            flag = False
            for word in words:
                count = text.count(word.lower())
                count_per_word[word] = count
                if count > 0:
                    flag = True

            if flag or not discard_unrelated_documents:
                doc_id = row[id_key]
                network_doc_set.add(doc_id)
                for word in words:
                    count = count_per_word[word]
                    if count > 0:
                        network_word_set.add(word)
                        network_edge_list.append((doc_id,word,{"count":count}))

    # Build the nodes
    nodes = []
    text_df_no_text = text_df.drop(columns=[text_key]) 
    for index, row in text_df_no_text.iterrows():
      if row[id_key] in network_doc_set:
        nodes.append((row[id_key], {**row, 'label':row[id_key], 'type':'document'}))

    for index, row in word_df.iterrows():
      if row[word_key] in network_word_set:
        nodes.append((row[word_key], {**row, 'label':row[word_key], 'type':'term'}))

    # Build edges
    edges = network_edge_list

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print("Done building network graph")
    return G


if __name__ == '__main__':
    # Input file
    input_file = "tools/db2coin_out.csv"

    # Output files
    #output_file_words = "tools/words.csv"

    doc_df = pd.read_csv(input_file, quotechar='"', encoding='utf8', doublequote=True, quoting=csv.QUOTE_NONNUMERIC, dtype=object, on_bad_lines='skip')
    doc_df['temp_index'] = range(0,len(doc_df))
    
    print("Preview of the document list:")
    print(doc_df)

    words = doc_2_wordlist(doc_df, 'preprocess_txt')
    print(words)

    graph = text_2_network_graph(text_df=doc_df, id_key='temp_index', text_key='preprocess_txt', word_df=words, word_key='text')

    output_file_network = "tools/terms-document-network.gexf"
    nx.write_gexf(graph, output_file_network)


