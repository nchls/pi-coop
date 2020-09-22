module.exports = {
	env: {
		browser: true,
		es6: true,
	},
	extends: [
		'airbnb',
	],
	globals: {
		Atomics: 'readonly',
		SharedArrayBuffer: 'readonly'
	},
	parser: 'babel-eslint',
	parserOptions: {
		ecmaFeatures: {
			jsx: true,
		},
		ecmaVersion: 2018,
		sourceType: 'module',
	},
	plugins: [
		'react'
	],
	rules: {
		'indent': ["error", "tab"],
		'no-tabs': 0,
		'no-unused-vars': ['error', { varsIgnorePattern: 'React' }],
		'react/jsx-wrap-multilines': 0,
		'react/jsx-filename-extension': 0,
		'react/jsx-props-no-spreading': 0,
		'react/jsx-indent-props': ['error', 'tab'],
		'react/destructuring-assignment': 0,
		'max-len': ['warn', 120],
		'object-curly-newline': 0,
		'react/prop-types': 0,
		'arrow-body-style': 0,
		'react/jsx-indent': ['error', 'tab'],
		'react/no-unescaped-entities': 0,
		'react/jsx-one-expression-per-line': 0,
		'react/button-has-type': 0,
		'no-shadow': 0,
		'object-shorthand': 0,
		'radix': 0,
		'prefer-destructuring': 0,
		'no-use-before-define': 0,
		'quotes': ['error', 'single', { allowTemplateLiterals: true }],
		'no-console': 0,
		'no-debugger': 0,
		'import/prefer-default-export': 0,
		'consistent-return': 0,
		'no-plusplus': 0,
		'jsx-a11y/click-events-have-key-events': 0,
		'jsx-a11y/no-noninteractive-element-interactions': 0,
		'jsx-a11y/no-autofocus': 0,
	}
};
