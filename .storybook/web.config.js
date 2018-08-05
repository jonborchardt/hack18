const TSDocgenPlugin = require('react-docgen-typescript-webpack-plugin');

module.exports = (baseConfig, env, defaultConfig) => {
    defaultConfig.module.rules.push({
        test: /\.(ts|tsx)$/,
        loader: 'ts-loader',
        exclude: /node_modules/
    });
    defaultConfig.plugins.push(new TSDocgenPlugin());
    defaultConfig.resolve.extensions.push('.ts', '.tsx');
    return defaultConfig;
};