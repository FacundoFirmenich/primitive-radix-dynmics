# Recent integrated modules · RC3.3

See [RESULTS.md](RESULTS.md) for all 24 added claims and their scopes. `SOURCE_MANIFEST.json` pins the 31 imported code/data files; `figure-assets/` contains ten approved standalone SVG sources.

From the repository root, run `make recent-verify`. The runner uses temporary copies, checks imported hashes before and after, and writes its current logs and receipt to `outputs/reports/recent/`. No private manuscript is required. The complete T5000 census is a separate `make recent-full-census` target.
