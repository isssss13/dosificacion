module.exports = {

    entry: {
        graficas: './src/index.js',
    },

    output: {
        path: __dirname + '/dosificacion/static/js',
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: { loader: 'babel-loader' }
            },
        ]
    }    
}
