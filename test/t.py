import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from inter import Interprinter
pna = Interprinter()
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "x.pna")
pna.read(file_path)
