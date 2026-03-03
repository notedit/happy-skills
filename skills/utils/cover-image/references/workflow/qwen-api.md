# Qwen Image API 调用指南

## API 端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
```

## 环境变量

```bash
DASHSCOPE_API_KEY=your-api-key
```

## Python 调用示例

```python
import requests
import os
import json
import time

def generate_cover(prompt, output_path, size='1664*928'):
    """
    使用 Qwen-Image-Plus 生成封面图片
    
    Args:
        prompt: 图片描述提示词
        output_path: 输出图片路径
        size: 图片尺寸 (1664*928, 1024*1024, 928*1664, 1472*1104, 1104*1472)
    
    Returns:
        str: 生成的图片路径
    """
    api_key = os.environ.get('DASHSCOPE_API_KEY')
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'X-DashScope-Async': 'enable'  # 异步模式
    }
    
    payload = {
        'model': 'qwen-image-plus',
        'input': {
            'prompt': prompt
        },
        'parameters': {
            'size': size,
            'n': 1
        }
    }
    
    # 1. 提交任务
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis'
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if 'output' not in result or 'task_id' not in result['output']:
        raise Exception(f"Task creation failed: {result}")
    
    task_id = result['output']['task_id']
    
    # 2. 轮询任务状态
    for i in range(60):  # 最多等待 3 分钟
        time.sleep(3)
        query_url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
        query_response = requests.get(query_url, headers={'Authorization': f'Bearer {api_key}'})
        query_result = query_response.json()
        status = query_result.get('output', {}).get('task_status', 'UNKNOWN')
        
        if status == 'SUCCEEDED':
            # 3. 下载图片
            image_url = query_result['output']['results'][0]['url']
            img_response = requests.get(image_url)
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            return output_path
        
        elif status == 'FAILED':
            raise Exception(f"Generation failed: {query_result}")
    
    raise Exception("Generation timeout after 3 minutes")


def resize_for_wechat(input_path, output_path):
    """
    将图片调整为公众号封面尺寸 900x383
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
    """
    from PIL import Image
    
    img = Image.open(input_path)
    
    # 缩放并裁剪
    img_resized = img.resize((900, 502), Image.LANCZOS)
    top = (502 - 383) // 2
    img_crop = img_resized.crop((0, top, 900, top + 383))
    img_crop.save(output_path)
    
    return output_path
```

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| `Throttling.RateQuota` | 请求限流 | 等待 60 秒后重试 |
| `InvalidParameter` | 参数错误 | 检查 prompt 和 size 参数 |
| `DataInspectionFailed` | 内容审核失败 | 修改 prompt 内容 |

## 尺寸映射

| 目标比例 | Qwen Size | 公众号适配 |
|----------|-----------|------------|
| 16:9 | `1664*928` | 裁剪为 900x383 |
| 1:1 | `1024*1024` | 裁剪为 900x383 |
| 2.35:1 | `1664*928` | 直接缩放 |
| 4:3 | `1472*1104` | 裁剪适配 |
