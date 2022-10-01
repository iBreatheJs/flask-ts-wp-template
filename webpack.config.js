const webpack = require('webpack')
const path = require('path')
const DeclarationBundlerPlugin = require('./declaration-bundler-webpack-plugin.fix')
// const UglifyJSPlugin = require('uglifyjs-webpack-plugin')
// const TerserPlugin = require("terser-webpack-plugin");


module.exports = {
    entry: {
        mylib: path.resolve(__dirname, 'src/ts/init.ts')
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: [/node_modules/],
                loader: 'ts-loader'
            }
        ]
    },
    resolve: { extensions: ['.ts', '.js'] },
    output: {
        publicPath: "static",
        path: path.resolve(__dirname, 'src/server/static/'),
        chunkFilename: 'bundle.js',
        filename: 'bundle.js'
    },

    mode: 'development',
    // watch: true,
    // plugins: [
    //     // new TerserPlugin(),
    //     new DeclarationBundlerPlugin({
    //         moduleName: '"mylib"',
    //         out: '@types/index.d.ts'
    //     })
    // ],
    devtool: 'source-map',
    optimization: {
        // splitChunks: {
        //     cacheGroups: {
        //         vendors: {
        //             priority: -10,
        //             test: /[\\/]node_modules[\\/]/
        //         }
        //     },

        //     chunks: 'async',
        //     minChunks: 1,
        //     minSize: 30000,
        //     name: true
        // }
    }
}