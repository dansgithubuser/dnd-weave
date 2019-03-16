const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  publicPath: 'http://0.0.0.0:8080/',
  chainWebpack: config => {
    config.plugin('BundleTracker')
      .use(BundleTracker)
    config.entryPoints.delete('app');
    config.entry('plaintext_explorer').add('./src/plaintext_explorer.js');
  },
};
