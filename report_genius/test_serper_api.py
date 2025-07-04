#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Serper API测试脚本

此脚本用于测试Serper API的连接状态和功能。
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper

# 加载环境变量
load_dotenv()

def test_serper_api_direct():
    """直接使用requests库测试Serper API连接"""
    # 检查环境变量中是否存在SERPER_API_KEY
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("错误: 未找到SERPER_API_KEY环境变量。请在.env文件中添加您的Serper API密钥。")
        return False
    
    print(f"找到SERPER_API_KEY: {serper_api_key[:5]}...{serper_api_key[-5:]}")
    print(f"API密钥长度: {len(serper_api_key)}")
    
    # 设置API请求参数
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    params = {
        "q": "artificial intelligence in healthcare",
        "gl": "us",
        "hl": "en",
        "num": 10
    }
    
    # 打印请求信息
    print("\n请求信息:")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps({k: (v[:5] + '...' + v[-5:] if k == 'X-API-KEY' else v) for k, v in headers.items()}, indent=2)}")
    print(f"Params: {json.dumps(params, indent=2)}")
    
    # 发送请求
    try:
        print("\n发送API请求...")
        response = requests.get(url, headers=headers, params=params)
        
        # 打印响应信息
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {json.dumps(dict(response.headers), indent=2)}")
        
        # 检查响应状态
        if response.status_code == 200:
            print("\n请求成功!")
            result = response.json()
            print("\n搜索结果预览:")
            print(json.dumps(result, indent=2)[:500] + "..." if len(json.dumps(result, indent=2)) > 500 else json.dumps(result, indent=2))
            return True
        else:
            print(f"\n请求失败! 状态码: {response.status_code}")
            try:
                error_content = response.json()
                print(f"错误详情: {json.dumps(error_content, indent=2)}")
            except:
                print(f"错误内容: {response.text}")
            return False
    except Exception as e:
        print(f"\n发送请求时出错: {str(e)}")
        return False

def test_serper_api_langchain():
    """使用LangChain测试Serper API连接"""
    # 检查环境变量中是否存在SERPER_API_KEY
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("错误: 未找到SERPER_API_KEY环境变量。请在.env文件中添加您的Serper API密钥。")
        return False
    
    print(f"找到SERPER_API_KEY: {serper_api_key[:5]}...{serper_api_key[-5:]}")
    
    # 直接使用API密钥创建GoogleSerperAPIWrapper实例
    try:
        search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
        print("成功创建GoogleSerperAPIWrapper实例")
    except Exception as e:
        print(f"创建GoogleSerperAPIWrapper实例时出错: {str(e)}")
        return False
    
    # 测试搜索功能 - 方法1：使用run方法
    try:
        query = "artificial intelligence in healthcare"
        print(f"方法1 - 正在搜索: {query}")
        result = search.run(query)
        print("搜索成功完成!")
        print("\n搜索结果预览 (前500个字符):")
        print(result[:500] + "..." if len(result) > 500 else result)
        return True
    except Exception as e:
        print(f"方法1 - 执行搜索时出错: {str(e)}")
        print("尝试使用另一种方法...")
        
        # 测试搜索功能 - 方法2：直接使用results方法
        try:
            print(f"方法2 - 正在搜索: {query}")
            results = search.results(query)
            print("搜索成功完成!")
            print("\n搜索结果预览:")
            print(str(results)[:500] + "..." if len(str(results)) > 500 else str(results))
            return True
        except Exception as e:
            print(f"方法2 - 执行搜索时出错: {str(e)}")
            return False

def main():
    """主函数"""
    print("开始测试Serper API...\n")
    print("=== 测试1: 直接使用requests库测试 ===")
    success1 = test_serper_api_direct()
    
    print("\n\n=== 测试2: 使用LangChain测试 ===")
    success2 = test_serper_api_langchain()
    
    if success1 or success2:
        print("\n✅ Serper API测试成功!")
        sys.exit(0)
    else:
        print("\n❌ Serper API测试失败!")
        print("\n可能的原因:")
        print("1. API密钥已过期或无效")
        print("2. API使用配额已用尽")
        print("3. API服务限制了当前IP地址的访问")
        print("4. API服务暂时不可用")
        print("\n建议:")
        print("1. 检查API密钥是否正确")
        print("2. 访问 https://serper.dev 查看账户状态")
        print("3. 尝试生成新的API密钥")
        print("4. 联系Serper API支持团队")
        sys.exit(1)

if __name__ == "__main__":
    main()