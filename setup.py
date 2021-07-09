from setuptools import setup

setup(
    name='fund',
    version='0.1',
    py_modules=['fund'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        savefund=fund:save
        showfund=fund:show
    ''',
)
