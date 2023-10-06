import os


class Path:

    path_folder = os.path.dirname(__file__)

    input_ = os.path.join(path_folder, '..', 'input')
    modelo = os.path.join(input_, 'clasificor_web.pkl')
    vector = os.path.join(input_, 'tfidf_vectorizer_model.pkl')
    out_ = os.path.join(path_folder, '..', 'public', 'static', 'img')
    public = os.path.join(path_folder, '..', 'public')

    public_key_jwt = os.path.join(input_, 'credenciales', 'public_jwt.pem')
    private_key_jwt = os.path.join(input_, 'credenciales', 'private_jwt.pem')
