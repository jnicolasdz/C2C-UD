import sys
from pathlib import Path

# Agrega la raíz del proyecto al path para que 'app' sea importable
sys.path.insert(0, str(Path(__file__).resolve().parent))