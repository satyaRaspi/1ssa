# Frontend

Version: 1.0.8  
Build: 20260701.8

React + Vite frontend for the Shakti Scheme Application prototype.

The UI shows versioning in the sidebar footer, top header badge, application footer, and Settings release history.

v1.0.8 includes the v1.0.5 tooltip UI and all earlier application features. It also updates startup handling at the project root to repair incomplete backend virtual environments.

Run with:

```bash
rm -f package-lock.json
npm config set registry https://registry.npmjs.org/
npm install --no-audit --no-fund
npm run dev
```
