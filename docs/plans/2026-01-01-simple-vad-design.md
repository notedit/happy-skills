# Simple VAD 设计文档

## 概述

实现一个简单的浏览器端 VAD（Voice Activity Detection），用于语音助手场景，检测用户开始/停止说话。

## 需求

- **场景**：语音助手，检测用户说话触发录音/识别
- **环境**：浏览器，Web Audio API
- **方案**：基于音量阈值，简单快速

## 架构

```
┌─────────────┐    ┌───────────────┐    ┌─────────────┐
│ getUserMedia │ → │  AnalyserNode  │ → │   VAD 检测   │
│   (麦克风)   │    │   (音频分析)   │    │  (阈值判断)  │
└─────────────┘    └───────────────┘    └─────────────┘
                                              ↓
                                    ┌─────────────────┐
                                    │      状态机      │
                                    │ SILENT ↔ SPEAKING │
                                    └─────────────────┘
                                              ↓
                                    ┌─────────────────┐
                                    │     事件回调     │
                                    │  onSpeechStart  │
                                    │   onSpeechEnd   │
                                    └─────────────────┘
```

**核心组件**：
1. **音频采集** - `getUserMedia` 获取麦克风输入
2. **音量分析** - `AnalyserNode` 获取音频数据
3. **状态机** - 管理 `SILENT` / `SPEAKING` 状态切换
4. **事件系统** - 触发 `onSpeechStart` / `onSpeechEnd` 回调

## 状态机

```
        音量 > 阈值 (连续 N 帧)
    ┌─────────────────────────────┐
    │                             ▼
┌───────┐                    ┌──────────┐
│ SILENT │                    │ SPEAKING │
└───────┘                    └──────────┘
    ▲                             │
    └─────────────────────────────┘
        音量 < 阈值 (连续 M 帧)
```

### 参数配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `threshold` | 0.02 | 音量阈值 (0-1)，需根据环境调整 |
| `speechStartFrames` | 3 | 连续 N 帧超过阈值才判定开始说话 |
| `silenceEndFrames` | 15 | 连续 M 帧低于阈值才判定停止说话 |
| `pollInterval` | 50ms | 轮询间隔 |

## API 设计

### 使用示例

```typescript
// 创建 VAD 实例
const vad = new SimpleVAD({
  threshold: 0.02,
  silenceEndFrames: 15,
  onSpeechStart: () => {
    console.log('用户开始说话');
    startRecording();
  },
  onSpeechEnd: () => {
    console.log('用户停止说话');
    stopRecordingAndSendToASR();
  }
});

// 启动
await vad.start();

// 停止
vad.stop();

// 动态调整阈值
vad.setThreshold(0.03);
```

### 类型定义

```typescript
interface VADOptions {
  threshold?: number;
  speechStartFrames?: number;
  silenceEndFrames?: number;
  pollInterval?: number;
  onSpeechStart?: () => void;
  onSpeechEnd?: () => void;
}
```

## 文件结构

```
src/
  └── vad/
      └── SimpleVAD.ts    # 单文件实现，约 80 行
```

## 错误处理

```typescript
try {
  await vad.start();
} catch (err) {
  if (err.name === 'NotAllowedError') {
    // 用户拒绝麦克风权限
  } else if (err.name === 'NotFoundError') {
    // 没有麦克风设备
  }
}
```

## 注意事项

| 问题 | 解决方案 |
|------|----------|
| 环境噪音大 | 调高 `threshold` |
| 说话检测太慢 | 减少 `speechStartFrames` |
| 说话结束太快 | 增加 `silenceEndFrames` |
| 浏览器兼容性 | 需要 HTTPS 或 localhost |

**资源清理**：
- `stop()` 时自动释放 `AudioContext` 和 `MediaStream`
- 页面卸载时建议调用 `stop()` 避免麦克风占用
