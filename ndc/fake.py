import argparse
import logging
import sys

from faker import Faker
import numpy as np
import pandas as pd
import user_agents

from ndc.utils import get_device_class, DEVICE_CLASS_NAMES

logger = logging.getLogger(__name__)


def fake_data(n=1000):
    fake = Faker()
    df = pd.DataFrame(
        columns=('device_class', 'oui', 'dhcp_options', 'dhcp_vendor'))

    random_state = np.random.RandomState()

    for i in range(n):
        ua_str = fake.user_agent()
        ua = user_agents.parse(ua_str)

        device_class = get_device_class(ua_str)

        try:
            brand = str(ua.device.brand).ljust(3)
        except Exception:
            brand = 'None'

        # Create a fake MAC address, using the first 3 characters from the
        # device brand to have a consistent OUI
        oui = ':'.join('%02x' % x for x in (
            ord(brand[0]),
            ord(brand[1]),
            ord(brand[2]),
        ))

        # Create a random comma-separated list of integers, seeded with the
        # length of the brand
        random_state.seed(len(brand))
        dhcp_options = ','.join('%s' % x for x in random_state.randint(
            1, 25, len(ua.os.family) + device_class, int))

        df = df.append({
            'device_class': DEVICE_CLASS_NAMES[device_class],
            'oui': oui,
            'dhcp_options': dhcp_options,
            'dhcp_vendor': brand.lower(),
        }, ignore_index=True)

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--samples', default='10', type=int)
    parser.add_argument('-o', '--output_file',
                        type=argparse.FileType('w+'), default=sys.stdout)
    args = parser.parse_args()

    df = fake_data(args.samples)
    df.to_csv(args.output_file, index=False)
