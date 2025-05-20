<template>
  <view class="container">
    <view class="title">📋 会议废话总结器</view>
    <view class="desc">粘贴会议内容，AI 自动提炼重点，顺便吐槽一下废话</view>

    <!-- 风格选择 -->
    <picker :range="modes" @change="onModeChange">
      <view class="picker">
        🛠 当前模式：{{ modes[selectedMode] }}
      </view>
    </picker>

    <!-- 输入框 -->
    <textarea
      v-model="inputText"
      class="textarea"
      placeholder="请粘贴或输入会议记录，支持多段内容..."
      auto-height
    />

    <!-- 提交按钮 -->
    <button :loading="loading" @click="submitText" type="primary" class="btn">
      {{ loading ? 'AI 正在思考中...' : '✏️ 一键总结' }}
    </button>

    <!-- 结果展示 -->
    <view v-if="summary" class="result-box">
      <view class="result-title">📌 总结结果：</view>
      <view class="summary-text">{{ summary }}</view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      inputText: '',
      summary: '',
      loading: false,
      modes: ['正经模式', '吐槽模式'],
      selectedMode: 0, // 0: formal, 1: funny
    }
  },
  methods: {
    onModeChange(e) {
      this.selectedMode = Number(e.detail.value)
    },
    submitText() {
      if (!this.inputText.trim()) {
        uni.showToast({ title: '请输入内容', icon: 'none' })
        return
      }
      this.loading = true

      const mode = this.selectedMode === 1 ? 'funny' : 'formal'

      uni.request({
        url: 'https://meeting-demo-au6n.onrender.com/summarize', // 改为你的后端地址
        method: 'POST',
        data: {
          text: this.inputText,
          mode: mode
        },
        header: {
          'Content-Type': 'application/json'
        },
        success: (res) => {
          this.summary = res.data.summary || '未能获取总结结果'
        },
        fail: () => {
          uni.showToast({ title: '请求失败，请检查后端', icon: 'none' })
        },
        complete: () => {
          this.loading = false
        }
      })
    }
  }
}
</script>

<style>
.container {
  padding: 30rpx;
  font-family: system-ui;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10rpx;
}

.desc {
  font-size: 28rpx;
  color: #666;
  text-align: center;
  margin-bottom: 40rpx;
}

.picker {
  background-color: #f0f0f0;
  padding: 20rpx;
  border-radius: 16rpx;
  font-size: 28rpx;
  margin-bottom: 20rpx;
}

.textarea {
  background: #fff;
  padding: 20rpx;
  border: 1px solid #ccc;
  border-radius: 16rpx;
  min-height: 300rpx;
  margin-bottom: 30rpx;
  font-size: 28rpx;
}

.btn {
  width: 100%;
  font-size: 32rpx;
  border-radius: 16rpx;
  margin-bottom: 40rpx;
}

.result-box {
  background: #f9f9f9;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-top: 20rpx;
}

.result-title {
  font-size: 30rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
}

.summary-text {
  font-size: 28rpx;
  line-height: 1.7;
  white-space: pre-wrap;
}
</style>
