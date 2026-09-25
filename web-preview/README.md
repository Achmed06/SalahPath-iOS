# SalahPath local browser preview

This is a fast local browser mirror for UI iteration. It does not replace the native SwiftUI runtime.

## Windows PowerShell

From the repository root:

```powershell
cd web-preview
npm run dev
```

Then open:

```text
http://localhost:5173
```

No `npm install` is required because the preview server uses only Node.js built-in modules.

At startup it copies current SalahPath feature, prayer and Wudu assets from `SalahZeit/Assets.xcassets` into its local preview asset folder.
