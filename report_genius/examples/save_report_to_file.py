#!/usr/bin/env python

"""
示例脚本：生成报告并保存到本地文件

这个脚本演示如何使用Report Genius生成一份综合报告，
并将其保存到本地文件中。
"""

import os
import sys
from pathlib import Path
import datetime

# 将项目根目录添加到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.report_genius.crew import ReportGeniusCrew

# 加载环境变量
load_dotenv()


def main():
    """运行示例"""
    # 报告参数
    topic = input("请输入报告主题 (默认: 人工智能在医疗领域的应用): ") or "人工智能在医疗领域的应用"
    report_type = input("请输入报告类型 (默认: 研究报告): ") or "研究报告"
    audience = input("请输入目标受众 (默认: 医疗专业人士): ") or "医疗专业人士"
    length = input("请输入报告长度 (默认: 中等长度): ") or "中等长度"
    special_requirements = input("请输入特殊要求 (默认: 包含最新的研究进展和案例分析): ") or "包含最新的研究进展和案例分析"

    # 生成时间戳作为文件名的一部分
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 创建安全的文件名（移除特殊字符）
    safe_topic = "".join(c for c in topic if c.isalnum() or c in [' ', '_']).replace(' ', '_')
    
    # 设置输出文件名
    output_file = f"{safe_topic}_{timestamp}.md"
    output_path = Path(__file__).parent / output_file

    print(f"\n🧠 正在为'{audience}'生成关于'{topic}'的{report_type}...\n")
    print("这可能需要几分钟时间。请耐心等待。\n")

    # 创建并运行crew
    crew = ReportGeniusCrew(
        topic=topic,
        report_type=report_type,
        audience=audience,
        length=length,
        special_requirements=special_requirements
    )
    
    result = crew.run()

    # 将报告保存到文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(result))

    print(f"\n✅ 报告生成成功！完整报告已保存到 '{output_file}'。\n")
    print("报告预览:")
    print("====================")
    # 打印预览（前300个字符）
    preview = str(result)[:300] + "..." if len(str(result)) > 300 else str(result)
    print(preview)
    print("\n====================")
    print(f"完整报告已保存到 '{output_path}'")


if __name__ == "__main__":
    main()