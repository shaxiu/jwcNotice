// index.js
// 获取应用实例
const app = getApp()
Page({
  data: {
    notice: [],
    hasMoreNotice: true,
    isLoading: false,
  },
  onLoad() {
    let that = this;
    this.getNoticeList()
  },
  /**
   * 获取通知列表数据
   */
  getNoticeList: function () {
    let that = this
    let num = 12
    let page = Math.ceil(that.data.notice.length / num)
    // console.log(page)
    wx.showLoading({
      title: '加载中',
    })
    that.setData({
      isLoading: true
    })
    /**
     * 调用云函数
     */
    return wx.cloud.callFunction({
      name: 'getNoticeList',
      data: {
        len: num * page,
        num: num
      }
    }).then(res => {
      that.setData({
        notice: that.data.notice.concat(res.result.data)
      })
      if (res.result.data.length < num) {
        that.setData({
          hasMoreNotice: false
        })
      }
      that.setData({
        isLoading: false
      })
      wx.hideLoading()
    }).catch(res => {
      console.log("请求失败", res)
    })
  },
  /**
   * 显示通知详情页
   */
  showNotice: function (e) {
    let flag = e.currentTarget.dataset.flag;
    // console.log(flag)
    wx.navigateTo({
      url: '/pages/notice_detail/notice_detail?id=' + flag,
    })
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    // 如果无数据了就不要再发请求了
    if (!this.data.hasMoreNotice) return;
    // 节流
    if (!this.data.isLoading) {
      this.getNoticeList()
    }
  },
})