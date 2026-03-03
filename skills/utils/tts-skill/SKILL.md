---
name: tts-skill
description: MiniMax TTS API - 文本转语音、声音克隆、声音设计
metadata:
  tags: minimax, tts, voice, audio, speech
---

# MiniMax TTS Skill

这个 Skill 提供 MiniMax TTS API 的完整封装，支持文本转语音、声音克隆和声音设计功能。

## 快速开始

### 1. 环境配置

确保已设置环境变量：
```bash
export MINIMAX_API_KEY="your-api-key"
```

详细配置说明见 [setup.md](rules/setup.md)

### 2. 使用 Python 模块

```python
import sys
import os

# 获取 skill 目录路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(skill_dir, "assets"))

from minimax_tts import text_to_audio, list_voices, voice_clone, voice_design, play_audio
```

## 功能概览

| 功能 | 函数 | 说明 |
|------|------|------|
| 文本转语音 | `text_to_audio()` | 将文本转换为语音文件 |
| 列出声音 | `list_voices()` | 获取可用的声音列表 |
| 声音克隆 | `voice_clone()` | 基于音频文件克隆声音 |
| 声音设计 | `voice_design()` | 根据文字描述生成声音 |
| 播放音频 | `play_audio()` | 播放音频文件 |

## 详细文档

- [环境配置](rules/setup.md) - API Key 和依赖安装
- [文本转语音](rules/text-to-audio.md) - TTS 功能详解
- [声音列表](rules/list-voices.md) - 可用声音和筛选
- [声音克隆](rules/voice-clone.md) - 克隆自定义声音
- [声音设计](rules/voice-design.md) - 根据描述生成声音

## 快速示例

### 文本转语音
```python
text_to_audio(
    text="你好，欢迎使用 MiniMax TTS 服务！",
    voice_id="female-shaonv",
    output_path="./hello.mp3"
)
```

### 列出可用声音
```python
voices = list_voices(voice_type="system")
for voice in voices:
    print(f"{voice['voice_id']}: {voice['name']}")
```

### 声音克隆
```python
voice_clone(
    voice_id="my-custom-voice",
    audio_file="./sample.mp3",
    voice_name="我的声音"
)
```

### 声音设计
```python
voice_design(
    prompt="一个温柔的年轻女性声音，带有轻微的南方口音",
    preview_text="你好，这是我的声音"
)
```

## 支持的模型

| 模型 | 说明 |
|------|------|
| speech-02-hd | 高清版本，音质最佳 |
| speech-02-turbo | 快速版本，延迟低 |
| speech-01-hd | 旧版高清 |
| speech-01-turbo | 旧版快速 |
| speech-2.6-hd | 2.6 版高清 |
| speech-2.6-turbo | 2.6 版快速 |

## 常用声音 ID

### 系统预设声音
- `female-shaonv` - 少女音
- `female-yujie` - 御姐音
- `female-chengshu` - 成熟女声
- `male-qingnian` - 青年男声
- `male-chengshu` - 成熟男声

更多声音请使用 `list_voices()` 查询。
