# 文本转语音 (Text to Audio)

## 函数签名

```python
def text_to_audio(
    text: str,
    voice_id: str = "female-shaonv",
    output_path: str = "./output.mp3",
    model: str = "speech-02-hd",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
    emotion: str = "happy",
    format: str = "mp3",
    sample_rate: int = 32000,
    bitrate: int = 128000
) -> dict
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| text | str | 必填 | 要转换的文本，最大 10000 字符 |
| voice_id | str | "female-shaonv" | 声音 ID |
| output_path | str | "./output.mp3" | 输出文件路径 |
| model | str | "speech-02-hd" | 模型版本 |
| speed | float | 1.0 | 语速 [0.5, 2.0] |
| vol | float | 1.0 | 音量 [0.1, 10.0] |
| pitch | int | 0 | 音调 [-12, 12] |
| emotion | str | "happy" | 情感风格 |
| format | str | "mp3" | 输出格式 |
| sample_rate | int | 32000 | 采样率 |
| bitrate | int | 128000 | 比特率 |

## 可用情感

- `happy` - 开心
- `sad` - 悲伤
- `angry` - 愤怒
- `fearful` - 恐惧
- `disgusted` - 厌恶
- `surprised` - 惊讶
- `calm` - 平静
- `fluent` - 流畅
- `whisper` - 低语

## 输出格式

- `mp3` - MP3 格式
- `wav` - WAV 格式
- `pcm` - PCM 格式
- `flac` - FLAC 格式

## 使用示例

### 基础用法

```python
from minimax_tts import text_to_audio

result = text_to_audio(
    text="你好，世界！",
    output_path="./hello.mp3"
)
print(f"音频已保存到: {result['file_path']}")
```

### 指定声音和情感

```python
result = text_to_audio(
    text="今天天气真好啊！",
    voice_id="female-yujie",
    emotion="happy",
    speed=1.1,
    output_path="./weather.mp3"
)
```

### 使用克隆的声音

```python
result = text_to_audio(
    text="这是用我的声音生成的",
    voice_id="my-cloned-voice",  # 使用 voice_clone 创建的声音 ID
    output_path="./my_voice.mp3"
)
```

### 批量生成

```python
texts = [
    "第一段文字",
    "第二段文字",
    "第三段文字"
]

for i, text in enumerate(texts):
    text_to_audio(
        text=text,
        output_path=f"./output_{i+1}.mp3"
    )
```

## SSML 支持

MiniMax TTS 支持 SSML 标记来精细控制语音：

```python
ssml_text = """
<speak>
    你好<break time="500ms"/>
    <phoneme alphabet="pinyin" ph="chong2qing4">重庆</phoneme>欢迎你
    <prosody rate="slow" pitch="high">慢速高音调</prosody>
</speak>
"""

text_to_audio(text=ssml_text, output_path="./ssml_demo.mp3")
```

### 常用 SSML 标签

| 标签 | 说明 | 示例 |
|------|------|------|
| `<break>` | 停顿 | `<break time="500ms"/>` |
| `<phoneme>` | 拼音标注 | `<phoneme ph="hao3">好</phoneme>` |
| `<prosody>` | 韵律控制 | `<prosody rate="fast">快速</prosody>` |
| `<say-as>` | 朗读方式 | `<say-as interpret-as="digits">123</say-as>` |

## 返回值

```python
{
    "success": True,
    "file_path": "/path/to/output.mp3",
    "duration": 2.5,  # 音频时长（秒）
    "trace_id": "xxx"  # 请求追踪 ID
}
```

## 错误处理

```python
try:
    result = text_to_audio(text="测试", output_path="./test.mp3")
    if result["success"]:
        print(f"成功: {result['file_path']}")
except Exception as e:
    print(f"错误: {e}")
```
