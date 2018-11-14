import numpy as np
import pickle
from imp import reload
from ipynb.fs.defs.SHW5 import read_index_file, read_data_file, get_hyponym_terms, create_clusters

def check_get_hyponym(examples, hyponyms, first_synset2word):
    try:
        results = [get_hyponym_terms(example["synset"], hyponyms, first_synset2word) == example["terms"]
                   for example in examples["get_hyponym_terms"]]
        if len(set(results)) == 1 and results[0]:
            print("Check for get_hyponym_terms successful")
        else:
            print("There are errors in get_hyponym_terms")
    except Exception as e:
        print("Error!")
        print(e.args)

    
def check_create_clusters(examples, first_synset2word, glove_dict):
    def cosine_sim(x, y):
        return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    try:
        error = 1e-12
        student_clusters = create_clusters(first_synset2word, glove_dict)
        results = [abs(cosine_sim(student_clusters[example["synset"]], example["cluster"]) - 1.0) < 1e-12
                   for example in examples["create_clusters"]]
        if len(set(results)) == 1 and results[0]:
            print("Check for create_clusters successful")
        else: print("There are errors in create_clusters")
    except Exception as e:
        print("Error!")
        print(e.args)
        

if __name__ == "__main__":
    with open('hw8_sanity_data.pkl', 'rb') as f:
        examples = pickle.load(f)
    word2first_synset, first_synset2word = read_index_file('index.noun')
    hyponyms = read_data_file('data.noun')
    glove_dict = {}
    with open('glove.twitter.27B.25d.txt', 'r') as f:
        for line in f.readlines():
                glove_dict[line.split()[0]] = np.array(line.split()[1:], dtype=np.float32)
    
    check_get_hyponym(examples, hyponyms, first_synset2word)
    check_create_clusters(examples, first_synset2word, glove_dict)
