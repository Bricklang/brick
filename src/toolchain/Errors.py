from .Colors import *

class Err:
    def unknownchar(line, col, char, linesrc):
            underline=(" "*(col-1))+(Colors.RED+"^"+Colors.END)
            linesrc = linesrc[:(col-1)] + Colors.RED + linesrc[col-1] + Colors.END + linesrc[col:]
            errmsg=f"""
    {Colors.RED + Colors.BOLD}[ERR]{Colors.CYAN} Unexpected character {Colors.RED}{char}  {Colors.YELLOW}(line {line}, column {col}){Colors.END}
    {Colors.ITALIC}{linesrc}{Colors.END}
    {underline}
    """
            print(errmsg)