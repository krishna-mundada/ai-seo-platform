module.exports = {
  hooks: {
    readPackage(pkg) {
      // Allow esbuild to run scripts
      return pkg;
    }
  }
};