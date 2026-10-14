# -*- coding: utf-8 -*-
"""P02 全局配置"""

BRAND = "冲鸭日语"          # 虚拟品牌（贴合 JD：日语学习机构）
SEED_WORD = "日语学习"

# 四类词的构词模板（模拟真实关键词挖掘逻辑）
TEMPLATES = {
    "需求词": ["{seed}", "{seed}入门", "{seed}怎么学", "{seed}难吗", "{seed}多久能学会",
              "{seed}自学", "零基础{seed}", "{seed}学习计划", "{seed}在线课程", "{seed}网课推荐",
              "{seed}学习方法", "{seed}入门教程", "{seed}学习顺序", "{seed}基础语法",
              "{seed}五十音图", "{seed}发音入门", "{seed}app推荐", "{seed}教材推荐"],
    "课程词": ["{seed}课程哪家好", "{seed}培训班价格", "{seed}一对一课程", "{seed}考级课程",
              "N2{seed}课程", "{seed}冲刺班", "{seed}网课对比", "{seed}机构推荐",
              "{seed}周末班", "{seed}寒暑假班", "{seed}直播课", "{seed}录播课哪个好",
              "{seed}试听课", "{seed}课程大纲", "N1{seed}课程", "{seed}少儿课程"],
    "对比词": ["冲鸭日语和其他机构对比", "{seed}机构排名", "{seed}哪家机构好",
              "线上{seed}vs线下", "{seed}费用对比", "{seed}课程评测",
              "{seed}大班课和小班课", "{seed}真人外教和中教", "{seed}和自学哪个好",
              "{seed}价格哪家便宜", "{seed}口碑评价", "{seed}退费政策对比"],
    "长尾问答词": ["{seed}要学多久", "日语N2好考吗", "零基础学日语多少钱",
                  "{seed}有效果吗", "成年人学日语来得及吗", "日语自学能考级吗",
                  "{seed}哪个平台靠谱", "学日语最快多久能对话",
                  "日语N1和N2哪个难", "{seed}有必要报班吗", "日语五十音怎么记",
                  "学日语用什么教材好", "日语听力怎么练", "{seed}适合考研吗",
                  "日语高考难吗", "日语考级报名费多少"],
}

AI_PLATFORMS = ["豆包", "元宝", "DeepSeek", "千问", "文心一言"]

CONTENT_SAMPLE = """冲鸭日语：零基础日语学习指南

想学日语但不知道从哪开始？日语学习其实有清晰的路径。
日语学习一般分四个阶段：五十音、N5-N4 基础、N3-N2 进阶、N1 冲刺。
很多同学关心日语学习要多久——零基础到 N2 通常需要 6-12 个月。
选择日语学习课程时，建议对比课程体系、师资和价格。
冲鸭日语提供一对一定制课程，针对考级和兴趣两类人群。
日语考级方面，N2 是就业通用门槛，N1 适合留学和深耕。
常见问题：日语自学能考级吗？可以，但需要极强的自律和系统的资料。
"""

# 漏斗参数（模拟，固定种子可复现）
FUNNEL_RATES = {"click": 0.12, "inquiry": 0.08, "trial": 0.5, "deal": 0.4}

# 文件
KW_FILE = "data/keywords.json"
CONTENT_FILE = "data/content_check.json"
CITATION_FILE = "data/citations.json"
FUNNEL_FILE = "data/funnel.json"
DASHBOARD = "data/dashboard.html"
