from pathlib import Path
import base64
import io
import tarfile

payload = "".join(
    Path(f"v311-patch/part-{index:02d}.b64").read_text().strip()
    for index in range(5)
)
raw = base64.b64decode(payload)

with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
    archive.extractall(Path("."))

Path("scripts/build_unsigned_ipa.sh").chmod(0o755)
print("SalahPath v3.11 reference home overlay applied")
