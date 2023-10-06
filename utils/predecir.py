import nltk
import re
import string
import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

from config import get_model, get_vector_model
from metadata.categorias import Categorias


def predir_categoria(data):

    data = data.lower()
    nltk.download('punkt')
    data = word_tokenize(data)

    data = [re.sub(f'[{string.punctuation}]+', '', i) for i in data if i not in list(string.punctuation)]
    nltk.download('stopwords')
    data = [i for i in data if i not in stopwords.words('english')]
    nltk.download('wordnet')
    wordnetlemmatizer = WordNetLemmatizer()
    data = [wordnetlemmatizer.lemmatize(i) for i in data]
    data = ' '.join(data)

    tf_idf_vectorizer = get_vector_model()
    data = [data]
    data = tf_idf_vectorizer.transform(data)
    data = pd.DataFrame(data.toarray(),
                          columns=tf_idf_vectorizer.get_feature_names_out())

    model = get_model()
    y = model.predict(data)
    categoria = Categorias.categorias.get(y[0])

    return categoria
