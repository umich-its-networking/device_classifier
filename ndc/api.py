import copy
import os

from flask import Flask, request, jsonify

from ndc.train import train


app = Flask(__name__)

app.logger.info('Parsing raw data file "%s"' % os.getenv('RAW_DATA'))

classifier, meta = train(os.getenv('RAW_DATA'))

app.logger.info('Training sample size: %d' % meta.sample_size)
app.logger.info('Classifier accuracy: %.1f%%' % (meta.accuracy * 100))


@app.route("/")
def predict():
    x = copy.deepcopy(meta.format)

    for param in request.args:
        category = '%s:%s' % (param, request.args.get(param))
        try:
            x.loc[0, [category]] = 1
        except KeyError:
            app.logger.warn('Unknown category "%s"' % category)

    a = classifier.predict_proba(x)[0]
    probability = list(map(lambda x: round(float(x), 5), a))
    return jsonify({
            'predicted_class': meta.classes[classifier.predict(x)[0]],
            'probabilities': dict(zip(meta.classes, probability)),
        })


@app.route("/info/")
def info():
    return jsonify({
            'sample_size': meta.sample_size,
            'accuracy': meta.accuracy,
        })
