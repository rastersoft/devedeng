#!/usr/bin/env python3

import os
import sys
from glob import glob
from distutils.core import setup

try:
    from distutils import dep_util
except:
    pass


def get_data_files():
    data_files = [
        (os.path.join('share', 'applications'), ['data/devede_ng.py.desktop']),
        (os.path.join('share', 'pixmaps'), ['data/devedeng.svg']),
        (os.path.join('share', 'icons', 'hicolor',
                      'scalable', 'apps'), ['data/devedeng_icon.svg']),
        (os.path.join('share', 'devedeng'), glob("data/interface/*")),
        (os.path.join('share', 'devedeng'), glob('data/pixmaps/*g')),
        (os.path.join('share', 'devedeng'), ['data/devedeng.svg']),
        (os.path.join('share', 'devedeng'), ['data/devedeng_icon.svg']),
        (os.path.join('share', 'devedeng'), ['data/codepages.lst']),
        (os.path.join('share', 'devedeng'), ['data/languages.lst']),
        (os.path.join('share', 'devedeng', 'backgrounds'),
         glob('data/pixmaps/backgrounds/*')),
        (os.path.join('share', 'doc', 'devedeng', 'html'), glob('doc/*')),
        (os.path.join('share', 'man', 'man1'), ['data/devede.1.gz'])
    ]

    for lang_name in [f for f in os.listdir('locale')]:
        mofile = os.path.join('locale', lang_name,
                              'LC_MESSAGES', 'devedeng.mo')
        # translations must be always in /usr/share because Gtk.builder only
        # search there. If someone knows how to fix this...
        # share/locale/fr/LC_MESSAGES/
        target = os.path.join('/usr', 'share', 'locale',
                              lang_name, 'LC_MESSAGES')
        data_files.append((target, [mofile]))

    return data_files


def compile_translations():

    if (os.system("msgfmt -V") != 0):
        print('You need the binary "msgfmt" (from "gettext") to compile the translations. Aborting')
        sys.exit(-1)

    try:
        for pofile in [f for f in os.listdir('po') if f.endswith('.po')]:
            pofile = os.path.join('po', pofile)

            lang = os.path.basename(pofile)[:-3]  # len('.po') == 3
            # e.g. locale/fr/LC_MESSAGES/
            modir = os.path.join('locale', lang, 'LC_MESSAGES')
            # e.g. locale/fr/LC_MESSAGES/devedeng.mo
            mofile = os.path.join(modir, 'devedeng.mo')

            # create an architecture for these locales
            if not os.path.isdir(modir):
                os.makedirs(modir)

            if not os.path.isfile(mofile) or dep_util.newer(pofile, mofile):
                # msgfmt.make(pofile, mofile)
                os.system("msgfmt \"" + pofile + "\" -o \"" + mofile + "\"")
    except:
        pass


compile_translations()
try:
    if os.path.isfile('data/devede.1'):
        os.system("gzip -c data/devede.1 > data/devede.1.gz")
except:
    pass

#here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='devedeng',

    version='4.8.12',

    description='A video DVD creator',
    long_description="A program that allows to create video DVDs",

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
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video :: Conversion',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Video :: Conversion'
    ],

    keywords='dvd video',

    packages=['devedeng'],

    package_dir={"devedeng": "src/devedeng"},

    #package_data={'devede': ['data/*.ui']},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('share/devedeng/ui', ['ui/test.ui'])],
    data_files=get_data_files(),
    scripts=['src/devede_ng.py', 'src/copy_files_verbose.py'],
)

if (len(sys.argv) == 2) and (sys.argv[1] == "install"):
    os.system("gtk-update-icon-cache")
