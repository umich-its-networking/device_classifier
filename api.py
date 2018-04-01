import copy
import logging
import os

from flask import Flask, request, jsonify

from train import train


logger = logging.getLogger(__name__)

_classes = [
    'mobile',
    'tablet',
    'pc',
    'other',
]

app = Flask(__name__)

classifier, meta = train(os.getenv('RAW_DATA'))


@app.route("/")
def predict():
    x = copy.deepcopy(meta.format)

    for param in request.args:
        category = '%s:%s' % (param, request.args.get(param))
        try:
            x.loc[0, [category]] = 1
        except KeyError:
            logger.warn('Unknown category "%s"' % category)

    a = classifier.predict_proba(x)[0]
    probability = list(map(lambda x: round(float(x), 5), a))
    return jsonify({
            'predicted_class': _classes[classifier.predict(x)[0]],
            'probabilities': dict(zip(_classes, probability)),
        })


@app.route("/info")
def info():
    return jsonify({
            'sample_size': meta.sample_size,
            'accuracy': meta.accuracy,
        })
