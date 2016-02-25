from os.path import dirname,join,abspath
lib = join(dirname(__file__),'EasyGame.lib')
from sys import path
path.append(join(dirname(abspath(__file__)),'EasyGame.lib'))
path.append(join(dirname(abspath(__file__)),'EasyGame.lib/PygameReadWrite'))

from form import MenuForm
from slidemenu import menu as slidemenu
from MenuSystem import Menu as MSmenu
from MenuSystem import MenuSystem
