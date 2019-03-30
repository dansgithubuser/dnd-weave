const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  chainWebpack: config => {
    config.plugin('BundleTracker').use(BundleTracker);
    config.entryPoints.delete('app');
    config.entry('plaintext_explorer').add('./frontend/plaintext_explorer.js');
    config.entry('secretmaker').add('./frontend/secretmaker.js');
    config.entry('spellgranter').add('./frontend/spellgranter.js');
    config.entry('character_delver').add('./frontend/character_delver.js');
    config.optimization.delete('splitChunks');
  },
};

if (process.env.NODE_ENV === 'production') {
  module.exports.publicPath = '/static/';
} else {
  module.exports.publicPath = 'http://0.0.0.0:8080/';
}
