from setuptools import find_packages, setup

setup(
    name='ndc',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Faker==0.9.1',
        'Flask==1.0.2',
        'netaddr==0.7.19',
        'pandas==0.23.4',
        'scikit-learn==0.20.0',
        'user-agents==1.1.0',
    ],
)
