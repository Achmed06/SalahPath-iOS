from pathlib import Path
import base64, gzip

payload = Path("v342-patch/apply_v342.py.gz.b64").read_text(encoding="utf-8").strip()
source = gzip.decompress(base64.b64decode(payload)).decode("utf-8")
exec(compile(source, "v342-patch/apply_v342.py", "exec"))
