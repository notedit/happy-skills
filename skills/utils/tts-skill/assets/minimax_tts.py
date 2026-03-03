#!/usr/bin/env python3
"""
MiniMax TTS API Python Module

提供文本转语音、声音克隆、声音设计等功能的完整封装。

使用方法:
    import sys
    import os

    # 方式1: 直接添加 assets 目录
    sys.path.insert(0, "/path/to/skills/tts-skill/assets")
    from minimax_tts import text_to_audio, list_voices, voice_clone, voice_design, play_audio

    # 方式2: 相对路径
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(skill_dir, "assets"))
    from minimax_tts import text_to_audio, list_voices, voice_clone, voice_design, play_audio

环境变量:
    MINIMAX_API_KEY: API 密钥 (必需)
    MINIMAX_API_HOST: API 地址 (可选，默认 https://api.minimax.io)
    MINIMAX_OUTPUT_DIR: 默认输出目录 (可选)
"""

import os
import json
import base64
import subprocess
import platform
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

try:
    import requests
except ImportError:
    raise ImportError("请安装 requests: pip install requests")


# ============================================================
# 配置
# ============================================================

def get_config() -> Dict[str, str]:
    """获取配置信息"""
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError(
            "请设置环境变量 MINIMAX_API_KEY\n"
            "在 ~/.zshrc 或 ~/.bashrc 中添加:\n"
            "export MINIMAX_API_KEY=\"your-api-key\""
        )

    return {
        "api_key": api_key,
        "api_host": os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io"),
        "output_dir": os.environ.get("MINIMAX_OUTPUT_DIR", os.getcwd())
    }


def ensure_output_dir(path: str = None) -> str:
    """确保输出目录存在"""
    if path:
        dir_path = Path(path).parent
    else:
        config = get_config()
        dir_path = Path(config["output_dir"])

    dir_path.mkdir(parents=True, exist_ok=True)
    return str(dir_path)


# ============================================================
# 文本转语音
# ============================================================

def text_to_audio(
    text: str,
    voice_id: str = "female-shaonv",
    output_path: str = None,
    model: str = "speech-02-hd",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
    emotion: str = "happy",
    format: str = "mp3",
    sample_rate: int = 32000,
    bitrate: int = 128000
) -> Dict[str, Any]:
    """
    将文本转换为语音文件

    Args:
        text: 要转换的文本，最大 10000 字符
        voice_id: 声音 ID
        output_path: 输出文件路径
        model: 模型版本 (speech-02-hd, speech-02-turbo, etc.)
        speed: 语速 [0.5, 2.0]
        vol: 音量 [0.1, 10.0]
        pitch: 音调 [-12, 12]
        emotion: 情感 (happy, sad, angry, fearful, disgusted, surprised, calm, fluent, whisper)
        format: 输出格式 (mp3, wav, pcm, flac)
        sample_rate: 采样率
        bitrate: 比特率

    Returns:
        dict: 包含 success, file_path, duration, trace_id 等信息
    """
    config = get_config()

    # 处理输出路径
    if output_path is None:
        ensure_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(config["output_dir"], f"tts_{timestamp}.{format}")
    else:
        output_path = os.path.expanduser(output_path)
        ensure_output_dir(output_path)

    # 构建请求
    url = f"{config['api_host']}/v1/t2a_v2"

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
            "emotion": emotion
        },
        "audio_setting": {
            "format": format,
            "sample_rate": sample_rate,
            "bitrate": bitrate
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        if "data" in result and "audio" in result["data"]:
            # 解码并保存音频 (API 返回的是十六进制编码)
            audio_data = bytes.fromhex(result["data"]["audio"])
            with open(output_path, "wb") as f:
                f.write(audio_data)

            return {
                "success": True,
                "file_path": output_path,
                "duration": result.get("data", {}).get("duration"),
                "trace_id": result.get("trace_id"),
                "extra_info": result.get("extra_info")
            }
        else:
            return {
                "success": False,
                "error": result.get("base_resp", {}).get("status_msg", "未知错误"),
                "error_code": result.get("base_resp", {}).get("status_code")
            }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# 声音列表
# ============================================================

def list_voices(voice_type: str = "all") -> List[Dict[str, Any]]:
    """
    列出可用的声音

    Args:
        voice_type: 声音类型筛选 (all, system, cloned, designed)

    Returns:
        list: 声音列表
    """
    config = get_config()

    url = f"{config['api_host']}/v1/voice/list"

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        result = response.json()
        voices = result.get("data", {}).get("voices", [])

        # 如果 API 没有返回数据，返回默认系统声音列表
        if not voices:
            voices = get_default_system_voices()

        # 筛选
        if voice_type == "all":
            return voices
        elif voice_type == "system":
            return [v for v in voices if v.get("type") == "system"]
        elif voice_type == "cloned":
            return [v for v in voices if v.get("type") == "cloned"]
        elif voice_type == "designed":
            return [v for v in voices if v.get("type") == "designed"]
        else:
            return voices

    except requests.exceptions.RequestException:
        # 如果 API 调用失败，返回默认声音列表
        return get_default_system_voices() if voice_type in ["all", "system"] else []


def get_default_system_voices() -> List[Dict[str, Any]]:
    """返回默认的系统声音列表"""
    return [
        {"voice_id": "female-shaonv", "name": "少女音", "type": "system", "language": "zh"},
        {"voice_id": "female-yujie", "name": "御姐音", "type": "system", "language": "zh"},
        {"voice_id": "female-chengshu", "name": "成熟女声", "type": "system", "language": "zh"},
        {"voice_id": "female-tianmei", "name": "甜美音", "type": "system", "language": "zh"},
        {"voice_id": "male-qingnian", "name": "青年男声", "type": "system", "language": "zh"},
        {"voice_id": "male-chengshu", "name": "成熟男声", "type": "system", "language": "zh"},
        {"voice_id": "presenter_male", "name": "男性主持", "type": "system", "language": "zh"},
        {"voice_id": "presenter_female", "name": "女性主持", "type": "system", "language": "zh"},
        {"voice_id": "audiobook_male_1", "name": "有声书男声1", "type": "system", "language": "zh"},
        {"voice_id": "audiobook_female_1", "name": "有声书女声1", "type": "system", "language": "zh"},
    ]


# ============================================================
# 声音克隆
# ============================================================

def voice_clone(
    voice_id: str,
    audio_file: str,
    voice_name: str = None,
    voice_description: str = None,
    demo_text: str = None
) -> Dict[str, Any]:
    """
    克隆声音

    Args:
        voice_id: 自定义声音 ID（唯一标识）
        audio_file: 音频文件路径
        voice_name: 声音名称
        voice_description: 声音描述
        demo_text: 试听文本

    Returns:
        dict: 包含 success, voice_id, status 等信息
    """
    config = get_config()

    audio_path = os.path.expanduser(audio_file)
    if not os.path.exists(audio_path):
        return {
            "success": False,
            "error": f"音频文件不存在: {audio_path}"
        }

    url = f"{config['api_host']}/v1/voice/clone"

    headers = {
        "Authorization": f"Bearer {config['api_key']}"
    }

    # 准备文件和表单数据
    with open(audio_path, "rb") as f:
        files = {
            "file": (os.path.basename(audio_path), f, "audio/mpeg")
        }

        data = {
            "voice_id": voice_id
        }

        if voice_name:
            data["voice_name"] = voice_name
        if voice_description:
            data["voice_description"] = voice_description
        if demo_text:
            data["demo_text"] = demo_text

        try:
            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=data,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()

            if result.get("base_resp", {}).get("status_code") == 0:
                return {
                    "success": True,
                    "voice_id": voice_id,
                    "voice_name": voice_name,
                    "status": "ready",
                    "created_at": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": result.get("base_resp", {}).get("status_msg", "克隆失败"),
                    "error_code": result.get("base_resp", {}).get("status_code")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }


# ============================================================
# 声音设计
# ============================================================

def voice_design(
    prompt: str,
    preview_text: str,
    voice_id: str = None,
    voice_name: str = None
) -> Dict[str, Any]:
    """
    根据描述设计声音

    Args:
        prompt: 声音描述
        preview_text: 试听预览文本
        voice_id: 保存时的声音 ID（可选）
        voice_name: 声音名称（可选）

    Returns:
        dict: 包含 success, preview_audio, voice_id 等信息
    """
    config = get_config()

    url = f"{config['api_host']}/v1/voice/design"

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "preview_text": preview_text
    }

    if voice_id:
        payload["voice_id"] = voice_id
    if voice_name:
        payload["voice_name"] = voice_name

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            # 保存预览音频
            preview_audio = None
            if "audio" in result["data"]:
                ensure_output_dir()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                preview_path = os.path.join(
                    config["output_dir"],
                    f"voice_design_preview_{timestamp}.mp3"
                )

                audio_data = bytes.fromhex(result["data"]["audio"])
                with open(preview_path, "wb") as f:
                    f.write(audio_data)
                preview_audio = preview_path

            return {
                "success": True,
                "voice_id": voice_id,
                "preview_audio": preview_audio,
                "voice_features": result.get("data", {}).get("voice_features", {})
            }
        else:
            return {
                "success": False,
                "error": result.get("base_resp", {}).get("status_msg", "设计失败"),
                "suggestion": "请提供更详细的声音特征描述"
            }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# 播放音频
# ============================================================

def play_audio(file_path: str) -> Dict[str, Any]:
    """
    播放音频文件

    Args:
        file_path: 音频文件路径

    Returns:
        dict: 包含 success 和可能的 error 信息
    """
    file_path = os.path.expanduser(file_path)

    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"文件不存在: {file_path}"
        }

    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            subprocess.run(["afplay", file_path], check=True)
        elif system == "Windows":
            os.startfile(file_path)
        else:  # Linux
            # 尝试多种播放器
            players = ["aplay", "paplay", "mpv", "ffplay"]
            for player in players:
                try:
                    subprocess.run([player, file_path], check=True)
                    break
                except FileNotFoundError:
                    continue
            else:
                return {
                    "success": False,
                    "error": "未找到可用的音频播放器，请安装 aplay, paplay, mpv 或 ffplay"
                }

        return {"success": True, "file_path": file_path}

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"播放失败: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# 便捷函数
# ============================================================

def quick_tts(text: str, voice: str = "female-shaonv") -> str:
    """
    快速 TTS，返回生成的文件路径

    Args:
        text: 要转换的文本
        voice: 声音 ID

    Returns:
        str: 生成的音频文件路径
    """
    result = text_to_audio(text=text, voice_id=voice)
    if result["success"]:
        return result["file_path"]
    else:
        raise Exception(result.get("error", "TTS 失败"))


def speak(text: str, voice: str = "female-shaonv") -> None:
    """
    直接朗读文本（生成并播放）

    Args:
        text: 要朗读的文本
        voice: 声音 ID
    """
    file_path = quick_tts(text, voice)
    play_audio(file_path)


# ============================================================
# 主函数（用于测试）
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("MiniMax TTS 模块")
        print("\n可用函数:")
        print("  - text_to_audio(text, voice_id, output_path, ...)")
        print("  - list_voices(voice_type)")
        print("  - voice_clone(voice_id, audio_file, ...)")
        print("  - voice_design(prompt, preview_text, ...)")
        print("  - play_audio(file_path)")
        print("  - quick_tts(text, voice)")
        print("  - speak(text, voice)")
        print("\n测试: python minimax_tts.py test")
        sys.exit(0)

    if sys.argv[1] == "test":
        print("测试 MiniMax TTS...")

        # 测试获取配置
        try:
            config = get_config()
            print(f"✓ API Key 已配置")
            print(f"✓ API Host: {config['api_host']}")
        except ValueError as e:
            print(f"✗ 配置错误: {e}")
            sys.exit(1)

        # 测试列出声音
        print("\n测试列出声音...")
        voices = list_voices(voice_type="system")
        print(f"✓ 获取到 {len(voices)} 个系统声音")
        for v in voices[:3]:
            print(f"  - {v['voice_id']}: {v['name']}")

        print("\n测试完成!")
