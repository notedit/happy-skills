# 环境配置

## 获取 MiniMax API Key

1. 访问 [MiniMax 开放平台](https://platform.minimaxi.com/)
2. 注册/登录账号
3. 在控制台创建应用
4. 获取 API Key

## 设置环境变量

### macOS / Linux

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# MiniMax TTS 配置 (必需)
export MINIMAX_API_KEY="your-api-key-here"

# 可选配置
export MINIMAX_API_HOST="https://api.minimax.io"  # API 地址
export MINIMAX_OUTPUT_DIR="~/Downloads/minimax"   # 默认输出目录
```

添加后执行：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

### 验证配置

```bash
echo $MINIMAX_API_KEY
```

## 安装依赖

```bash
pip install requests
```

## 测试连接

```python
import sys
import os

# 添加 assets 目录到路径
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(skill_dir, "assets"))

from minimax_tts import list_voices

# 测试 API 连接
voices = list_voices(voice_type="system")
print(f"连接成功，获取到 {len(voices)} 个系统声音")
```

## 常见问题

### API Key 未设置
```
ValueError: 请设置环境变量 MINIMAX_API_KEY
```
解决方法：确保已正确设置环境变量并重新加载配置。

### 网络连接失败
检查网络连接和 API 地址是否正确。

### 权限不足
确认 API Key 有相应的权限。
