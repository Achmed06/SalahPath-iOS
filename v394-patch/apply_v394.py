"""Apply the phase-one regression fixes without changing the release version."""
from pathlib import Path
import subprocess
root = Path(__file__).resolve().parent.parent
patch = Path(__file__).with_name('phase1.patch')
subprocess.run(['git', 'apply', '--check', str(patch)], cwd=root, check=True)
subprocess.run(['git', 'apply', str(patch)], cwd=root, check=True)
