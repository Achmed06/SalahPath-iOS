import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(here, "..");
const assetCatalog = path.join(projectRoot, "SalahZeit", "Assets.xcassets");
const publicAssets = path.join(here, "public", "assets");

fs.mkdirSync(publicAssets, { recursive: true });

function syncAssets() {
  if (!fs.existsSync(assetCatalog)) {
    console.warn("SalahZeit/Assets.xcassets not found. Preview will use fallbacks.");
    return;
  }

  const prefixes = ["feature_", "salahpath_logo", "home_mosque", "male_", "female_", "wudu_"];
  let copied = 0;

  for (const entry of fs.readdirSync(assetCatalog, { withFileTypes: true })) {
    if (!entry.isDirectory() || !entry.name.endsWith(".imageset")) continue;
    const assetName = entry.name.slice(0, -".imageset".length);
    if (!prefixes.some(prefix => assetName.startsWith(prefix))) continue;

    const folder = path.join(assetCatalog, entry.name);
    const contentsPath = path.join(folder, "Contents.json");
    if (!fs.existsSync(contentsPath)) continue;

    try {
      const payload = JSON.parse(fs.readFileSync(contentsPath, "utf8"));
      const image = payload.images?.find(item => item.filename)?.filename;
      if (!image) continue;
      const source = path.join(folder, image);
      if (!fs.existsSync(source)) continue;
      const ext = path.extname(image).toLowerCase() || ".svg";
      fs.copyFileSync(source, path.join(publicAssets, assetName + ext));
      copied++;
    } catch (error) {
      console.warn("Asset sync skipped:", assetName, error.message);
    }
  }

  console.log(`Synced ${copied} SalahPath assets into browser preview.`);
}

syncAssets();

const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".ico": "image/x-icon"
};

function safeFile(urlPath) {
  const clean = decodeURIComponent(urlPath.split("?")[0]);
  const requested = clean === "/" ? "/index.html" : clean;
  const resolved = path.resolve(here, "." + requested);
  if (!resolved.startsWith(here)) return null;
  return resolved;
}

const server = http.createServer((req, res) => {
  let file = safeFile(req.url || "/");
  if (!file) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    file = path.join(here, "index.html");
  }

  try {
    const ext = path.extname(file).toLowerCase();
    res.writeHead(200, {
      "Content-Type": mime[ext] || "application/octet-stream",
      "Cache-Control": ext === ".html" || ext === ".js" || ext === ".css" ? "no-store" : "no-cache"
    });
    fs.createReadStream(file).pipe(res);
  } catch (error) {
    res.writeHead(500);
    res.end(error.message);
  }
});

const port = Number(process.env.PORT || 5173);
const host = process.env.HOST || "127.0.0.1";

server.listen(port, host, () => {
  console.log("");
  console.log("SalahPath browser preview is running:");
  console.log(`  http://localhost:${port}`);
  console.log("");
  console.log("Press Ctrl+C to stop.");
});
