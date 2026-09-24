# Node Review

Review

Server startup

Memory usage

Unhandled promises

Exception handling

Graceful shutdown

Health endpoint

Compression

Security headers

Logging

Rate limiting

Request validation

## ECMAScript Modules (ESM) & TypeScript NodeNext

If the project is using `"type": "module"` in `package.json` and `"moduleResolution": "NodeNext"` in `tsconfig.json`:
- Ensure **ALL** relative imports within `.ts` files explicitly include the `.js` extension (e.g., `import { Service } from './service.js';`).
- Without this, the `tsc` compiler will throw `TS2835` and `TS2307` module resolution errors during the Hostinger build step.
- Verify `"esModuleInterop": true` is set in `tsconfig.json` to handle CommonJS default exports cleanly.
