# 声音设计 (Voice Design)

## 函数签名

```python
def voice_design(
    prompt: str,
    preview_text: str,
    voice_id: str = None,
    voice_name: str = None
) -> dict
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | str | 必填 | 声音描述（中文或英文） |
| preview_text | str | 必填 | 试听预览文本 |
| voice_id | str | None | 保存时的声音 ID |
| voice_name | str | None | 声音名称 |

## 使用示例

### 生成预览

```python
from minimax_tts import voice_design

result = voice_design(
    prompt="一个温柔的年轻女性声音，带有轻微的南方口音，语速适中",
    preview_text="你好，欢迎来到我们的节目"
)

if result["success"]:
    # 播放预览
    from minimax_tts import play_audio
    play_audio(result["preview_audio"])
```

### 保存设计的声音

```python
result = voice_design(
    prompt="深沉有磁性的中年男声，像电台主播",
    preview_text="晚上好，欢迎收听今晚的节目",
    voice_id="radio-host",
    voice_name="电台主播"
)

if result["success"]:
    print(f"声音已保存: {result['voice_id']}")
```

## Prompt 编写技巧

### 描述维度

1. **性别和年龄**
   - 年轻女性、中年男性、老年人

2. **音色特点**
   - 温柔、沙哑、清亮、低沉、磁性

3. **说话风格**
   - 活泼、稳重、专业、亲切

4. **口音特征**
   - 标准普通话、南方口音、北方口音

5. **情感倾向**
   - 愉快、平静、严肃、热情

### 优秀 Prompt 示例

#### 新闻播音
```
专业的新闻播音员声音，男性，中年，
声音浑厚有力，吐字清晰，
语速适中，富有权威感
```

#### 有声书旁白
```
温柔的女性声音，年轻，
声音清亮悦耳，富有感染力，
适合讲述故事，能够表达丰富的情感
```

#### 儿童节目
```
活泼可爱的年轻女声，
声音甜美清脆，充满活力，
语调活泼有趣，适合儿童内容
```

#### 商务配音
```
成熟稳重的男性声音，中年，
声音低沉有磁性，专业可信，
适合商务场合和产品介绍
```

### 避免的描述

- 过于简短: "女声" ❌
- 矛盾的描述: "温柔且愤怒" ❌
- 不相关的信息: "穿红色衣服的人" ❌

## 返回值

### 成功

```python
{
    "success": True,
    "voice_id": "radio-host",  # 如果提供了 voice_id
    "preview_audio": "/tmp/preview_xxx.mp3",
    "voice_features": {
        "gender": "male",
        "age": "middle",
        "style": "professional"
    }
}
```

### 失败

```python
{
    "success": False,
    "error": "描述不够清晰",
    "suggestion": "请提供更详细的声音特征描述"
}
```

## 工作流程

### 1. 迭代设计

```python
# 第一次尝试
result1 = voice_design(
    prompt="温柔的女声",
    preview_text="测试文本"
)
play_audio(result1["preview_audio"])

# 根据效果调整
result2 = voice_design(
    prompt="更加温柔甜美的年轻女声，带有轻微的撒娇感",
    preview_text="测试文本"
)
play_audio(result2["preview_audio"])

# 满意后保存
result3 = voice_design(
    prompt="更加温柔甜美的年轻女声，带有轻微的撒娇感",
    preview_text="测试文本",
    voice_id="sweet-girl",
    voice_name="甜美女声"
)
```

### 2. 使用设计的声音

```python
from minimax_tts import text_to_audio

text_to_audio(
    text="这是用设计的声音生成的",
    voice_id="sweet-girl",
    output_path="./designed_output.mp3"
)
```

## 与声音克隆的对比

| 特性 | 声音设计 | 声音克隆 |
|------|----------|----------|
| 输入 | 文字描述 | 音频文件 |
| 相似度 | 符合描述 | 高度相似 |
| 灵活性 | 高，可任意设计 | 受限于样本 |
| 使用场景 | 创造新声音 | 复制特定声音 |

## 注意事项

1. 设计的声音是 AI 生成的，不代表真实人物
2. 每次设计可能产生略有不同的结果
3. 复杂的描述可能需要多次调整
4. 建议先预览再保存
