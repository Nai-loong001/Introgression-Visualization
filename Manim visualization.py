from manim import *

class FinalCombinedAnimation(Scene):
    def construct(self):
        #设置中文支持
        Text.set_default(font="STKaiti")
        Tex.set_default(tex_environment="ctex")
        
        formula = MathTex(r"\frac{ABBA - BABA}{ABBA + BABA}", 
                         font_size=60, color=BLUE)
        self.play(Write(formula), run_time=2)
        
        #高亮分子ABBA
        abba_box = SurroundingRectangle(formula[0][0:4], color=YELLOW, buff=0.1)
        annotation1 = Text("2和3共享等位基因", font_size=36, color=RED)
        annotation1.next_to(abba_box, UP, buff=0.3)
        arrow1 = Arrow(annotation1.get_bottom(), abba_box.get_top(), color=RED)
        
        self.play(Create(abba_box))
        self.play(Write(annotation1), GrowArrow(arrow1), run_time=1.5)
        self.wait(1)
        
        #高亮分母BABA
        baba_box = SurroundingRectangle(formula[0][15:20], color=YELLOW, buff=0.1)
        annotation2 = Text("1和3共享等位基因", font_size=36, color=GREEN)
        annotation2.next_to(baba_box, DOWN, buff=0.3)
        arrow2 = Arrow(annotation2.get_top(), baba_box.get_bottom(), color=GREEN)
        
        self.play(Create(baba_box))
        self.play(Write(annotation2), GrowArrow(arrow2), run_time=1.5)
        self.wait(1)
        
        #添加D=并形成等式
        d_symbol = MathTex("D = ", font_size=60, color=WHITE)
        d_symbol.next_to(formula, LEFT, buff=0.5)
        equation = VGroup(d_symbol, formula)
        
        self.play(Write(d_symbol), run_time=1)
        self.wait(0.5)
        
        #整体移动并缩放到右侧
        formula_group = VGroup(equation, abba_box, annotation1, arrow1, baba_box, annotation2, arrow2)
        self.play(formula_group.animate.scale(0.7).to_edge(RIGHT, buff=1), run_time=2)
        self.wait(0.5)
        
        #定义基准高度
        baseline_y = -1.0
        terminal_radius = 0.2
        
        #定义节点位置
        positions = {
            'root': UP * 1.5 + LEFT * 3.0,
            'branch1': UP * 0.8 + LEFT * 3.0,
            'O': RIGHT * 1.5 + baseline_y * UP + LEFT * 3.0,
            'P1': LEFT * 1.5 + baseline_y * UP + LEFT * 3.0
        }
        
        #计算分支结构
        o_branch_vector = positions['O'] - positions['branch1']
        branch_angle = np.arctan2(o_branch_vector[1], o_branch_vector[0])
        main_branch_vector = positions['P1'] - positions['branch1']
        
        positions['branch2'] = positions['branch1'] + main_branch_vector * 0.4
        positions['branch3'] = positions['branch1'] + main_branch_vector * 0.7
        
        #计算P3和P2位置
        delta_y = baseline_y - positions['branch2'][1]
        L_p3 = delta_y / np.sin(branch_angle)
        positions['P3'] = positions['branch2'] + L_p3 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
        
        delta_y = baseline_y - positions['branch3'][1]
        L_p2 = delta_y / np.sin(branch_angle)
        positions['P2'] = positions['branch3'] + L_p2 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
        
        #创建节点标签
        labels = {
            'root': Text("共同祖先节点", font_size=28, color=WHITE).next_to(positions['root'], UP, buff=0.1),
            'O': Text("O", font_size=15, color="#ffff7f"),
            'P1': Text("P1", font_size=15, color="#ff7f7f"),
            'P2': Text("P2", font_size=15, color="#7fff7f"),
            'P3': Text("P3", font_size=15, color="#ff7fff")
        }
        
        #创建节点圆形
        nodes = {
            'O': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, 
                       stroke_color="#ffff7f", stroke_width=2),
            'P1': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, 
                        stroke_color="#ff7f7f", stroke_width=2),
            'P2': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, 
                        stroke_color="#7fff7f", stroke_width=2),
            'P3': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, 
                        stroke_color="#ff7fff", stroke_width=2)
        }
        
        #设置节点位置
        for key in nodes:
            nodes[key].move_to(positions[key])
            labels[key].move_to(positions[key])
        
        #创建连接线
        lines = [
            Line(positions['root'], positions['branch1'], color="#23aaff", stroke_width=4),
            Line(positions['branch1'], positions['O'], color="#23aaff", stroke_width=4),
            Line(positions['branch1'], positions['branch2'], color="#23aaff", stroke_width=4),
            Line(positions['branch2'], positions['P3'], color="#23aaff", stroke_width=4),
            Line(positions['branch2'], positions['branch3'], color="#23aaff", stroke_width=4),
            Line(positions['branch3'], positions['P2'], color="#23aaff", stroke_width=4),
            Line(positions['branch3'], positions['P1'], color="#23aaff", stroke_width=4)
        ]
        
        #绘制主干
        self.play(Create(lines[0]), run_time=1)
        self.wait(0.3)
        
        #分支到外群O
        self.play(
            Create(lines[1]),
            Create(nodes['O']),
            Write(labels['O']),
            run_time=1
        )
        self.wait(0.3)
        
        #主分支延伸
        self.play(Create(lines[2]), run_time=1)
        self.wait(0.3)
        
        #分支到P3
        self.play(
            Create(lines[3]),
            Create(nodes['P3']),
            Write(labels['P3']),
            run_time=1
        )
        self.wait(0.3)
        
        #主分支延伸
        self.play(Create(lines[4]), run_time=1)
        self.wait(0.3)
        
        #分支到P2
        self.play(
            Create(lines[5]),
            Create(nodes['P2']),
            Write(labels['P2']),
            run_time=1
        )
        self.wait(0.3)
        
        #最后到P1
        self.play(
            Create(lines[6]),
            Create(nodes['P1']),
            Write(labels['P1']),
            run_time=1
        )
        self.wait(0.3)
        
        #添加共同祖先节点标签
        self.play(Write(labels['root']), run_time=1)
        self.wait(0.5)
        
        #第一行标签 (A, B, B, A)
        allele_labels1 = VGroup(
            Text("A", font_size=24).next_to(nodes['P1'], DOWN, buff=0.3),
            Text("B", font_size=24).next_to(nodes['P2'], DOWN, buff=0.3),
            Text("B", font_size=24).next_to(nodes['P3'], DOWN, buff=0.3),
            Text("A", font_size=24).next_to(nodes['O'], DOWN, buff=0.3)
        )
        
        #第二行标签 (B, A, B, A)
        allele_labels2 = VGroup(
            Text("B", font_size=24).next_to(allele_labels1[0], DOWN, buff=0.2),
            Text("A", font_size=24).next_to(allele_labels1[1], DOWN, buff=0.2),
            Text("B", font_size=24).next_to(allele_labels1[2], DOWN, buff=0.2),
            Text("A", font_size=24).next_to(allele_labels1[3], DOWN, buff=0.2)
        )
        
        #动画添加标签
        self.play(LaggedStart(*[Write(l) for l in allele_labels1], lag_ratio=0.2), run_time=1.5)
        self.wait(0.5)
        self.play(LaggedStart(*[Write(l) for l in allele_labels2], lag_ratio=0.2), run_time=1.5)
        self.wait(0.5)
        
        formula_explanation = Text("D即为D统计量", 
                         font_size=32,
                         color=YELLOW)\
                         .next_to(formula_group, DOWN, buff=0.3)\
                         .align_to(formula_group, LEFT)
        Tree_explanation = Text("若无混血事件，则ABBA与BABA数量几乎相等", 
                         font_size=32,
                         color=RED)\
                         .next_to(allele_labels2, DOWN, buff=0.3)\
                         .align_to(allele_labels2, LEFT)

        self.play(Write(formula_explanation), run_time=1)
        self.play(Write(Tree_explanation), run_time=1)

        all_elements = VGroup(
            formula_group,
            *lines,
            *nodes.values(),
            *labels.values(),
            allele_labels1,
            allele_labels2,
            formula_explanation
        )

        #创建要保留并移动到中央的文字
        final_message = Text("若无混血事件，则ABBA与BABA数量几乎相等", 
                    font_size=36,  
                    color=RED)
        
        #动画序列：
        #其他元素渐隐
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.5)

        #文字出现并移动到中央
        self.play(
            Transform(Tree_explanation, final_message.move_to(ORIGIN)),  
            run_time=1.5
        )
        self.wait(2)  

        #最后渐隐
        self.play(FadeOut(final_message), run_time=1)

        self.wait(3)

#使用命令渲染：
#manim -pqh --resolution=1920,1080 test.py FinalCombinedAnimation


class Interval(Scene):
    def construct(self):
        #设置中文支持
        Text.set_default(font="STKaiti")
        Tex.set_default(tex_environment="ctex")

        #创建要留到中央的文字
        interval_message1 = Text("若P1与P3混血，则BABA数量多于ABBA", 
                    font_size=36,  
                    color=YELLOW)\
                        .move_to(ORIGIN)
        self.play(Write(interval_message1), run_time=1)
        self.wait(2)
        
        #最后渐隐
        self.play(FadeOut(interval_message1), run_time=1)
        self.wait(3)

        #创建要留到中央的文字
        interval_message2 = Text("若P2与P3混血，则ABBA数量多于BABA", 
                    font_size=36,  
                    color=GREEN)\
                        .move_to(ORIGIN)
        self.play(Write(interval_message2), run_time=1)
        self.wait(2)
        
        #最后渐隐
        self.play(FadeOut(interval_message2), run_time=1)
        self.wait(3)

        #创建要留到右边的文字
        interval_message2 = Text("2010年的Science文章第一次报道\n现代人和尼安德特人存在混血", 
                    font_size=28,  
                    color=GREEN)\
                        .to_edge(RIGHT, buff=1).to_edge(UP, buff=3)
        self.play(Write(interval_message2), run_time=1.5)
        self.wait(2)  

        #创建要显示在右下角的文字
        d_stat_text = Text("首次提出一种检验混血的方法", 
                          font_size=28,
                          color=WHITE)\
                          .next_to(interval_message2, DOWN, aligned_edge=LEFT, buff=0.5)
        d_stat_red = Text("D统计量", 
                    font_size=28,
                     color=RED)\
                     .next_to(d_stat_text, DOWN, aligned_edge=LEFT, buff=0.3)

        #先显示第二段文字
        self.play(Write(d_stat_text), run_time=1)
        self.wait(1)  

        #然后显示红色"D统计量"
        self.play(Write(d_stat_red), run_time=1)
        self.wait(2)  

        #最后一起淡出所有文字
        self.play(
            FadeOut(interval_message2),
            FadeOut(d_stat_text),
            FadeOut(d_stat_red),
            run_time=1.5
        )
        

#使用命令渲染：
#manim -pqh --resolution=1920,1080 test.py Interval

from manim import *

class NeanderthalDialogueAnimation(Scene):
    def construct(self):
        #设置中文支持
        Text.set_default(font="STKaiti")
        
        #第一行文字（施万特·帕博说的）
        text1 = Text("尼安德特人没有完全灭绝，他们的DNA仍存在于今天的人类中",
                   font_size=32,
                   color=YELLOW)
        signature1 = Text("——施万特·帕博", font_size=24, color=WHITE).next_to(text1, DOWN*2, buff=0.2).shift(RIGHT*4.5)
        top_text = VGroup(text1, signature1).center().shift(UP*2)
        
         #第二行文字（偏下）带关键词高亮
        line1_part1 = Text("尼安德特人与", font_size=32, color=BLUE_C)
        highlight1 = Text("所有非洲以外人群", font_size=32, color=RED)
        line1_part2 = Text("的血缘关系", font_size=32, color=BLUE_C)
        
        line2_part1 = Text("都比", font_size=32, color=BLUE_C)
        highlight2 = Text("所有撒哈拉以南非洲人", font_size=32, color=RED)
        line2_part2 = Text("要更", font_size=32, color=BLUE_C)
        highlight3 = Text("亲近", font_size=32, color=RED)
        line2_part3 = Text("些", font_size=32, color=BLUE_C)
        
        #组合第一行
        bottom_line1 = VGroup(
            line1_part1, highlight1, line1_part2
        ).arrange(RIGHT, buff=0.08)
        
        #组合第二行
        bottom_line2 = VGroup(
            line2_part1, highlight2, line2_part2, highlight3, line2_part3
        ).arrange(RIGHT, buff=0.08)
        
        signature2 = Text("——大卫·赖克", font_size=24, color=WHITE).next_to(bottom_line2, DOWN, buff=0.2)

        #组合所有行
        bottom_text = VGroup(bottom_line1, bottom_line2, signature2)\
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.3)\
            .center()\
            .shift(DOWN*1)
        
        #动画序列（完全保持原有动画效果）
        self.play(
            LaggedStart(
                Write(top_text),
                lag_ratio=0.8
            ),
            run_time=2
        )
        self.wait(1)
        
        self.play(
            LaggedStart(
                Write(bottom_text),
                lag_ratio=0.8
            ),
            run_time=2
        )
        self.wait(3)
        
        #渐隐效果
        self.play(
            FadeOut(top_text),
            FadeOut(bottom_text),
            run_time=1.5
        )

#manim -pqh --resolution=1920,1080 test.py NeanderthalDialogueAnimation

class PerfectPhylogeneticTree(Scene):
    def construct(self):
        #设置背景颜色
        self.camera.background_color = BLACK
        
        #定义基准高度（所有终端节点在同一水平线上）
        baseline_y = -2.5
        terminal_radius = 0.3  
        
        #定义关键节点位置
        positions = {
            'root': UP * 2.5,               
            'branch1': UP * 1.5,             
            'O': RIGHT * 3 + baseline_y * UP, 
            'P1': LEFT * 3 + baseline_y * UP  
        }
        
        #计算O分支的角度和长度（作为基准）
        o_branch_vector = positions['O'] - positions['branch1']
        branch_angle = np.arctan2(o_branch_vector[1], o_branch_vector[0])
        branch_length = np.linalg.norm(o_branch_vector)
        
        #计算主干方向 (branch1到P1)
        main_branch_vector = positions['P1'] - positions['branch1']
        
        #计算分支点位置 (沿主干均匀分布)
        positions['branch2'] = positions['branch1'] + main_branch_vector * 0.4
        positions['branch3'] = positions['branch1'] + main_branch_vector * 0.7

        delta_y = baseline_y - positions['branch2'][1]
        L_p3 = delta_y / np.sin(branch_angle)
        positions['P3'] = positions['branch2'] + L_p3 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
        
        #同样计算P2位置
        delta_y = baseline_y - positions['branch3'][1]
        L_p2 = delta_y / np.sin(branch_angle)
        positions['P2'] = positions['branch3'] + L_p2 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
        
        #创建节点标签
        labels = {
            'root': Text("共同祖先节点", font_size=24, color=WHITE).next_to(positions['root'], UP, buff=0.1),
            'O': Text("O", font_size=24, color="#ffff7f"),
            'P1': Text("P1", font_size=24, color="#ff7f7f"),
            'P2': Text("P2", font_size=24, color="#7fff7f"),
            'P3': Text("P3", font_size=24, color="#ff7fff")
        }
        
        #创建节点圆形
        nodes = {
            'O': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#ffff7f"),
            'P1': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#ff7f7f"),
            'P2': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#7fff7f"),
            'P3': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#ff7fff")
        }
        
        #设置节点位置
        for key in nodes:
            nodes[key].move_to(positions[key])
            labels[key].move_to(positions[key])
        
        #创建连接线
        lines = [
            #主干线
            Line(positions['root'], positions['branch1'], color="#23aaff"),
            
            #O分支 (基准分支)
            Line(positions['branch1'], positions['O'], color="#23aaff"),
            
            #主分支继续延伸
            Line(positions['branch1'], positions['branch2'], color="#23aaff"),
            
            #P3分支 (与O平行)
            Line(positions['branch2'], positions['P3'], color="#23aaff"),
            
            #主分支继续延伸
            Line(positions['branch2'], positions['branch3'], color="#23aaff"),
            
            #P2分支 (与O平行)
            Line(positions['branch3'], positions['P2'], color="#23aaff"),
            
            #最后到P1
            Line(positions['branch3'], positions['P1'], color="#23aaff")
        ]
        
        #动画序列
        #首先绘制主干
        self.play(Create(lines[0]), run_time=1)
        self.wait(0.3)
        
        #分支到外群O (基准分支)
        self.play(
            Create(lines[1]),
            Create(nodes['O']),
            Write(labels['O']),
            run_time=1
        )
        self.wait(0.3)
        
        #主分支继续延伸
        self.play(
            Create(lines[2]),
            run_time=1
        )
        self.wait(0.3)
        
        #分支到P3 (与O平行)
        self.play(
            Create(lines[3]),
            Create(nodes['P3']),
            Write(labels['P3']),
            run_time=1
        )
        self.wait(0.3)
        
        #主分支继续延伸
        self.play(
            Create(lines[4]),
            run_time=1
        )
        self.wait(0.3)
        
        #分支到P2 (与O平行)
        self.play(
            Create(lines[5]),
            Create(nodes['P2']),
            Write(labels['P2']),
            run_time=1
        )
        self.wait(0.3)
        
        #最后到达P1
        self.play(
            Create(lines[6]),
            Create(nodes['P1']),
            Write(labels['P1']),
            run_time=1
        )
        self.wait(0.3)
        
        #添加共同祖先节点标签
        self.play(Write(labels['root']), run_time=1)

        allele_labels1 = VGroup(
            Text("A", font_size=24).next_to(nodes['P1'], DOWN, buff=0.3),
            Text("B", font_size=24).next_to(nodes['P2'], DOWN, buff=0.3),
            Text("B", font_size=24).next_to(nodes['P3'], DOWN, buff=0.3),
            Text("A", font_size=24).next_to(nodes['O'], DOWN, buff=0.3)
        )
        self.play(LaggedStart(*[Write(l) for l in allele_labels1], lag_ratio=0.2), run_time=1.5)
        
        #添加黄框突出显示共享等位基因的节点
        highlight_group = VGroup(
            nodes['P2'],
            nodes['P3'],
            allele_labels1[1],  
            allele_labels1[2]   
        )
        
        #创建黄框
        highlight_box = SurroundingRectangle(
            highlight_group,
            color=YELLOW,
            buff=0.3,
            stroke_width=2,
            corner_radius=0.2
        )
        
        #创建注释文本
        annotation_text = Text("共享相同等位基因", font_size=24, color=RED)
        annotation_text.next_to(highlight_box, UP, buff=0.2)
        
        #动画显示
        self.play(
            Create(highlight_box),
            Write(annotation_text),
            run_time=1.5
        )

        entire_tree = VGroup(
            *lines,
            *nodes.values(),
            *labels.values(),
            allele_labels1,
            highlight_box,
            annotation_text
        )
        
        #计算缩放和平移参数
        target_scale = 0.8  
        target_x_offset = -2.5  
        
        #创建目标位置
        entire_tree.generate_target()
        entire_tree.target.scale(target_scale)\
                      .to_edge(LEFT, buff=1.5)\
                      .shift(UP*0.2)  
        
        #动画效果 - 平滑移动和缩放
        self.play(
            MoveToTarget(entire_tree),
            run_time=2,
            rate_func=smooth
        )
        
        #左侧树稳定后暂停
        self.wait(1.5)  

        main_tree = VGroup(
            *lines,
            *nodes.values(),
            *labels.values(),
        )

        #创建右侧树（BABA模式）
        right_tree = main_tree.copy()
        
        #精确定位（与左侧对称）
        right_pos = main_tree.get_center()
        right_pos[0] = -right_pos[0]  # 水平镜像
        right_tree.move_to(right_pos)
        
        #动画显示右侧树
        right_tree.set_opacity(0)
        self.play(
            right_tree.animate.set_opacity(1),
            run_time=2,
            rate_func=smooth
        )
        
        #获取右树中节点的引用
        #通常顺序是：线条(7个) + 节点(4个: O, P1, P2, P3)
        right_nodes = {
            'O': right_tree[7],    
            'P1': right_tree[8],   
            'P2': right_tree[9],  
            'P3': right_tree[10]  
        }

        #创建BABA模式的等位基因标签 - 确保正确对应
        allele_labels2 = VGroup(
            Text("B", font_size=19).next_to(right_nodes['P1'], DOWN, buff=0.22),  
            Text("A", font_size=19).next_to(right_nodes['P2'], DOWN, buff=0.22),  
            Text("B", font_size=19).next_to(right_nodes['P3'], DOWN, buff=0.22),  
            Text("A", font_size=19).next_to(right_nodes['O'], DOWN, buff=0.22)    
        )

        #显示右树的等位基因标签
        self.play(
            LaggedStart(*[Write(l) for l in allele_labels2], lag_ratio=0.2), 
            run_time=1.5
        )

        #添加右树的高亮框（高亮P1和P3的B）
        #第一个高亮框：P1的B
        highlight_b_p1 = VGroup(
            right_nodes['P1'],
            allele_labels2[0] 
        )
        
        box_p1 = SurroundingRectangle(
            highlight_b_p1,
            color="#FFA500", 
            buff=0.3,
            stroke_width=2,
            corner_radius=0.2
        )
        
        #第二个高亮框：P3的B
        highlight_b_p3 = VGroup(
            right_nodes['P3'],
            allele_labels2[2]  
        )
        
        box_p3 = SurroundingRectangle(
            highlight_b_p3,
            color="#FFA500",  
            buff=0.3,
            stroke_width=2,
            corner_radius=0.2
        )
        center_point = (box_p1.get_center() + box_p3.get_center()) / 2
        center_point[1] = box_p1.get_bottom()[1] - 0.5  
        
        right_annotation = Text("共享相同等位基因", font_size=20, color=RED)
        right_annotation.move_to(center_point)
        
        #动画显示两个高亮框和注释
        self.play(
            LaggedStart(
                Create(box_p1),
                Create(box_p3),
                lag_ratio=0.3
            ),
            run_time=1.5
        )
        self.play(
            Write(right_annotation),
            run_time=1
        )
        
        #更新标题添加方式
        left_title = Text("ABBA模式", font_size=22, color="#23aaff")
        left_title.next_to(entire_tree, UP, buff=0.3)
        
        right_title = Text("BABA模式", font_size=22, color="#ff7f7f")
        right_title.next_to(right_tree, UP, buff=0.3)
        
        self.play(
            FadeIn(left_title, shift=DOWN),
            FadeIn(right_title, shift=DOWN),
            run_time=1.5
        )
        
        self.wait(3)

#manim -pqh --resolution=1920,1080 test.py PerfectPhylogeneticTree

from scipy import stats

class GeneticDistancePlot(Scene):
    def construct(self):
        #设置黑色背景
        self.camera.background_color = BLACK
        
        #创建坐标轴
        axes = Axes(
            x_range=[0.5, 2.5, 1],
            y_range=[-2, 7, 1],
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_numbers": True,
            },
            x_axis_config={
                "include_ticks": False,
                "include_numbers": False,
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
            y_axis_config={
                "numbers_to_include": np.arange(-2, 7, 1),
                "tick_size": 0.05,
                "numbers_with_elongated_ticks": np.arange(-2, 8, 1),
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
            tips=True,
            x_length=4,
            y_length=5,
        ).shift(DOWN*0.3)

        #手动添加x轴刻度线
        x_ticks = VGroup()
        for x in [1, 2]:
            tick = Line(
                start=axes.c2p(x, 0),
                end=axes.c2p(x, -0.1),
                stroke_width=2,
                color=WHITE
            )
            x_ticks.add(tick)

        #Y轴标签
        y_label = axes.get_y_axis_label("D(\%)", edge=LEFT, direction=LEFT, buff=0.2)
        
        #添加坐标轴和标签
        self.play(Create(axes), Write(y_label))
        self.play(Create(x_ticks))
        self.wait(0.5)
        
        #处理数据并计算统计量
        within_africa = []
        africa_eurasia = []
        
        for entry in raw_data:
            if entry["type"] == "within_africa":
                within_africa.append(entry["D"])
            else:
                africa_eurasia.append(entry["D"])
        
        #计算均值和标准差
        def calculate_stats(data):
            mean = np.mean(data)
            std = np.std(data, ddof=1)  
            return mean, std
        
        w_mean, w_std = calculate_stats(within_africa)
        a_mean, a_std = calculate_stats(africa_eurasia)
        
        #创建数据点
        within_dots = VGroup(*[
            Dot(point=axes.c2p(1, d), color=BLUE, radius=0.06)
            for d in within_africa
        ])
        
        eurasia_dots = VGroup(*[
            Dot(point=axes.c2p(2, d), color=YELLOW, radius=0.06)
            for d in africa_eurasia
        ])

        #创建误差条
        def create_error_bar(x, mean, std, color):
            top = mean + std
            bottom = mean - std
            #主垂直线
            line = Line(
                start=axes.c2p(x, bottom),
                end=axes.c2p(x, top),
                color=color,
                stroke_width=2
            )
            #顶部横线
            cap_top = Line(
                start=axes.c2p(x-0.1, top),
                end=axes.c2p(x+0.1, top),
                color=color,
                stroke_width=2
            )
            #底部横线
            cap_bottom = Line(
                start=axes.c2p(x-0.1, bottom),
                end=axes.c2p(x+0.1, bottom),
                color=color,
                stroke_width=2
            )
            return VGroup(line, cap_top, cap_bottom)
        
        #创建误差条
        w_error = create_error_bar(1, w_mean, w_std, BLUE)
        a_error = create_error_bar(2, a_mean, a_std, YELLOW)
        
        #动画序列
        self.play(
            LaggedStart(*[Create(d) for d in within_dots], lag_ratio=0.1),
            LaggedStart(*[Create(d) for d in eurasia_dots], lag_ratio=0.1)
        )
        self.wait(0.3)
        self.play(Create(w_error), Create(a_error))  #先绘制误差条
        
        #添加组标签
        within_label = Text("非洲内部", color=BLUE, font_size=20).next_to(
            axes.c2p(1, -2), DOWN, buff=0.2).shift(UP*0.2)
        eurasia_label = Text("非洲vs欧亚", color=YELLOW, font_size=20).next_to(
            axes.c2p(2, -2), DOWN, buff=0.2).shift(UP*0.2)
        
        self.play(Write(within_label), Write(eurasia_label))
        
        #添加均值标记
        w_mean_dot = Dot(point=axes.c2p(1, w_mean), color=WHITE, radius=0.08)
        a_mean_dot = Dot(point=axes.c2p(2, a_mean), color=WHITE, radius=0.08)
        self.play(Create(w_mean_dot), Create(a_mean_dot))
        
        #执行t检验（自动处理方差齐性问题）
        t_result = stats.ttest_ind(within_africa, africa_eurasia, equal_var=False)
        
        if t_result.pvalue < 0.001:
            p_text = "p < 0.001"
        else:
            p_text = f"p = {t_result.pvalue:.3f}"

        #创建p值横线标注
        p_value_line = VGroup(
            #横线（从x=1延伸到x=2）
            Line(
                start=axes.c2p(1, 6.5),
                end=axes.c2p(2, 6.5),
                color=WHITE,
                stroke_width=1.5
            ),
            #两端短竖线
            Line(
                start=axes.c2p(1, 6.3),
                end=axes.c2p(1, 6.5),
                color=WHITE,
                stroke_width=1.5
            ),
            Line(
                start=axes.c2p(2, 6.3),
                end=axes.c2p(2, 6.5),
                color=WHITE,
                stroke_width=1.5
            ),
            #p值文本
            Text(p_text, 
                font_size=24, 
                color=YELLOW
            ).move_to(axes.c2p(1.5, 7))
        )
        
        #动画显示
        self.play(Create(p_value_line))

        #创建包含所有元素的VGroup
        all_graph_elements = VGroup(
            axes,
            x_ticks,
            y_label,
            within_dots,
            eurasia_dots,
            w_error,
            a_error,
            p_value_line,
            w_mean_dot,
            a_mean_dot,
            within_label,
            eurasia_label
        )
        
        #计算缩放和平移参数
        target_scale = 0.8  
        target_x_offset = -2.5 
        
        #创建目标位置
        all_graph_elements.generate_target()
        all_graph_elements.target.scale(target_scale)\
                      .to_edge(LEFT, buff=1.5)\
                      .shift(UP*0.2) 
        
        #动画效果 - 平滑移动和缩放
        self.play(
            MoveToTarget(all_graph_elements),
            run_time=2,
            rate_func=smooth
        )

        self.wait(2)
        
        #定义基准高度（所有终端节点在同一水平线上）
        baseline_y = -2.5
        terminal_radius = 0.3  
        
        #定义关键节点位置（初始位置设在右侧）
        initial_right_shift = 5 * RIGHT 
        positions = {
            'root': UP * 2.5 + initial_right_shift,               
            'branch1': UP * 1.5 + initial_right_shift,             
            'O': RIGHT * 3 + baseline_y * UP + initial_right_shift,
            'P1': LEFT * 3 + baseline_y * UP + initial_right_shift
        }
        
        #计算O分支的角度和长度（作为基准）
        o_branch_vector = positions['O'] - positions['branch1']
        branch_angle = np.arctan2(o_branch_vector[1], o_branch_vector[0])
        branch_length = np.linalg.norm(o_branch_vector)
        
        #计算主干方向 (branch1到P1)
        main_branch_vector = positions['P1'] - positions['branch1']
        
        #计算分支点位置 (沿主干均匀分布)
        positions['branch2'] = positions['branch1'] + main_branch_vector * 0.4
        positions['branch3'] = positions['branch1'] + main_branch_vector * 0.7
        
        #计算P3和P2位置（保持在同一水平线上且分支平行）
        delta_y = baseline_y - positions['branch2'][1]
        L_p3 = delta_y / np.sin(branch_angle)
        positions['P3'] = positions['branch2'] + L_p3 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
        
        delta_y = baseline_y - positions['branch3'][1]
        L_p2 = delta_y / np.sin(branch_angle)
        positions['P2'] = positions['branch3'] + L_p2 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
        
        #创建节点标签
        labels = {
            'root': Text("共同祖先节点", font_size=24, color=WHITE).next_to(positions['root'], UP, buff=0.1),
            'O': Text("O", font_size=24, color="#ffff7f"),
            'P1': Text("P1", font_size=24, color="#ff7f7f"),
            'P2': Text("P2", font_size=24, color="#7fff7f"),
            'P3': Text("P3", font_size=24, color="#ff7fff")
        }
        
        #创建节点圆形
        nodes = {
            'O': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#ffff7f"),
            'P1': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#ff7f7f"),
            'P2': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#7fff7f"),
            'P3': Circle(radius=terminal_radius, fill_color=BLACK, fill_opacity=1, stroke_color="#ff7fff")
        }
        
        #设置节点位置
        for key in nodes:
            nodes[key].move_to(positions[key])
            labels[key].move_to(positions[key])
        
        #创建连接线
        lines = [
            Line(positions['root'], positions['branch1'], color="#23aaff"),
            Line(positions['branch1'], positions['O'], color="#23aaff"),
            Line(positions['branch1'], positions['branch2'], color="#23aaff"),
            Line(positions['branch2'], positions['P3'], color="#23aaff"),
            Line(positions['branch2'], positions['branch3'], color="#23aaff"),
            Line(positions['branch3'], positions['P2'], color="#23aaff"),
            Line(positions['branch3'], positions['P1'], color="#23aaff")
        ]
        
        #创建等位基因标签
        allele_labels1 = VGroup(
            Text("A", font_size=24).next_to(nodes['P1'], DOWN, buff=0.3),
            Text("B", font_size=24).next_to(nodes['P2'], DOWN, buff=0.3),
            Text("B", font_size=24).next_to(nodes['P3'], DOWN, buff=0.3),
            Text("A", font_size=24).next_to(nodes['O'], DOWN, buff=0.3)
        )
        
        allele_labels2 = VGroup(
            Text("非洲", font_size=24).next_to(allele_labels1[0], DOWN, buff=0.2),
            Text("欧亚", font_size=24).next_to(allele_labels1[1], DOWN, buff=0.2),
            Text("尼安德特人", font_size=24).next_to(allele_labels1[2], DOWN, buff=0.2),
            Text("黑猩猩", font_size=24).next_to(allele_labels1[3], DOWN, buff=0.2)
        )

        #创建高亮组
        highlight_group = VGroup(
            nodes['P2'],
            nodes['P3'],
            allele_labels1[1],
            allele_labels1[2],
            allele_labels2[1],
            allele_labels2[2]
        )
        
        #创建黄框和注释
        highlight_box = SurroundingRectangle(
            highlight_group,
            color=YELLOW,
            buff=0.3,
            stroke_width=2,
            corner_radius=0.2
        )
        annotation_text = Text("共享更多等位基因", font_size=24, color=RED)
        annotation_text.next_to(highlight_box, UP, buff=0.2)
        
        #将所有元素组合并移动到右侧目标位置
        final_position = config.frame_width/4 * RIGHT 
        tree_elements = VGroup(
            *lines, *nodes.values(), *labels.values(), 
            allele_labels1, allele_labels2, highlight_box, annotation_text
        ).scale(0.6).move_to(final_position)
        
        #动画序列 - 直接在右侧创建元素
        self.play(Create(lines[0]), run_time=1)  
        self.wait(0.2)
        
        self.play(
            Create(lines[1]),  
            Create(nodes['O']),
            Write(labels['O']),
            run_time=1
        )
        self.wait(0.2)
        
        self.play(Create(lines[2]), run_time=1)  
        self.wait(0.2)
        
        self.play(
            Create(lines[3]),  
            Create(nodes['P3']),
            Write(labels['P3']),
            run_time=1
        )
        self.wait(0.2)
        
        self.play(Create(lines[4]), run_time=1)  
        self.wait(0.2)
        
        self.play(
            Create(lines[5]),  
            Create(nodes['P2']),
            Write(labels['P2']),
            run_time=1
        )
        self.wait(0.2)
        
        self.play(
            Create(lines[6]),  
            Create(nodes['P1']),
            Write(labels['P1']),
            run_time=1
        )
        self.wait(0.2)
        
        self.play(Write(labels['root']), run_time=1)  
        self.wait(0.2)
        
        self.play(LaggedStart(*[Write(l) for l in allele_labels1], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[Write(l) for l in allele_labels2], lag_ratio=0.2), run_time=1.5)
        self.wait(0.5)
        
        self.play(
            Create(highlight_box),
            Write(annotation_text),
            run_time=1.5
        )
        #第一段文字（蓝色）
        text1 = Text("与非洲人相比\n欧亚人与尼安德特人共享更多的等位基因", 
            font_size=32,
            color=BLUE,
            font="STKaiti"  
           ).to_edge(DOWN, buff=0.5)  

        #第二段文字（红色）
        text2 = Text("这提示欧亚人与尼安德特人存在混血", 
            font_size=32,
            color=RED,
            font="STKaiti"
           ).to_edge(DOWN, buff=0.5) 

        #动画序列
        self.play(Write(text1), run_time=1.5) 
        self.wait(1)
        self.play(FadeOut(text1), run_time=1)
        self.play(FadeIn(text2))  
        self.wait(2)

        all_elements = VGroup(tree_elements, all_graph_elements)

        #其他元素渐隐
        self.play(FadeOut(all_elements), run_time=1)

        final_message = Text("这提示欧亚人与尼安德特人存在混血", 
                font_size=36, 
                font="STKaiti",
                color=RED)

        #文字出现并移动到中央
        self.play(
            Transform(text2, final_message.move_to(ORIGIN)), 
            run_time=1.5
        )
        self.wait(2) 

#输入数据
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

#manim -pqh --resolution=1920,1080 test.py GeneticDistancePlot

