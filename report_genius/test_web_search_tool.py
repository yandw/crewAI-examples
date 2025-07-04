import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入WebSearchTool
from src.report_genius.tools.web_search_tool import WebSearchTool

# 加载环境变量
load_dotenv()

def test_serper_api():
    """测试使用Serper API的网络搜索工具"""
    print("\n=== 测试 Serper API 搜索 ===")
    tool = WebSearchTool(api_type="serper")
    print(f"API类型: {tool.api_type}")
    print(f"Serper API密钥是否存在: {bool(tool.serper_api_key)}")
    
    if tool.serper_api_key:
        result = tool._run("最新的人工智能技术趋势")
        print("\n搜索结果:")
        print(result)
    else:
        print("\n警告: 未找到Serper API密钥，无法执行搜索")

def test_serpapi():
    """测试使用SerpAPI的网络搜索工具"""
    print("\n=== 测试 SerpAPI 搜索 ===")
    tool = WebSearchTool(api_type="serpapi")
    print(f"API类型: {tool.api_type}")
    print(f"SerpAPI密钥是否存在: {bool(tool.serpapi_api_key)}")
    
    if tool.serpapi_api_key:
        result = tool._run("最新的人工智能技术趋势")
        print("\n搜索结果:")
        print(result)
    else:
        print("\n警告: 未找到SerpAPI密钥，无法执行搜索")

def test_auto_select():
    """测试自动选择API类型"""
    print("\n=== 测试自动选择API类型 ===")
    tool = WebSearchTool()
    print(f"自动选择的API类型: {tool.api_type}")
    print(f"Serper API密钥是否存在: {bool(tool.serper_api_key)}")
    print(f"SerpAPI密钥是否存在: {bool(tool.serpapi_api_key)}")
    
    result = tool._run("最新的人工智能技术趋势")
    print("\n搜索结果:")
    print(result)

if __name__ == "__main__":
    # 测试Serper API
    test_serper_api()
    
    # 测试SerpAPI
    test_serpapi()
    
    # 测试自动选择
    test_auto_select()