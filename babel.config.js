const presets = [
	['@babel/preset-react'],
	['@babel/env', {
		targets: {
			browsers: [
				'Chrome >= 85',
				'Safari >= 13',
				'iOS >= 13',
				'Firefox >= 80',
			],
		},
		useBuiltIns: 'usage',
	}],
];

module.exports = { presets };
