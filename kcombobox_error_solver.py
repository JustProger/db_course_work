'''
    kcombobox_error_solve.py - программа, решающая ошибку kcombobox.
    Qt Designer неверно подключает QComboBox: использует несуществующие моудуль и класс kcombobox и KComboBox.
'''

import sys

if len(sys.argv) != 2:
    sys.exit('Error: only 1 argument needed.')
if (sys.argv[1].split('.')[-1] != 'py'):
    sys.exit('Error: argument must be a path to .py file.')

with open(sys.argv[1], 'r+') as f:
    f_inner = f.read()
    f_inner = f_inner.replace('from kcombobox import KComboBox', '')
    f_inner = f_inner.replace('KComboBox', 'QtWidgets.QComboBox')
    f.seek(0, 0)
    f.truncate(0)
    f.write(f_inner)
