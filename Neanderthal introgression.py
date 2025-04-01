import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib import rcParams
import matplotlib.font_manager as fm

# 字体设置
try:
    rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS
    # rcParams['font.sans-serif'] = ['SimHei']  # Windows
    # rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']  # Linux
except:
    rcParams['font.sans-serif'] = ['DejaVu Sans']  
rcParams['axes.unicode_minus'] = False

ANIMATION_PHASES = {
    "POINTS_DURATION": 30,  # 点动画持续时间
    "FADE_DURATION": 30,    # 淡出动画持续时间
    "ROTATE_DURATION": 30,  # 旋转动画持续时间
    "HOLD_DURATION": 80     # 保持持续时间   
}
TOTAL_FRAMES = sum(ANIMATION_PHASES.values())

COLORS = {
    "BG": '#0e1116',       # 背景色
    "BLUE": '#56B4E9',     # 蓝色
    "YELLOW": '#FFFF00',   # 黄色
    "GRAY": '#808080',     # 灰色
    "WHITE": '#FFFFFF'     # 白色
}

raw_data = [
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA18507 (约鲁巴人)", "D": -0.1, "type": "within_africa"},
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA19240 (约鲁巴人)", "D": 1.5, "type": "within_africa"},
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA19129 (约鲁巴人)", "D": -0.1, "type": "within_africa"},
    {"H1": "NA18507 (约鲁巴人)", "H2": "NA19240 (约鲁巴人)", "D": -0.5, "type": "within_africa"},
    {"H1": "NA18507 (约鲁巴人)", "H2": "NA19129 (约鲁巴人)", "D": 0.0, "type": "within_africa"},
    {"H1": "NA19240 (约鲁巴人)", "H2": "NA19129 (约鲁巴人)", "D": -0.6, "type": "within_africa"},
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA12878 (欧洲人)", "D": 4.1, "type": "africa_vs_eurasia"},
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA12156 (欧洲人)", "D": 5.1, "type": "africa_vs_eurasia"},
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA18956 (日本人)", "D": 2.9, "type": "africa_vs_eurasia"},
    {"H1": "NA18517 (约鲁巴人)", "H2": "NA18555 (中国人)", "D": 3.9, "type": "africa_vs_eurasia"},
    {"H1": "NA18507 (约鲁巴人)", "H2": "NA12878 (欧洲人)", "D": 4.2, "type": "africa_vs_eurasia"},
    {"H1": "NA18507 (约鲁巴人)", "H2": "NA12156 (欧洲人)", "D": 5.5, "type": "africa_vs_eurasia"},
    {"H1": "NA18507 (约鲁巴人)", "H2": "NA18956 (日本人)", "D": 5.0, "type": "africa_vs_eurasia"},
    {"H1": "NA18507 (约鲁巴人)", "H2": "NA18555 (中国人)", "D": 5.8, "type": "africa_vs_eurasia"},
    {"H1": "NA19240 (约鲁巴人)", "H2": "NA12878 (欧洲人)", "D": 3.5, "type": "africa_vs_eurasia"},
    {"H1": "NA19240 (约鲁巴人)", "H2": "NA12156 (欧洲人)", "D": 3.1, "type": "africa_vs_eurasia"},
    {"H1": "NA19240 (约鲁巴人)", "H2": "NA18956 (日本人)", "D": 2.7, "type": "africa_vs_eurasia"},
    {"H1": "NA19240 (约鲁巴人)", "H2": "NA18555 (中国人)", "D": 5.4, "type": "africa_vs_eurasia"},
    {"H1": "NA19129 (约鲁巴人)", "H2": "NA12878 (欧洲人)", "D": 3.9, "type": "africa_vs_eurasia"},
    {"H1": "NA19129 (约鲁巴人)", "H2": "NA12156 (欧洲人)", "D": 4.9, "type": "africa_vs_eurasia"},
    {"H1": "NA19129 (约鲁巴人)", "H2": "NA18956 (日本人)", "D": 5.1, "type": "africa_vs_eurasia"},
    {"H1": "NA19129 (约鲁巴人)", "H2": "NA18555 (中国人)", "D": 4.7, "type": "africa_vs_eurasia"},
    {"H1": "HGDP01029 (桑人)", "H2": "HGDP01029 (约鲁巴人)", "D": -0.1, "type": "within_africa"},
    {"H1": "HGDP01029 (桑人)", "H2": "HGDP00521 (法国人)", "D": 4.2, "type": "africa_vs_eurasia"},
    {"H1": "HGDP01029 (桑人)", "H2": "HGDP00542 (巴布亚人)", "D": 3.9, "type": "africa_vs_eurasia"},
    {"H1": "HGDP01029 (桑人)", "H2": "HGDP00778 (汉族)", "D": 5.0, "type": "africa_vs_eurasia"},
    {"H1": "HGDP01029 (约鲁巴人)", "H2": "HGDP00521 (法国人)", "D": 4.5, "type": "africa_vs_eurasia"},
    {"H1": "HGDP01029 (约鲁巴人)", "H2": "HGDP00542 (巴布亚人)", "D": 4.4, "type": "africa_vs_eurasia"},
    {"H1": "HGDP01029 (约鲁巴人)", "H2": "HGDP00778 (汉族)", "D": 5.3, "type": "africa_vs_eurasia"},
]

def clean_pop_name(name):
    """清洗名称"""
    return name.split('(')[-1].replace(')', '').strip()

processed_data = []
for entry in raw_data:
    cleaned_entry = {
        "H1": clean_pop_name(entry["H1"]),
        "H2": clean_pop_name(entry["H2"]),
        "D": entry["D"],
        "type": entry["type"],
        "color": COLORS["YELLOW"] if entry["type"] == "within_africa" else COLORS["BLUE"]
    }
    processed_data.append(cleaned_entry)

# 生成种群列表
african_pops = list(sorted({e["H1"] for e in processed_data if "约鲁巴人" in e["H1"] or "桑人" in e["H1"]}))
other_pops = list(sorted({e["H2"] for e in processed_data if e["H2"] not in african_pops}))
all_pops = african_pops + other_pops
pop_to_idx = {pop: i for i, pop in enumerate(all_pops)}

# 生成坐标数据
x = [pop_to_idx[e["H2"]] for e in processed_data]
y = [pop_to_idx[e["H1"]] for e in processed_data]
z = [e["D"] for e in processed_data]
colors = [e["color"] for e in processed_data]

plt.style.use('dark_background')
rcParams.update({
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': ':'
})

fig = plt.figure(figsize=(14, 10), facecolor=COLORS["BG"])
ax = fig.add_subplot(111, projection='3d', facecolor=COLORS["BG"])
fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

def setup_axes(axes):
    """初始化坐标轴样式"""
    axes.grid(True, linestyle=':', alpha=0.3)
    for axis in [axes.xaxis, axes.yaxis, axes.zaxis]:
        axis.line.set_linewidth(1.5)
        axis.line.set_color(COLORS["GRAY"])
        axis.set_pane_color((0, 0, 0, 0))

setup_axes(ax)

# 图例配置
legend_elements = [
    Line2D([0], [0], marker='o', color=COLORS["BG"], 
           markerfacecolor=COLORS["BLUE"], markersize=10, label='非洲 vs 欧亚大陆'),
    Line2D([0], [0], marker='o', color=COLORS["BG"], 
           markerfacecolor=COLORS["YELLOW"], markersize=10, label='非洲内部')
]

def calculate_progress(frame):
    """计算动画进度"""
    phases = [
        (0, ANIMATION_PHASES["POINTS_DURATION"], "points"),
        (ANIMATION_PHASES["POINTS_DURATION"], ANIMATION_PHASES["FADE_DURATION"], "fade"),
        (ANIMATION_PHASES["POINTS_DURATION"] + ANIMATION_PHASES["FADE_DURATION"], 
         ANIMATION_PHASES["ROTATE_DURATION"], "rotate"),
        (ANIMATION_PHASES["POINTS_DURATION"] + ANIMATION_PHASES["FADE_DURATION"] + ANIMATION_PHASES["ROTATE_DURATION"],
         ANIMATION_PHASES["HOLD_DURATION"], "hold")
    ]
    
    for start, duration, phase in phases:
        if start <= frame < start + duration:
            return phase, (frame - start) / duration if duration > 0 else 1.0
    return "hold", 1.0

def update(frame):
    ax.clear()
    setup_axes(ax)
    
    # 显示数据点
    current_limit = min(frame + 1, len(processed_data))
    ax.scatter(x[:current_limit], y[:current_limit], z[:current_limit],
               c=colors[:current_limit], s=80, alpha=0.8, depthshade=False)

    # 处理动画阶段
    phase, progress = calculate_progress(frame)
    
    # 标签透明度控制
    if phase == "hold":
        label_alpha = 0.0  # 保持最终状态
    else:
        label_alpha = 1.0 - progress if phase == "fade" else (0.0 if phase == "rotate" else 1.0)
    
    # 坐标轴标签设置
    ax.set_xticks(np.arange(len(all_pops)))
    ax.set_yticks(np.arange(len(all_pops)))
    ax.set_xticklabels(all_pops, rotation=45, ha='right', 
                       color=COLORS["WHITE"], alpha=label_alpha)
    ax.set_yticklabels(all_pops, rotation=-45, ha='left', 
                       color=COLORS["WHITE"], alpha=label_alpha)
    
    # 轴标签
    ax.set_xlabel('H2 种群', fontsize=14, color=COLORS["WHITE"], 
                  alpha=label_alpha, labelpad=40)
    ax.set_ylabel('H1 种群', fontsize=14, color=COLORS["WHITE"], 
                  alpha=label_alpha, labelpad=40)
    ax.set_zlabel('D 值', fontsize=14, color=COLORS["WHITE"], labelpad=15)

    # 视角控制
    if phase == "rotate":
        ax.view_init(elev=25*(1 - progress), azim=-60 - 30*progress)
    elif phase == "hold":
        # 保持最终2D视图
        ax.view_init(elev=0, azim=-89.5)
    else:
        ax.view_init(elev=25, azim=-60)

    # 固定显示范围
    ax.set_xlim(-0.5, len(all_pops)-0.5)
    ax.set_ylim(-0.5, len(all_pops)-0.5)
    ax.set_zlim(min(z)-1, max(z)+1)
    
    # 标题和图例
    ax.set_title('共享尼安德特人等位基因程度 (D统计量)', 
                 pad=20, fontsize=16, color=COLORS["BLUE"])
    ax.legend(handles=legend_elements, loc='upper right', 
              framealpha=0.5, facecolor=COLORS["BG"])
    
    return ax,

# 运行动画
ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=50, blit=False)
plt.show()

# 保存动画
# ani.save('neanderthal_d_statistics.mp4', 
#          writer='ffmpeg', 
#          fps=20, 
#          dpi=200,  
#          savefig_kwargs={
#              'facecolor': COLORS["BG"],  
#              'transparent': False
# })