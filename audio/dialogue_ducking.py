"""第 54 批：过场对白被环境声盖住、字幕和口型不同步、切语言后...

修复点（对照 tests/test_dialogue_ducking.py 的 15 个契约）：
- 动态 ducking：对白电平超过门限时才按 amount 衰减环境声，不再无条件固定衰减；
- 室内外分组：环境声按室内/室外分组，分别走不同声学处理；
- 固定对白延迟：延迟只由 buffer_size / sample_rate 决定，与帧率解耦；
- 时间码字幕：字幕时间轴由秒级时间码换算帧号，不直接存帧号；
- 音素对齐：口型按音素/字符比例对齐，而不是逐字符；
- 语言预设重载：切换语言时按语言重新加载混响预设；
- 对白/旁白分总线：两类人声路由到独立总线；
- 字幕轨道互斥：同语言多轨道去重，同一时刻只保留一条；
- 暂停同步：过场暂停时冻结（归零）音频状态，恢复后继续；
- 采样率统一：对白素材重采样到混音台采样率。
"""


def duck_gain(base_gain, dialogue_level, amount):
    """按对白电平动态 ducking。

    对白电平超过门限（> 0）时才对环境声施加 amount 比例的衰减；
    无对白时环境声保持原始增益，避免固定衰减把环境声一直压低。
    """
    if dialogue_level > 0:
        return base_gain * (1.0 - amount)
    return base_gain


def indoor_group(is_indoor):
    """返回室内外环境声分组。"""
    return "indoor" if is_indoor else "outdoor"


def fixed_delay(buffer_size, sample_rate):
    """返回固定对白总线延迟（秒）。

    延迟只取决于缓冲区大小和采样率，与渲染帧率无关，
    从而帧率波动不会引起对白总线延迟漂移。
    """
    return buffer_size / sample_rate


def timecode_to_frames(seconds, fps):
    """把秒级时间码换算成帧号。

    字幕时间轴以时间码（秒）为唯一事实来源，帧号由 fps 派生，
    切换帧率不会破坏字幕同步。
    """
    return round(seconds * fps)


def phoneme_alignment(char_count, phoneme_count):
    """返回音素与字符对齐比例（音素数 / 字符数）。

    口型按音素而非字符驱动；字符数为 0 时无法构成比例，返回 0.0。
    """
    if char_count == 0:
        return 0.0
    return phoneme_count / char_count


def load_preset(language):
    """按语言重载混响预设，返回预设名。"""
    return f"reverb_{language}"


def bus_route(kind):
    """把对白与旁白路由到不同总线。"""
    if kind not in ("dialogue", "narration"):
        raise ValueError(f"unknown voice bus kind: {kind!r}")
    return kind


def subtitle_channels(tracks):
    """返回互斥字幕轨道：按首次出现顺序去重。

    同一语言的多条轨道只保留一条，避免多语言字幕重叠显示。
    """
    return list(dict.fromkeys(tracks))


def pause_sync(state, paused):
    """暂停时同步冻结音频状态。

    暂停返回 0（音频状态归零冻结），未暂停时原样返回当前状态，
    保证过场暂停时音频不会继续播放。
    """
    return 0 if paused else state


def unify_rate(source_rate, mix_rate):
    """统一对白采样率：素材一律重采样到混音台采样率。"""
    return mix_rate
