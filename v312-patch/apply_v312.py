from pathlib import Path
import base64
import io
import tarfile

parts = [
    "v312-patch/part-00.b64",
    "v312-patch/part-01.b64",
    "v312-patch/part-02.b64",
    "v312-patch/part-03a.b64",
    "v312-patch/part-03b.b64",
    "v312-patch/part-04a.b64",
    "v312-patch/part-04b.b64",
    "v312-patch/part-05.b64",
]

payload = "".join(Path(path).read_text().strip() for path in parts)
raw = base64.b64decode(payload)

with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
    archive.extractall(Path("."))

Path("scripts/build_unsigned_ipa.sh").chmod(0o755)
print("SalahPath v3.12 reference visual parity overlay applied")
