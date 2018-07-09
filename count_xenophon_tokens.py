from extract_features import parse_tess
from cltk.utils.file_operations import open_pickle
text = parse_tess('tesserae/texts/grc/xenophon.anabasis.tess')
tokenizer = open_pickle('tokenizers/ancient_greek.pickle')
print(len(tokenizer.tokenize(text)))
