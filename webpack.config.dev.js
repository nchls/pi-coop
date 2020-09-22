const path = require('path');

const config = require('./webpack.config.js');

config.mode = 'development';

config.devtool = 'source-map';

config.devServer = {
	contentBase: path.join(__dirname, 'dashboard', 'dist'),
};

module.exports = config;
