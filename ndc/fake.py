import argparse
import logging
import sys

from faker import Faker
import numpy as np
import pandas as pd
import user_agents

from ndc.train import get_device_class

logger = logging.getLogger(__name__)


def fake_data(n=1000):
    fake = Faker()
    df = pd.DataFrame(
        columns=('mac_int', 'mac_str', 'user_agent', 'req_list', 'vendor'))

    random_state = np.random.RandomState()

    for i in range(n):
        ua_str = fake.user_agent()
        # ua_strs[np.random.randint(0, NUM_UA_STRS - 1)]
        ua = user_agents.parse(ua_str)

        device_class = get_device_class(ua_str)

        # if device_class == 2 and np.random.randint(0, 10) != 0:
        #     continue

        try:
            brand = str(ua.device.brand).ljust(3)
        except Exception:
            brand = 'None'

        # Create a fake MAC address, using the first 2 characters from the
        # device brand to have a consistent OUI
        mac_str = ':'.join('%02x' % x for x in (
            ord(brand[0]),
            ord(brand[1]),
            int(device_class),
            np.random.randint(0, 256),
            np.random.randint(0, 256),
            np.random.randint(0, 256),
        ))

        # Create a random comma-separated list of integers, seeded with the
        # length of the brand
        random_state.seed(len(brand))
        dhcp_opts = ','.join('%s' % x for x in random_state.randint(
            1, 25, len(ua.os.family) + device_class, int))

        df = df.append({
            'mac_int': i,
            'mac_str': mac_str,
            'user_agent': ua_str,
            'req_list': dhcp_opts,
            'vendor': brand.lower(),
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
