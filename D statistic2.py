import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams

# 字体设置
try:
    rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS
    # rcParams['font.sans-serif'] = ['SimHei']  # Windows
    # rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']  # Linux
except:
    rcParams['font.sans-serif'] = ['DejaVu Sans']  
rcParams['axes.unicode_minus'] = False

# 全局变量初始化
D_values = []
ABBA_counts = []
BABA_counts = []

# 设置参数
n_steps = 200
introgressions = np.linspace(0, 0.5, n_steps)

# 模拟函数
def simulate_abba_baba(introgression):
    ABBA = 1000 * (0.1 + 0.1 * introgression)
    BABA = 1000 * (0.1 + 0.8 * introgression)
    return ABBA, BABA

def calculate_D(ABBA, BABA):
    denominator = ABBA + BABA
    if denominator == 0:
        return 0
    return (ABBA - BABA) / denominator

# 创建纯黑色背景的图形
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 8), facecolor='black')

# 创建子图网格
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.3], width_ratios=[1, 1])
ax1 = fig.add_subplot(gs[0, 0], facecolor='black')  # 树结构
ax2 = fig.add_subplot(gs[0, 1], facecolor='black')  # D值曲线
ax_text = fig.add_subplot(gs[1, :], facecolor='black')  # 文本解释
ax_text.axis('off')

# 定义树结构
def draw_tree(ax, introgression):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3.5, 0.5)
    ax.axis('off')
    
    G = nx.DiGraph()
    
    pos = {
        '': (1.5, 0.0),      # 共同祖先节点
        ' ': (0.0, -1.0),     # 第一个分支点
        'O': (3.0, -3.0),     # 外群
        'P3': (1.0, -3.0),    # 群体3
        '  ': (-1.5, -2.0),  # 第二个分支点
        'P2': (-1.0, -3.0),   # 群体2
        'P1': (-3.0, -3.0)    # 群体1
    }
    
    edges = [
        ('', ' '),    # 共同祖先节点到第一个分支
        ('', 'O'),   # 第一个分支到外群
        (' ', 'P3'), # 第二个分支到P3
        (' ', '  '), # 第二个分支到第三个分支
        ('  ', 'P2'), # 第三个分支到P2
        ('  ', 'P1')  # 第三个分支到P1
    ]
    G.add_edges_from(edges)
    
    # 绘制所有边，其中 (' ', 'P3') 和 ('  ', 'P1') 的宽度随 introgression 变化
    edge_widths = [3] * len(edges)  # 默认宽度
    edge_alphas = [0.8] * len(edges)  # 默认透明度
    
    # 找到 (' ', 'P3') 和 ('  ', 'P1') 的索引
    p3_edge_idx = edges.index((' ', 'P3'))
    p1_edge_idx = edges.index(('  ', 'P1'))
    
    # 设置这两条边的宽度和透明度（随 introgression 增加）
    edge_widths[p3_edge_idx] = 3 + 10 * introgression
    edge_widths[p1_edge_idx] = 3 + 10 * introgression
    edge_alphas[p3_edge_idx] = 0.8 + 0.4 * introgression  
    edge_alphas[p1_edge_idx] = 0.8 + 0.4 * introgression  
    # 绘制边
    for i, (u, v) in enumerate(edges):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax, 
                             edge_color='#23aaff', 
                             width=edge_widths[i], 
                             alpha=edge_alphas[i], 
                             arrows=False)
    
    for node, (x, y) in pos.items():
        if node.strip():
            color = {
                'P1': '#ff7f7f',
                'P2': '#7fff7f',
                'P3': '#ff7fff',
                'O': '#ffff7f'
            }.get(node, 'lightblue')
            
            ax.text(x, y, node, color=color, fontsize=12, ha='center', va='center',
                   bbox=dict(facecolor='black', edgecolor=color, boxstyle='round,pad=0.3'))
    
    ax.text(1.5, 0.2, '共同祖先节点', ha='center', color='white', fontsize=12)
    
    if introgression > 0:
        start_pos = (-2.625, -2.75)
        end_pos = (0.875, -2.75)

        arrow_style = dict(arrowstyle="-", color="#ff5555", 
                          lw=3 + 10*introgression, alpha=0.6 + 0.6*introgression)
        ax.annotate("", xy=end_pos, xytext=start_pos,
                    arrowprops=arrow_style)
    
    ax.set_title(f"混血分析", 
                 pad=20, color='white', fontsize=14)

# 初始化动画
def init():
    global D_values, ABBA_counts, BABA_counts
    D_values = []
    ABBA_counts = []
    BABA_counts = []
    
    ax2.clear()
    ax2.set_facecolor('black')
    ax2.set_xlim(0, n_steps-1)
    ax2.set_ylim(-0.2, 0.8)
    ax2.set_xlabel("基因渗入事件", fontsize=12, color='white')
    ax2.set_ylabel("D统计量", fontsize=12, color='white')
    ax2.grid(True, color='#333344', linestyle='--', alpha=0.5)
    ax2.set_title(r"$D = \frac{ABBA - BABA}{ABBA + BABA}$", 
                 pad=20, color='white', fontsize=16)
    
    ax_text.clear()
    ax_text.axis('off')
    ax_text.set_xlim(0, 1)
    ax_text.set_ylim(0, 1)
    ax_text.text(0.02, 0.8, "ABBA-BABA检验解释:", 
                 color='#23aaff', fontsize=14)
    ax_text.text(0.05, 0.6, r"$\bullet$ D > 0: ABBA多于BABA (P2-P3基因渗入)", 
                 color='white', fontsize=12)
    ax_text.text(0.05, 0.4, r"$\bullet$ D = 0: 无基因渗入证据", 
                 color='white', fontsize=12)
    ax_text.text(0.05, 0.2, r"$\bullet$ ABBA: P3和P2共享的衍生等位基因", 
                 color='#ff7f7f', fontsize=12)
    ax_text.text(0.05, 0.0, r"$\bullet$ BABA: P3和P1共享的衍生等位基因", 
                 color='#7fff7f', fontsize=12)
    
    return []

# 更新动画
def update(step):
    global D_values, ABBA_counts, BABA_counts
    
    introgression = introgressions[step]
    ABBA, BABA = simulate_abba_baba(introgression)
    D = calculate_D(ABBA, BABA)
    
    ABBA_counts.append(ABBA)
    BABA_counts.append(BABA)
    D_values.append(D)
    
    draw_tree(ax1, introgression)
    
    ax2.clear()
    ax2.set_facecolor('black')
    ax2.plot(range(len(D_values)), D_values, color='#23aaff', lw=4, alpha=0.8, 
             label=f"D值 (当前: {D:.3f})")
    ax2.scatter([len(D_values)-1], [D], color='#ff5555', s=100, zorder=5)
    ax2.axhline(0, color='white', linestyle=':', alpha=0.7)
    
    ax2.set_xlim(0, n_steps-1)
    y_min = min(-0.2, min(D_values) - 0.1)
    y_max = max(0.8, max(D_values) + 0.1)
    ax2.set_ylim(y_min, y_max)
    ax2.set_xlabel("基因渗入事件", fontsize=12, color='white')
    ax2.set_ylabel("D统计量", fontsize=12, color='white')
    ax2.grid(True, color='#333344', linestyle='--', alpha=0.5)
    ax2.legend(loc='upper left', fontsize=12, facecolor='black', edgecolor='none')
    
    ax2.text(0.02, 0.85, f"ABBA: {int(ABBA)}    BABA: {int(BABA)}", 
             transform=ax2.transAxes, fontsize=12, color='white',
             bbox=dict(facecolor='black', edgecolor='#23aaff', pad=5))
    
    ax_text.clear()
    ax_text.axis('off')
    ax_text.set_xlim(0, 1)
    ax_text.set_ylim(0, 1)
    
    explanation = [
        "解释说明:",
        "ABBA为P2和P3之间共享的等位基因",
        "BABA为P1和P3之间共享的等位基因",
        f"D = ({int(ABBA)} - {int(BABA)}) / ({int(ABBA)} + {int(BABA)}) = {D:.3f}",
        "随着基因渗入增加，D值变得更负",
        "表明P1和P3之间有更多的等位基因共享",
        "作者：迷雾幻境里的梦龙"
    ]
    
    for i, line in enumerate(explanation):
        ax_text.text(0.02, 0.8 - i*0.15, line, color='white', fontsize=12 + (i==0)*2)
    
    return []

# 创建动画
ani = FuncAnimation(fig, update, frames=n_steps, init_func=init, 
                   blit=False, interval=50)

# 保存动画
# ani.save(r'abba_baba2.mp4', writer='ffmpeg', fps=30, dpi=150)

plt.tight_layout()
plt.show()