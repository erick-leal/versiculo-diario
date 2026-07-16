const { getDefaultConfig } = require("expo/metro-config");
const path = require("path");

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, "../..");

const config = getDefaultConfig(projectRoot);

// A diferencia de un monorepo npm/yarn, pnpm hoistea paquetes dentro de
// node_modules/.pnpm/node_modules/, no directamente en la raiz. Metro necesita
// poder recorrer los node_modules hacia arriba (hierarchical lookup) para
// encontrarlos ahi, asi que NO lo deshabilitamos.
config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, "node_modules"),
  path.resolve(workspaceRoot, "node_modules"),
];
config.resolver.unstable_enableSymlinks = true;

module.exports = config;
