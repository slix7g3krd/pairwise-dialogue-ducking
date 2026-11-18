# pairwise-dialogue-ducking

过场对白被环境声盖住、字幕和口型不同步、切语言后混响不对：对白 ducking 按固定衰减；环境声不区分室内外；对白总线延迟随帧率；字幕时间轴按帧号；口型音素按字符；语言切换没重载混响预设；对白和旁白共用总线；多语言字幕重叠；过场暂停时音频继续；对白采样率和混音台不一致。audio/dialogue_ducking.py 是核心，tests/test_dialogue_ducking.py 15个红。要修的是：动态 ducking；室内外分组；固定对白延迟；时间码字幕；音素对齐；语言预设重载；对白旁白分总线；字幕轨道互斥；暂停同步；采样率统一。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：音视频处理；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
