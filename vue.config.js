const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  chainWebpack: config => {
    config.plugin('BundleTracker')
      .use(BundleTracker)
    config.entryPoints.delete('app');
    config.entry('plaintext_explorer').add('./frontend/plaintext_explorer.js');
    config.optimization.delete('splitChunks')
  },
};

if (process.env.NODE_ENV === 'production') {
  module.exports.publicPath = '/static/';
} else {
  module.exports.publicPath = 'http://0.0.0.0:8080/';
}
