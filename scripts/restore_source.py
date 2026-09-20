"""Restore the verified base and the ordered patch chain on Linux or macOS.

The archived workflow/README are intentionally excluded: an old archive must
never overwrite the checked-out CI definitions or current documentation.
"""
from pathlib import Path
import base64
import hashlib
import io
import json
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parent.parent
names = ['01', '02a', '02b', '03', '04', '05', '06', '07', '08']
data = base64.b64decode(''.join((root / f'v3-source/part-{n}.b64').read_text() for n in names))
if hashlib.sha256(data).hexdigest() != 'b1d6608ea108341d12b22c45e1af5a6c27ee5701d2fa119c118cb0aad8567406':
    raise SystemExit('Base source checksum mismatch')
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    for entry in archive.infolist():
        path = Path(entry.filename)
        if path.is_absolute() or '..' in path.parts:
            raise SystemExit('Unsafe archive path')
        if entry.filename.startswith(('SalahZeit/', 'SalahZeit.xcodeproj/')) or entry.filename == 'scripts/build_unsigned_ipa.sh':
            archive.extract(entry, root)
for script in json.loads((root / 'scripts/source-patches.json').read_text()):
    subprocess.run([sys.executable, str(root / script)], cwd=root, check=True)
print('SalahPath source restored; release checkpoint remains 3.62 / 73')
