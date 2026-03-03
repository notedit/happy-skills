# 列出可用声音 (List Voices)

## 函数签名

```python
def list_voices(voice_type: str = "all") -> list
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| voice_type | str | "all" | 声音类型筛选 |

### voice_type 可选值

- `all` - 所有声音
- `system` - 系统预设声音
- `cloned` - 用户克隆的声音
- `designed` - 用户设计的声音

## 使用示例

### 获取所有声音

```python
from minimax_tts import list_voices

voices = list_voices()
for voice in voices:
    print(f"{voice['voice_id']}: {voice['name']}")
```

### 只获取系统声音

```python
system_voices = list_voices(voice_type="system")
print(f"共 {len(system_voices)} 个系统声音")
```

### 获取用户克隆的声音

```python
cloned_voices = list_voices(voice_type="cloned")
for voice in cloned_voices:
    print(f"克隆声音: {voice['voice_id']} - {voice['name']}")
```

## 返回值格式

```python
[
    {
        "voice_id": "female-shaonv",
        "name": "少女音",
        "type": "system",
        "language": "zh",
        "description": "清新活泼的少女声音",
        "sample_url": "https://..."  # 试听链接
    },
    {
        "voice_id": "my-cloned-voice",
        "name": "我的声音",
        "type": "cloned",
        "language": "zh",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

## 系统预设声音列表

### 女声

| voice_id | 名称 | 特点 |
|----------|------|------|
| female-shaonv | 少女音 | 清新活泼 |
| female-yujie | 御姐音 | 成熟知性 |
| female-chengshu | 成熟女声 | 稳重大方 |
| female-tianmei | 甜美音 | 温柔甜美 |
| female-qingxin | 清新音 | 自然清新 |

### 男声

| voice_id | 名称 | 特点 |
|----------|------|------|
| male-qingnian | 青年男声 | 朝气蓬勃 |
| male-chengshu | 成熟男声 | 沉稳大气 |
| male-磁性 | 磁性男声 | 低沉有磁性 |

### 特殊声音

| voice_id | 名称 | 特点 |
|----------|------|------|
| narrator | 旁白音 | 适合叙述 |
| news | 新闻播音 | 标准播音腔 |

## 筛选和搜索

### 按语言筛选

```python
voices = list_voices()
chinese_voices = [v for v in voices if v.get("language") == "zh"]
english_voices = [v for v in voices if v.get("language") == "en"]
```

### 按名称搜索

```python
voices = list_voices()
female_voices = [v for v in voices if "女" in v.get("name", "")]
```

## 注意事项

1. 系统声音 ID 是固定的，不会改变
2. 克隆和设计的声音 ID 是在创建时指定的
3. 建议缓存声音列表，避免频繁调用 API
