import sys
from pathlib import Path

# This compatibility filename must not shadow the installed mathforge package.
script_dir = Path(__file__).resolve().parent
sys.path[:] = [p for p in sys.path if Path(p).resolve() != script_dir]
from mathforge.cli import main
raise SystemExit(main())
