#!/usr/bin/env python3

import os
from glob import glob
from distutils.core import setup
from distutils import dep_util

def get_mopath(pofile):
    # Function to determine right locale path for a .po file
    lang = os.path.basename(pofile)[:-3] # len('.po') == 3
    modir = os.path.join('locale', lang, 'LC_MESSAGES') # e.g. locale/fr/LC_MESSAGES/
    mofile = os.path.join(modir, 'devede_ng.mo') # e.g. locale/fr/LC_MESSAGES/devede_ng.mo
    return modir, mofile

def get_data_files():
    data_files = [
        (os.path.join('share', 'applications'), ['data/devede_ng.desktop']),
        (os.path.join('share', 'pixmaps'), ['data/devedeng.svg']),
        (os.path.join('share', 'devede_ng'), glob("data/interface/*")),
        (os.path.join('share', 'devede_ng'), glob('data/pixmaps/*g')),
        (os.path.join('share', 'devede_ng'), ['data/devedeng.svg']),
        (os.path.join('share', 'devede_ng'), ['data/codepages.lst']),
        (os.path.join('share', 'devede_ng'), ['data/languages.lst']),
        (os.path.join('share', 'devede_ng', 'backgrounds'), glob('data/pixmaps/backgrounds/*')),
        (os.path.join('share', 'doc', 'devede_ng', 'html'), glob('docs/html/*'))
    ]

    try:
        for pofile in [f for f in os.listdir('po') if f.endswith('.po')]:
            pofile = os.path.join('po', pofile) # po/fr.po
            modir, mofile = get_mopath(pofile)
            # translations must be always in /usr/share because Gtk.builder only search there. If someone knows how to fix this...
            target = os.path.join('/usr','share', modir) # share/locale/fr/LC_MESSAGES/
            data_files.append((target, [mofile]))
    except:
        pass

    return data_files


def compile_translations():
    
    try:
        for pofile in [f for f in os.listdir('po') if f.endswith('.po')]:
            pofile = os.path.join('po', pofile)
            modir, mofile = get_mopath(pofile)
    
            # create an architecture for these locales
            if not os.path.isdir(modir):
                os.makedirs(modir)
    
            if not os.path.isfile(mofile) or dep_util.newer(pofile, mofile):
                print('compiling %s' % mofile)
                # msgfmt.make(pofile, mofile)
                os.system("msgfmt \"" + pofile + "\" -o \"" + mofile + "\"")
            else:
                print('skipping %s - up to date' % mofile)
    except:
        pass

compile_translations()


#here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='devedeng',

    version='0.1.0.beta10',

    description='A video DVD creator',
    long_description = "A program that allows to create video DVDs",

    url='http://www.rastersoft.com',

    author='Raster Software Vigo (Sergio Costas)',
    author_email='raster@rastersoft.com',

    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        # 1 - Planning
        # 2 - Pre-Alpha
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video :: Conversion',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ],

    keywords='dvd video',

    packages=['devede'],

    package_dir={"devede" : "src/devede"},

    #package_data={'devede': ['data/*.ui']},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('share/devedeng/ui', ['ui/test.ui'])],
    data_files = get_data_files(),
    scripts=['src/devede_ng.py', 'src/copy_files_verbose.py'],
)
