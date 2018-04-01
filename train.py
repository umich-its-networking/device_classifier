import argparse
import logging
import pickle

import pandas as pd
import user_agents
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


_device_classes = {
    (1, 0, 0): 0,
    (0, 1, 0): 1,
    (0, 0, 1): 2,
}

_device_class_names = [
    'mobile',
    'tablet',
    'pc',
    'other',
]

def _get_device_class(ua_string):
    ua = user_agents.parse(ua_string)
    return _device_classes.get(
         (int(ua.is_mobile), int(ua.is_tablet), int(ua.is_pc)),
         3
    )


def get_data_and_target(orig):
    # pull OUI from MAC address
    orig['oui'] = orig.mac_str.apply(lambda x: x[:8])

    cols = ['req_list', 'vendor', 'oui']

    return (
        pd.get_dummies(orig.loc[:, cols], prefix_sep=':'),
        orig.user_agent.map(_get_device_class).values,
    )


def get_fitted_classifier(X, y):
    lr = LogisticRegression(C=100.0, random_state=1)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1, stratify=y)
    lr.fit(X_train, y_train)

    return lr


def train(raw_file):
    X, y = get_data_and_target(
        pd.read_csv(raw_file).drop_duplicates()
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=1, stratify=y)

    lr = get_fitted_classifier(X_train, y_train)

    class Meta(object):
        def __init__(self):
            self.format = X.head(1).copy()
            self.format[:] = 0

            self.sample_size = len(X_train)
            self.accuracy = lr.score(X_test, y_test)
            self.classes = _device_class_names

    return (lr, Meta())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--classifier_file',
                        type=argparse.FileType('wb+'), required=True)
    parser.add_argument('-f', '--format_file',
                        type=argparse.FileType('wb+'), required=True)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('data_file')
    args = parser.parse_args()

    if args.verbose >= 2:
        log_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
        log_level = logging.DEBUG
    elif args.verbose == 1:
        log_format = '%(asctime)s %(levelname)s %(message)s'
        log_level = logging.INFO
    else:
        log_format = '%(asctime)s %(levelname)s %(message)s'
        log_level = logging.WARN

    logging.basicConfig(
        format=log_format,
        datefmt='%Y-%m-%dT%H:%M:%S%z',
        level=log_level,
    )

    logger.info('Parsing raw data file "%s"' % args.data_file)

    classifier, meta = train(args.data_file)

    logger.info('Training sample size: %d' % meta.sample_size)
    logger.info('Classifier accuracy: %.1f%%' % (meta.accuracy * 100))

    logger.info('Saving classifer to "%s"' % args.classifier_file.name)
    pickle.dump(classifier, args.classifier_file)

    logger.info('Saving format to "%s"' % args.format_file.name)
    pickle.dump(meta.format, args.format_file)
