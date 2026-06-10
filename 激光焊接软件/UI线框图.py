"""
激光焊接工艺参数查询系统 — UI线框图生成
用于设计评审沟通，生成后可打印/分享/标注修改意见
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = "/Users/luxiangzhi/.openclaw/workspace/projects/激光焊接软件/UI线框图"

# 颜色
C_PRIMARY = "#2F5496"
C_PRIMARY_DARK = "#1a3a6b"
C_PRIMARY_LIGHT = "#e8f0fe"
C_GOLD = "#f0ad4e"
C_GREEN = "#28a745"
C_BLUE = "#007bff"
C_ORANGE = "#fd7e14"
C_BG = "#f5f6fa"
C_WHITE = "#ffffff"
C_TEXT = "#333333"
C_TEXT_SEC = "#666666"
C_TEXT_LIGHT = "#999999"
C_BORDER = "#e0e0e0"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    """画圆角矩形（自动缩小半径避免越界）"""
    x1, y1, x2, y2 = xy
    h = y2 - y1
    w = x2 - x1
    r = min(r, h//2, w//2)
    if r <= 0:
        draw.rectangle([x1, y1, x2, y2], fill=fill)
        return
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.pieslice([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=fill)
    draw.pieslice([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=width)

def draw_progress_bar(draw, x, y, w, h, pct, color):
    """画进度条"""
    fill_color = hex_to_rgb(color)
    draw.rounded_rectangle([x, y, x+w, y+h], radius=3, fill="#e0e0e0")
    if pct > 0:
        draw.rounded_rectangle([x, y, x+w*pct/100, y+h], radius=3, fill=fill_color)

def make_mobile_search():
    """图1: 移动端搜索界面"""
    W, H = 390, 844
    img = Image.new("RGB", (W, H), hex_to_rgb(C_BG))
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
        font_input = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_btn = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_tag = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
        font_label = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 10)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_input = font_title
        font_btn = font_title
        font_tag = font_title
        font_label = font_title

    # 头部
    draw.rectangle([0, 0, W, 56], fill=hex_to_rgb(C_PRIMARY))
    draw.rectangle([0, 56, W, 56+40], fill=hex_to_rgb(C_PRIMARY_DARK))
    # 渐变效果 - 模拟
    for i in range(56):
        r = int(47 + (26-47)*i/56)
        g = int(84 + (58-84)*i/56)
        b = int(150 + (107-150)*i/56)
        draw.line([0, i, W, i], fill=(r, g, b))
    
    draw.text((16, 18), "🔧  激光焊接工艺参数库", fill="white", font=font_title)
    draw.text((16, 40), "输入材料 → 查询最佳参数", fill=(200, 210, 230), font=font_sub)

    # 搜索面板
    sx, sy = 16, 72
    pw = W - 32
    rounded_rect(draw, [sx, sy, sx+pw, sy+200], 12, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)

    # 材料输入框
    inp_y = sy + 16
    rounded_rect(draw, [sx+12, inp_y, sx+pw-12, inp_y+44], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((sx+24, inp_y+13), "🔍  搜索材料名称，如 不锈钢304", fill=C_TEXT_LIGHT, font=font_input)

    # 接头类型下拉
    jt_y = inp_y + 52
    rounded_rect(draw, [sx+12, jt_y, sx+pw-12, jt_y+44], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((sx+24, jt_y+13), "接头类型：全部  ▼", fill=C_TEXT, font=font_input)

    # 厚度范围
    th_y = jt_y + 52
    half_w = (pw - 36) // 2
    rounded_rect(draw, [sx+12, th_y, sx+12+half_w, th_y+44], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((sx+24, th_y+13), "厚度从 (mm)", fill=C_TEXT_LIGHT, font=font_input)
    rounded_rect(draw, [sx+pw-12-half_w, th_y, sx+pw-12, th_y+44], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((sx+pw-12-half_w+12, th_y+13), "到 (mm)", fill=C_TEXT_LIGHT, font=font_input)

    # 按钮
    btn_y = th_y + 56
    btn_w1 = int((pw-36)*0.7)
    btn_w2 = pw-36-btn_w1
    rounded_rect(draw, [sx+12, btn_y, sx+12+btn_w1, btn_y+44], 8, hex_to_rgb(C_PRIMARY))
    draw.text((sx+12+btn_w1//2-40, btn_y+12), "🔍  查询参数", fill="white", font=font_btn)
    rounded_rect(draw, [sx+12+btn_w1+12, btn_y, sx+pw-12, btn_y+44], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((sx+12+btn_w1+12+btn_w2//2-24, btn_y+12), "清 除", fill=C_TEXT_SEC, font=font_btn)

    # 热门材料标签（新增功能窗口）
    tag_y = sy + 220
    draw.text((sx+12, tag_y), "🔥 热门材料（点击快速搜索）：", fill=C_TEXT, font=font_sub)
    tags = ["不锈钢304", "碳钢Q235", "铝合金6061", "紫铜T2", "钛合金TC4"]
    tag_x = sx+12
    tag_y2 = tag_y + 22
    for t in tags:
        tw = len(t) * 14 + 20
        rounded_rect(draw, [tag_x, tag_y2, tag_x+tw, tag_y2+30], 15, hex_to_rgb(C_PRIMARY_LIGHT), hex_to_rgb(C_PRIMARY), 1)
        draw.text((tag_x+10, tag_y2+7), t, fill=C_PRIMARY, font=font_tag)
        tag_x += tw + 8

    # 底部提示
    draw.text((16, 760), "⏱ 共 30 条工艺参数 · 数据持续更新中", fill=C_TEXT_LIGHT, font=font_label)

    # 标注
    draw.rectangle([0, H-60, W, H], fill="#1a1a2e")
    draw.text((16, H-52), "📱 移动端 · 搜索界面 V1.1", fill="#aabbcc", font=font_sub)
    draw.text((W-180, H-52), "激光焊接工艺参数查询系统", fill="#667788", font=font_label)

    path = os.path.join(OUT_DIR, "01-移动端-搜索界面.png")
    img.save(path)
    print(f"✅ {path}")
    return path

def make_mobile_results():
    """图2: 移动端结果展示"""
    W, H = 390, 1000
    img = Image.new("RGB", (W, H), hex_to_rgb(C_BG))
    draw = ImageDraw.Draw(img)
    try:
        font_card_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 15)
        font_badge = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 11)
        font_core = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
        font_unit = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
        font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
        font_note = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 11)
        font_tag = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 13)
        font_label = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 10)
    except:
        f = ImageFont.load_default()
        font_card_title = f; font_badge = f; font_core = f; font_unit = f
        font_sub = f; font_note = f; font_tag = f; font_label = f

    # 头部
    draw.rectangle([0, 0, W, 44], fill=hex_to_rgb(C_PRIMARY))
    draw.text((16, 12), "🔧  激光焊接工艺参数库", fill="white", font=font_tag)

    # 统计条
    draw.text((16, 56), "⏱ 共找到 8 条工艺参数", fill=C_TEXT_SEC, font=font_sub)

    # 卡片数据
    cards = [
        ("不锈钢304", "不锈钢304", "对接焊", 2000, 1.2, 1.5, "+2", "氩气(Ar)", 15, "气动夹具", "Ⅰ级", "", False),
        ("不锈钢304", "不锈钢316L", "搭接焊", 2500, 1.0, 2.0, "+1", "氩气(Ar)", 18, "气动夹具", "Ⅱ级", "异种钢焊接，偏向不锈钢侧调节", False),
        ("紫铜T2", "紫铜T2", "对接焊", 3500, 0.5, 1.0, "+4", "氦气(He)", 25, "铜制夹具", "Ⅱ级", "高反材料，建议绿光/蓝光激光器", True),
    ]

    cy = 80
    for mat1, mat2, jt, power, speed, thick, defocus, gas, flow, fix, quality, note, premium in cards:
        card_w = W - 32
        card_h = 180
        ch = card_h if not note else card_h + 30

        # 卡片背景
        border_color = C_GOLD if premium else C_GREEN if quality == "Ⅰ级" else C_BLUE if quality == "Ⅱ级" else C_ORANGE
        rounded_rect(draw, [16, cy, 16+card_w, cy+ch], 10, hex_to_rgb(C_WHITE))
        # 左边色块
        draw.rectangle([16, cy, 20, cy+ch], fill=hex_to_rgb(border_color))
        draw.rounded_rectangle([16, cy, 20, cy+ch], radius=3, fill=hex_to_rgb(border_color))

        # 材料标题
        title = f"{mat1} ⟷ {mat2}"
        draw.text((32, cy+10), title, fill=C_PRIMARY, font=font_card_title)

        # 质量等级徽标
        badge_colors = {"Ⅰ级": C_GREEN, "Ⅱ级": C_BLUE, "Ⅲ级": C_ORANGE}
        bc = badge_colors.get(quality, C_TEXT_LIGHT)
        bx = 32 + len(title) * 8 + 12
        rounded_rect(draw, [bx, cy+10, bx+44, cy+28], 10, fill=hex_to_rgb(bc))
        draw.text((bx+6, cy+12), quality, fill="white", font=font_badge)

        # Premium标志
        if premium:
            px = bx + 52
            rounded_rect(draw, [px, cy+10, px+42, cy+28], 10, fill=hex_to_rgb(C_GOLD))
            draw.text((px+6, cy+12), "PREMIUM", fill="white", font=font_badge)

        # 接头类型
        draw.text((bx + (60 if premium else 52), cy+12), jt, fill=C_TEXT_SEC, font=font_badge)

        # 分割线
        draw.line([32, cy+38, W-16, cy+38], fill=C_BORDER, width=1)

        # 核心参数 — 大字突出
        draw.text((32, cy+48), "⚡", fill=C_GOLD, font=font_core)
        draw.text((56, cy+48), f"{power}  W", fill=C_TEXT, font=font_core)
        draw.text((56, cy+48+22), "激光功率", fill=C_TEXT_LIGHT, font=font_unit)

        draw.text((200, cy+48), "⚡", fill=C_GOLD, font=font_core)
        draw.text((224, cy+48), f"{speed}  m/min", fill=C_TEXT, font=font_core)
        draw.text((224, cy+48+22), "焊接速度", fill=C_TEXT_LIGHT, font=font_unit)

        draw.text((32, cy+100), f"📏 板厚: {thick} mm    离焦量: {defocus} mm", fill=C_TEXT_SEC, font=font_sub)

        # 折叠区指示
        draw.line([32, cy+128, W-32, cy+128], fill="#eee", width=1)
        draw.text((32, cy+132), "▼  更多参数  保护气 · 气流量 · 工装要求", fill=C_PRIMARY, font=font_sub)
        draw.text((W-100, cy+132), "点击展开", fill=C_TEXT_LIGHT, font=font_unit)

        # 备注
        if note:
            draw.line([32, cy+158, W-32, cy+158], fill=C_BORDER, width=1)
            draw.text((32, cy+164), f"💡 {note}", fill=C_TEXT_SEC, font=font_note)

        cy += ch + 10

    # 分页
    draw.text((W//2-70, cy+5), "← 第 1/3 页 · 每页 20 条  →", fill=C_PRIMARY, font=font_tag)

    # 标注
    draw.rectangle([0, H-60, W, H], fill="#1a1a2e")
    draw.text((16, H-52), "📱 移动端 · 结果展示 V1.1", fill="#aabbcc", font=font_sub)
    draw.text((W-180, H-52), "核心参数大字突出 · 辅助参数折叠", fill="#667788", font=font_label)

    path = os.path.join(OUT_DIR, "02-移动端-结果展示.png")
    img.save(path)
    print(f"✅ {path}")
    return path

def make_desktop_grid():
    """图3: 桌面端网格布局"""
    W, H = 1200, 900
    img = Image.new("RGB", (W, H), hex_to_rgb(C_BG))
    draw = ImageDraw.Draw(img)
    try:
        font_h1 = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
        font_h2 = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_input = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_btn = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_card_t = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 15)
        font_core = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        font_unit = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 11)
        font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 12)
        font_badge = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 10)
        font_label = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 10)
    except:
        f = ImageFont.load_default()
        font_h1 = f; font_h2 = f; font_input = f; font_btn = f
        font_card_t = f; font_core = f; font_unit = f; font_sub = f
        font_badge = f; font_label = f

    # 头部
    draw.rectangle([0, 0, W, 64], fill=hex_to_rgb(C_PRIMARY))
    draw.text((40, 14), "🔧  激光焊接工艺参数库", fill="white", font=font_h1)
    draw.text((40, 42), "输入材料 → 查询最佳焊接参数", fill=(180,200,220), font=font_h2)

    # 搜索面板 — 横向布局
    px, py = 40, 84
    pw = W - 80
    rounded_rect(draw, [px, py, px+pw, py+70], 12, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)

    # 一行排列
    inp_x = px+16
    # 材料
    rounded_rect(draw, [inp_x, py+14, inp_x+240, py+56], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((inp_x+12, py+26), "🔍  搜索材料名称（如 不锈钢304）", fill=C_TEXT_LIGHT, font=font_input)
    # 接头
    jx = inp_x + 256
    rounded_rect(draw, [jx, py+14, jx+160, py+56], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((jx+12, py+26), "全部接头 ▼", fill=C_TEXT, font=font_input)
    # 厚度
    tx = jx + 176
    rounded_rect(draw, [tx, py+14, tx+80, py+56], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((tx+12, py+26), "从", fill=C_TEXT_LIGHT, font=font_input)
    tx += 96
    rounded_rect(draw, [tx, py+14, tx+80, py+56], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((tx+12, py+26), "到", fill=C_TEXT_LIGHT, font=font_input)
    # 按钮
    bx = tx + 100
    rounded_rect(draw, [bx, py+14, bx+120, py+56], 8, hex_to_rgb(C_PRIMARY))
    draw.text((bx+24, py+26), "🔍  查询", fill="white", font=font_btn)
    bx += 136
    rounded_rect(draw, [bx, py+14, bx+80, py+56], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((bx+20, py+26), "清除", fill=C_TEXT_SEC, font=font_btn)

    # 统计条
    draw.text((40, 170), "⏱ 共 30 条工艺参数  |  🔥 热门：不锈钢304  碳钢Q235  铝合金6061  紫铜T2", fill=C_TEXT_SEC, font=font_sub)

    # 桌面端网格 — 3列
    grid_data = [
        ("不锈钢304", "不锈钢304", 2000, 1.2, 1.5, "+2", "Ⅰ级", "氩气(Ar)", "15L/min", "气动夹具", "", False),
        ("不锈钢304", "不锈钢316L", 2500, 1.0, 2.0, "+1", "Ⅱ级", "氩气(Ar)", "18L/min", "气动夹具", "异种钢焊接", False),
        ("紫铜T2", "紫铜T2", 3500, 0.5, 1.0, "+4", "Ⅱ级", "氦气(He)", "25L/min", "铜制夹具", "高反材料", True),
        ("碳钢Q235", "碳钢Q235", 1500, 1.5, 1.0, "+1", "Ⅰ级", "氩气(Ar)", "10L/min", "气动夹具", "", False),
        ("铝合金6061", "铝合金6061", 3000, 0.6, 2.0, "+3", "Ⅱ级", "氩气(Ar)", "20L/min", "专用夹具", "需清理氧化层", False),
        ("钛合金TC4", "钛合金TC4", 2500, 0.6, 2.0, "+2", "Ⅰ级", "氩气(Ar)", "25L/min", "专用夹具", "全氩气保护", False),
    ]

    cols = 3
    gap = 16
    card_w = (W - 80 - (cols-1)*gap) // cols
    card_h = 220

    for i, (mat1, mat2, power, speed, thick, defocus, quality, gas, flow, fix, note, premium) in enumerate(grid_data):
        col = i % cols
        row = i // cols
        cx = 40 + col * (card_w + gap)
        cy = 190 + row * (card_h + gap)

        border_color = C_GOLD if premium else C_GREEN if quality == "Ⅰ级" else C_BLUE if quality == "Ⅱ级" else C_ORANGE
        rounded_rect(draw, [cx, cy, cx+card_w, cy+card_h], 10, hex_to_rgb(C_WHITE))

        # 顶部色条
        draw.rounded_rectangle([cx, cy, cx+card_w, cy+4], radius=2, fill=hex_to_rgb(border_color))

        # 标题
        title = f"{mat1} ⟷ {mat2}"
        draw.text((cx+12, cy+12), title, fill=C_PRIMARY, font=font_card_t)

        # 质量等级
        bc = {"Ⅰ级": C_GREEN, "Ⅱ级": C_BLUE, "Ⅲ级": C_ORANGE}.get(quality, C_TEXT_LIGHT)
        rounded_rect(draw, [cx+12, cy+36, cx+48, cy+50], 8, fill=hex_to_rgb(bc))
        draw.text((cx+16, cy+38), quality, fill="white", font=font_badge)

        # Premium
        if premium:
            rounded_rect(draw, [cx+56, cy+36, cx+92, cy+50], 8, fill=hex_to_rgb(C_GOLD))
            draw.text((cx+60, cy+38), "PREMIUM", fill="white", font=font_badge)

        # 核心参数
        draw.text((cx+12, cy+60), f"⚡ 功率: {power} W", fill=C_TEXT, font=font_core)
        draw.text((cx+12, cy+84), f"⚡ 速度: {speed} m/min", fill=C_TEXT, font=font_core)
        draw.text((cx+12, cy+108), f"📏 板厚: {thick} mm  |  离焦: {defocus} mm", fill=C_TEXT_SEC, font=font_sub)

        # 分割线
        draw.line([cx+12, cy+130, cx+card_w-12, cy+130], fill=C_BORDER, width=1)

        # 辅助参数（桌面端默认展开）
        draw.text((cx+12, cy+138), f"保护气: {gas}", fill=C_TEXT_SEC, font=font_sub)
        draw.text((cx+12, cy+156), f"气流量: {flow}  |  工装: {fix}", fill=C_TEXT_SEC, font=font_sub)
        if note:
            draw.text((cx+12, cy+178), f"💡 {note}", fill=C_TEXT_SEC, font=font_badge)

        # 排序名称
        draw.text((cx+card_w-80, cy+12), f"#{i+1}", fill=C_TEXT_LIGHT, font=font_badge)

    # 分页
    draw.text((W//2-80, 190 + 3*(card_h+16) + 10), "← 第 1/2 页  ·  共 30 条  →", fill=C_PRIMARY, font=font_sub)

    # 标注
    draw.rectangle([0, H-60, W, H], fill="#1a1a2e")
    draw.text((40, H-50), "🖥️ 桌面端 · 网格布局（3~4列）V1.1", fill="#aabbcc", font=font_h2)
    draw.text((800, H-50), "辅助参数默认展开 · 宽屏充分利用", fill="#667788", font=font_label)

    path = os.path.join(OUT_DIR, "03-桌面端-网格布局.png")
    img.save(path)
    print(f"✅ {path}")
    return path

def make_detail_window():
    """图4: 参数详情窗口（新增功能窗口）"""
    W, H = 500, 700
    img = Image.new("RGB", (W, H), hex_to_rgb(C_BG))
    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        font_h = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_m = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 13)
        font_s = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 11)
        font_l = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 10)
    except:
        f = ImageFont.load_default()
        font_t = f; font_h = f; font_m = f; font_s = f; font_l = f

    # 模拟模态窗口背景
    draw.rectangle([0, 0, W, H], fill=(0,0,0,100))

    # 窗口主体
    wx, wy, ww, wh = 30, 40, 440, 620
    rounded_rect(draw, [wx, wy, wx+ww, wy+wh], 16, hex_to_rgb(C_WHITE))

    # 标题栏
    draw.rectangle([wx, wy, wx+ww, wy+50], fill=hex_to_rgb(C_PRIMARY))
    draw.text((wx+16, wy+14), "📋  焊接参数详情", fill="white", font=font_h)
    draw.text((wx+ww-40, wy+14), "✕", fill="white", font=font_h)

    # 材料信息
    ly = wy + 62
    draw.text((wx+16, ly), "材料组合", fill=C_TEXT_LIGHT, font=font_s)
    draw.text((wx+16, ly+18), "不锈钢304  ⟷  不锈钢304", fill=C_PRIMARY, font=font_t)

    # 质量等级
    rounded_rect(draw, [wx+ww-100, ly+18, wx+ww-16, ly+42], 8, fill=hex_to_rgb(C_GREEN))
    draw.text((wx+ww-90, ly+22), "Ⅰ级  ✅", fill="white", font=font_m)

    # 参数表格
    py2 = ly + 56
    param_items = [
        ("接头类型", "对接焊"),
        ("板厚", "1.5 mm"),
        ("激光功率", "2000 W"),
        ("焊接速度", "1.2 m/min"),
        ("离焦量", "+2 mm"),
        ("保护气体", "氩气(Ar)"),
        ("气体流量", "15 L/min"),
        ("工装要求", "气动夹具"),
    ]

    # 表头
    draw.rectangle([wx+16, py2, wx+ww-16, py2+30], fill=hex_to_rgb(C_PRIMARY_LIGHT))
    draw.text((wx+30, py2+6), "参数名称", fill=C_PRIMARY, font=font_m)
    draw.text((wx+ww-100, py2+6), "参数值", fill=C_PRIMARY, font=font_m)

    for idx, (name, val) in enumerate(param_items):
        iy = py2 + 34 + idx * 34
        bg = hex_to_rgb(C_WHITE) if idx % 2 == 0 else hex_to_rgb("#fafbfc")
        draw.rectangle([wx+16, iy, wx+ww-16, iy+30], fill=bg)
        draw.text((wx+30, iy+6), name, fill=C_TEXT, font=font_m)
        draw.text((wx+ww-100, iy+6), val, fill=C_TEXT_SEC, font=font_m)

    # 备注
    ny = py2 + 34 + len(param_items) * 34 + 10
    draw.line([wx+16, ny, wx+ww-16, ny], fill=C_BORDER, width=1)
    draw.text((wx+16, ny+10), "💡 备注说明", fill=C_TEXT, font=font_h)
    draw.text((wx+16, ny+32), "标准焊接参数，适用于常规不锈钢薄板对接焊。", fill=C_TEXT_SEC, font=font_m)
    draw.text((wx+16, ny+50), "建议焊接前清理工件表面油污和氧化层。", fill=C_TEXT_SEC, font=font_m)

    # 操作按钮
    by = ny + 90
    rounded_rect(draw, [wx+16, by, wx+ww-16, by+44], 8, hex_to_rgb(C_PRIMARY))
    draw.text((wx+ww//2-60, by+12), "📋  复制参数到剪贴板", fill="white", font=font_m)
    by += 54
    rounded_rect(draw, [wx+16, by, wx+ww//2-8, by+36], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((wx+ww//4-32, by+9), "收藏 ⭐", fill=C_TEXT_SEC, font=font_m)
    rounded_rect(draw, [wx+ww//2+8, by, wx+ww-16, by+36], 8, hex_to_rgb(C_WHITE), hex_to_rgb(C_BORDER), 1)
    draw.text((wx+ww*3//4-32, by+9), "对比 📊", fill=C_TEXT_SEC, font=font_m)

    # 标注
    draw.rectangle([0, H-50, W, H], fill="#1a1a2e")
    draw.text((40, H-42), "🆕 新增功能：参数详情窗口", fill="#aabbcc", font=font_h)
    draw.text((300, H-42), "支持查看详情 · 复制 · 收藏 · 对比", fill="#667788", font=font_l)

    path = os.path.join(OUT_DIR, "04-新增-参数详情窗口.png")
    img.save(path)
    print(f"✅ {path}")
    return path

def make_compare_window():
    """图5: 参数对比窗口（新增功能）"""
    W, H = 700, 650
    img = Image.new("RGB", (W, H), hex_to_rgb(C_BG))
    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        font_h = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
        font_m = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 13)
        font_s = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 11)
    except:
        f = ImageFont.load_default()
        font_t = f; font_h = f; font_m = f; font_s = f

    # 窗口
    wx, wy, ww, wh = 20, 20, 660, 610
    rounded_rect(draw, [wx, wy, wx+ww, wy+wh], 16, hex_to_rgb(C_WHITE))

    # 标题
    draw.text((wx+20, wy+16), "📊  参数对比 — 不锈钢304 对接焊", fill=C_PRIMARY, font=font_t)
    draw.text((wx+500, wy+16), "✕", fill=C_TEXT_LIGHT, font=font_t)

    # 表头行
    hy = wy + 56
    cols_w = [160, 160, 160, 160]
    col_x = [wx+20, wx+20+cols_w[0]+10, wx+20+(cols_w[0]+10)*2, wx+20+(cols_w[0]+10)*3]
    headers = ["参数项", "0.5mm 板厚", "1.0mm 板厚", "1.5mm 板厚"]

    # 表头背景
    for i, (h, cx, cw) in enumerate(zip(headers, col_x, cols_w)):
        draw.rectangle([cx, hy, cx+cw, hy+36], fill=hex_to_rgb(C_PRIMARY_LIGHT))
        draw.text((cx+8, hy+10), h, fill=C_PRIMARY, font=font_h)

    # 表格数据
    table_data = [
        ("材料", "不锈钢304", "不锈钢304", "不锈钢304"),
        ("接头", "对接焊", "对接焊", "对接焊"),
        ("功率", "1500 W", "1800 W", "2000 W"),
        ("速度", "1.5 m/min", "1.3 m/min", "1.2 m/min"),
        ("离焦量", "+1 mm", "+1 mm", "+2 mm"),
        ("保护气", "Ar", "Ar", "Ar"),
        ("气流量", "12 L/min", "15 L/min", "15 L/min"),
        ("工装", "气动夹具", "气动夹具", "气动夹具"),
        ("质量等级", "Ⅰ级", "Ⅰ级", "Ⅰ级"),
    ]

    for idx, (p, v1, v2, v3) in enumerate(table_data):
        ry = hy + 40 + idx * 32
        bg = hex_to_rgb(C_WHITE) if idx % 2 == 0 else hex_to_rgb("#fafbfc")
        draw.rectangle([wx+20, ry, wx+ww-20, ry+28], fill=bg)
        f = font_m if idx < 2 else font_s
        draw.text((col_x[0]+8, ry+6), p, fill=C_TEXT, font=f)
        draw.text((col_x[1]+8, ry+6), v1, fill=C_TEXT_SEC, font=font_m)
        draw.text((col_x[2]+8, ry+6), v2, fill=C_TEXT_SEC, font=font_m)
        draw.text((col_x[3]+8, ry+6), v3, fill=C_TEXT_SEC, font=font_m)

    # 趋势可视化
    try_fy = hy + 40 + len(table_data) * 32 + 16
    draw.text((wx+20, try_fy), "📈  功率趋势（同材料不同板厚）：", fill=C_TEXT, font=font_h)
    # 柱状图
    bar_y = try_fy + 30
    bars = [(0.5, 1500, C_GREEN), (1.0, 1800, C_BLUE), (1.5, 2000, C_GOLD)]
    for i, (th, pw, clr) in enumerate(bars):
        bx = col_x[i+1]
        bh = int(pw / 2000 * 80)
        draw.rectangle([bx+20, bar_y+80-bh, bx+100, bar_y+80], fill=hex_to_rgb(clr))
        draw.text((bx+20, bar_y+84), f"{pw}W", fill=clr, font=font_m)
        draw.text((bx+30, bar_y+96), f"{th}mm", fill=C_TEXT_LIGHT, font=font_s)

    # 结论
    draw.text((wx+20, bar_y+116), "💡 趋势：板厚每增加0.5mm，功率需增加约300W，速度下降约0.2m/min", fill=C_TEXT_SEC, font=font_s)

    # 标注
    draw.rectangle([0, H-50, W, H], fill="#1a1a2e")
    draw.text((40, H-42), "🆕 新增功能：参数对比窗口", fill="#aabbcc", font=font_h)
    draw.text((400, H-42), "同材料不同厚度横向对比 · 趋势可视化", fill="#667788", font=font_s)

    path = os.path.join(OUT_DIR, "05-新增-参数对比窗口.png")
    img.save(path)
    print(f"✅ {path}")
    return path

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    make_mobile_search()
    make_mobile_results()
    make_desktop_grid()
    make_detail_window()
    make_compare_window()
    print(f"\n📁 所有线框图已保存到: {OUT_DIR}")
    print("📝 打印或传输到手机查看，标注修改意见后反馈")
