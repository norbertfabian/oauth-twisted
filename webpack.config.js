const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const ENV = process.env.NODE_ENV && process.env.NODE_ENV.trim() || null;

const PATHS = {
    src: path.resolve(__dirname, 'src'),
    static: path.resolve(__dirname, 'oauth/static')
};

const PLUGIN = {
    copy: new CopyWebpackPlugin([
        { from: './node_modules/sass-font-awesome/fonts', to: path.join(PATHS.static, 'fonts')}
    ]),
    extractCss: new ExtractTextPlugin({
        filename: '[name].css'
    })
};

module.exports = {
    entry: {
        style: './src/index.scss'
    },
    output: {
        path: PATHS.static,
        filename: '[name].css'
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: PLUGIN.extractCss.extract({
                    fallback: 'style-loader',
                    use: [{
                        loader: 'css-loader',
                        options: {
                            minimize: true
                        }
                    }, {
                        loader: 'postcss-loader',
                        options: {
                            plugins() {
                                return [
                                    require('postcss-smart-import')({ path: ['src'] }),
                                    require('autoprefixer')({ flexbox: true })
                                ];
                            }
                        }
                    }, {
                        loader: 'sass-loader',
                        options: {
                            includePaths: [
                                "./src",
                                './node_modules/webapp-style-core/src',
                                './node_modules/sass-font-awesome',
                            ]
                        }
                    }]
                })
            }
        ]
    },
    plugins: [
        PLUGIN.copy,
        PLUGIN.extractCss
    ],
};
