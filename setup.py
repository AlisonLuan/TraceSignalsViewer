from cx_Freeze import setup, Executable

setup(
    name="PlotterApp",
    version="1.0",
    description="Plot Signals App",
    executables=[Executable("main.py", base="Win32GUI")],
)
