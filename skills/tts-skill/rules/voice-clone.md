# 声音克隆 (Voice Clone)

## 函数签名

```python
def voice_clone(
    voice_id: str,
    audio_file: str,
    voice_name: str = None,
    voice_description: str = None,
    demo_text: str = None
) -> dict
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| voice_id | str | 必填 | 自定义声音 ID（唯一标识） |
| audio_file | str | 必填 | 音频文件路径 |
| voice_name | str | None | 声音名称（可选） |
| voice_description | str | None | 声音描述（可选） |
| demo_text | str | None | 试听文本（可选） |

## 音频要求

### 格式支持
- MP3, WAV, M4A, FLAC

### 最佳实践
- **时长**: 10-60 秒
- **质量**: 清晰无噪音
- **内容**: 自然说话，包含多种音调
- **环境**: 安静环境录制

## 使用示例

### 基础克隆

```python
from minimax_tts import voice_clone

result = voice_clone(
    voice_id="my-voice-001",
    audio_file="./my_recording.mp3"
)

if result["success"]:
    print(f"声音克隆成功: {result['voice_id']}")
```

### 完整参数

```python
result = voice_clone(
    voice_id="custom-narrator",
    audio_file="./narrator_sample.mp3",
    voice_name="专业旁白",
    voice_description="深沉有力的男声旁白",
    demo_text="这是一段试听文本"
)
```

### 使用克隆的声音

```python
from minimax_tts import text_to_audio

# 克隆后即可使用
text_to_audio(
    text="这是用我克隆的声音生成的",
    voice_id="my-voice-001",
    output_path="./cloned_output.mp3"
)
```

## 返回值

### 成功

```python
{
    "success": True,
    "voice_id": "my-voice-001",
    "voice_name": "我的声音",
    "status": "ready",  # ready, processing, failed
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 失败

```python
{
    "success": False,
    "error": "音频质量不符合要求",
    "error_code": "AUDIO_QUALITY_LOW"
}
```

## 录制建议

### 推荐设备
- 专业麦克风或手机录音
- 避免使用蓝牙耳机

### 录制环境
- 安静的室内环境
- 避免回声和噪音
- 关闭空调、风扇等

### 录制内容
- 自然流畅地说话
- 包含不同语调和情感
- 避免过长的停顿

### 示例脚本

```
大家好，我是[名字]。今天天气真不错。
我很高兴能够和大家分享这段内容。
让我们一起来看看接下来会发生什么。
这真是一个令人惊喜的消息！
好的，谢谢大家的收听。
```

## 管理克隆声音

### 查看所有克隆声音

```python
from minimax_tts import list_voices

cloned = list_voices(voice_type="cloned")
for voice in cloned:
    print(f"{voice['voice_id']}: {voice['name']}")
```

### 删除克隆声音

```python
# 暂不支持 API 删除，需要在控制台操作
```

## 常见问题

### 克隆失败
- 检查音频质量和时长
- 确保音频中只有一个人说话
- 尝试重新录制更清晰的音频

### 克隆效果不好
- 使用更长的样本（30 秒以上）
- 确保样本包含丰富的语调变化
- 选择更清晰的录音环境

## 注意事项

1. voice_id 必须唯一，重复会覆盖
2. 克隆可能需要几秒钟处理
3. 克隆声音仅供个人使用
4. 请确保有权使用所提供的音频
