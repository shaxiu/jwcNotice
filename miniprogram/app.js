// app.js
App({
  onLaunch() {
    wx.cloud.init({
      env:'lyy-production'
    })
  },
})