from cx_Freeze import setup, Executable
import sys,os
import matplotlib

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

packages = []

includes = ["os","sys","PyQt5","time","numpy.core._methods",'numpy','math']

include_files = [PYTHON_INSTALL_DIR+"\\DLLs\\tcl86t.dll",
                 PYTHON_INSTALL_DIR+"\\DLLs\\tk86t.dll",
                (matplotlib.get_data_path(), "mpl-data"),
                "D:\\RC\\doubly-reinforced-beamdesign\\RC_input.ui",
                "D:\\RC\\doubly-reinforced-beamdesign\\RC_output.ui",
                ]
options = {'build_exe': {'packages':packages,'includes':includes,"include_files":include_files}}


base = None

if sys.platform == "win32":
    base = "win32GUI"

setup(
    name="RC Calculate",
    options=options,
    version="1.0",
    description="RC Calculate",
    executables=[Executable("main.py",base = base,targetName ="main.exe")]
)