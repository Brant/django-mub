from setuptools import setup, find_packages

setup(
    name = "django-mub",
    version = "0.3.0",
    url = 'http://github.com/Brant/django-mub',
    license = 'GPL',
    description = "Monster Under the Bed - Compresses and Consolidates CSS and JS Files for Django Applications",
    long_description = open('README.md').read(),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',

    packages = find_packages(exclude=('mub_tests', )),
    include_package_data = True,
    zip_safe = False,

    install_requires = ['setuptools', 'django', 'jsmin<2.3', 'cssmin<0.3'],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
