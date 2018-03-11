import logging
import pickle

from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

_classes = [
    'mobile',
    'tablet',
    'pc',
    'other',
]

app = Flask(__name__)

with open('/srv/data/classifier.pkl', 'rb') as classifier_file:
    lr = pickle.load(classifier_file)

@app.route("/")
def predict():
    with open('/srv/data/format.pkl', 'rb') as format_file:
        x = pickle.load(format_file)

    for param in request.args:
        category = '%s:%s' % (param, request.args.get(param))
        try:
            x.loc[0,[category]] = 1
        except KeyError:
            logger.warn('Unknown category "%s"' % category)

    a = lr.predict_proba(x)[0]
    probability = list(map(lambda x: float(x), a))
    return jsonify({
            'predicted_class': _classes[lr.predict(x)[0]],
            'probabilities': dict(zip(_classes, probability)),
        })


