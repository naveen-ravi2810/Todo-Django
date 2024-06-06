const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '^/api': {
        target: process.env.BACKENDSERVER_URL,
        ws: true,
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      },
    }
  }
})
