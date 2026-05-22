# Banner 图片生成指南

> ⚠️ 自动生图失败（Google API网络不可达，MiniMax API Key无图片权限）
> 请使用下方 prompts 手动生成后替换对应文件。

## 需要替换的文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `banner-1.jpg` | ✅ 保留 | 激光器产品全家福，可用 |
| `banner-2.jpg` | ❌ 替换 | ~~展会现场，杂乱~~ |
| `banner-3.jpg` | ❌ 替换 | ~~PPT翻拍，画质差~~ |

## Banner规格

- 尺寸：**1200×600px**（或接近的16:9比例）
- 格式：JPG
- 风格：科技感、深色背景
- 禁止：品牌Logo、人物面部

---

## 🅰️ Banner-2：激光焊接火花特写（高速摄影风格）

**文件名：** `banner-2.jpg`

**Prompt（Midjourney / DALL-E 3 通用）：**

```
Close-up high-speed photography of laser welding on metal, brilliant 
orange-gold sparks spraying dynamically against dark industrial background, 
light trails and patterns from molten metal, deep navy blue-black background 
with warm golden-orange welding glow, cinematic macro photography, sharp 
detail on metal surface texture, dramatic lighting contrast, no people, 
no logos, no text --ar 16:9 --style raw --v 6
```

**关键词：** 高速摄影、激光焊接火花、橙色金色火花轨迹、深色背景

---

## 🅱️ Banner-3：抽象科技风（激光光束 + UI参数界面）

**文件名：** `banner-3.jpg`

**Prompt（Midjourney / DALL-E 3 通用）：**

```
Abstract technology banner for laser welding parameter tool, deep navy 
blue background, glowing cyan and orange laser beams cutting diagonally, 
holographic translucent UI panels floating in background, parameter 
data readouts, waveform graphs, tech grid lines on dark surface, fusion 
of warm laser orange and cool tech blue colors, sleek modern premium 
tech aesthetic, volumetric lighting, no people, no logos, no visible 
text --ar 16:9 --style raw --v 6
```

**关键词：** 抽象科技、激光光束、UI界面元素、全息参数面板

---

## 替换步骤

1. 用任意图像生成工具（Midjourney/DALL-E 3/Stable Diffusion）根据prompt生成图片
2. 调整尺寸为 **1200×600px**
3. 保存覆盖对应文件：
   - `banner-2.jpg`
   - `banner-3.jpg`
4. 刷新浏览器（`Cmd+Shift+R` 强制刷新）即可生效
