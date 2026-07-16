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

// El monorepo tiene otra app (admin) con su propia version de React (para
// web). Con hierarchical lookup activo, Metro a veces resolvia "react" hacia
// esa copia hoisteada en vez de la de mobile, causando "Invalid hook call"
// (dos copias de React coexistiendo). Fijamos explicitamente cuales archivos
// usar para estos paquetes, sin importar el resto de la resolucion.
config.resolver.extraNodeModules = {
  react: path.resolve(projectRoot, "node_modules/react"),
  "react-native": path.resolve(projectRoot, "node_modules/react-native"),
};

module.exports = config;
