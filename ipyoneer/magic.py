import ast
import typing

from IPython import InteractiveShell
from IPython.core.magic import Magics, cell_magic, magics_class, needs_local_scope


@magics_class
class PyoneerMagics(Magics):
    if typing.TYPE_CHECKING:
        shell: InteractiveShell

    @cell_magic
    @needs_local_scope
    def ipyoneer(self, line, cell, local_ns):
        """Magic to run ipyoneer on a cell"""
        source = ast.parse(cell, mode="exec")
        # source.body
        self.shell.run_cell(cell)
