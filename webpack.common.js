const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/main.tsx',
  output: {
    path: path.resolve('../resources/ui'),
    publicPath: '/',
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(ts|tsx)$/,
        loader: 'tslint-loader',
        exclude: /node_modules/,
        options: {
          emitErrors: true
        }
      },
      {
        test: /\.(ts|tsx)$/,
        loader: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        loader:'style-loader!css-loader'
      },
      {
        test: /\.html$/,
        use: [{
          loader: 'html-loader',
          options: {
            minimize: true,
            removeComments: false,
            collapseWhitespace: false
          }
        }]
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        use: [{
          loader: 'file-loader',
          options: {}
        }]
      },
      {
        test: /\.js$/,
        loader: 'ify-loader'
      }
    ]
  },
  resolve: {
    alias: {
     'crossfilter': 'crossfilter2'
    }
  },
  performance: {
    hints: false
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html'
    }),
    new CopyWebpackPlugin([{
      from: './src/assets/',
      to: 'assets/',
      ignore: ['**/.DS_Store']
    }])
  ],
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx']
  }
};