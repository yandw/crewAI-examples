#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SerpAPI测试脚本

此脚本用于测试SerpAPI的连接状态和功能。
参考文档: https://serpapi.com/search-api
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_serpapi_direct():
    """直接使用requests库测试SerpAPI连接"""
    # 检查环境变量中是否存在SERPAPI_API_KEY
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_api_key:
        print("错误: 未找到SERPAPI_API_KEY环境变量。请在.env文件中添加您的SerpAPI密钥。")
        print("提示: 您可以在 https://serpapi.com 注册并获取API密钥。")
        return False
    
    print(f"找到SERPAPI_API_KEY: {serpapi_api_key[:5]}...{serpapi_api_key[-5:]}")
    print(f"API密钥长度: {len(serpapi_api_key)}")
    
    # 设置API请求参数
    url = "https://serpapi.com/search"
    params = {
        "q": "artificial intelligence in healthcare",
        "engine": "google",
        "api_key": serpapi_api_key,
        "gl": "us",  # 地理位置（国家）
        "hl": "en",  # 语言
        "num": 10    # 结果数量
    }
    
    # 打印请求信息
    print("\n请求信息:")
    print(f"URL: {url}")
    safe_params = params.copy()
    if "api_key" in safe_params:
        safe_params["api_key"] = f"{safe_params['api_key'][:5]}...{safe_params['api_key'][-5:]}"
    print(f"Params: {json.dumps(safe_params, indent=2)}")
    
    # 发送请求
    try:
        print("\n发送API请求...")
        response = requests.get(url, params=params)
        
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

def test_serpapi_post():
    """使用POST方法测试SerpAPI连接"""
    # 检查环境变量中是否存在SERPAPI_API_KEY
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_api_key:
        print("错误: 未找到SERPAPI_API_KEY环境变量。请在.env文件中添加您的SerpAPI密钥。")
        return False
    
    print(f"找到SERPAPI_API_KEY: {serpapi_api_key[:5]}...{serpapi_api_key[-5:]}")
    
    # 设置API请求参数
    url = "https://serpapi.com/search"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "q": "artificial intelligence in healthcare",
        "engine": "google",
        "api_key": serpapi_api_key,
        "gl": "us",
        "hl": "en",
        "num": 10
    }
    
    # 打印请求信息
    print("\n请求信息 (POST方法):")
    print(f"URL: {url}")
    safe_data = data.copy()
    if "api_key" in safe_data:
        safe_data["api_key"] = f"{safe_data['api_key'][:5]}...{safe_data['api_key'][-5:]}"
    print(f"Data: {json.dumps(safe_data, indent=2)}")
    
    # 发送请求
    try:
        print("\n发送API请求...")
        response = requests.post(url, headers=headers, json=data)
        
        # 打印响应信息
        print(f"\n响应状态码: {response.status_code}")
        
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

def main():
    """主函数"""
    print("开始测试SerpAPI...\n")
    print("=== 测试1: 直接使用GET方法测试 ===\n")
    success1 = test_serpapi_direct()
    
    print("\n\n=== 测试2: 使用POST方法测试 ===\n")
    success2 = test_serpapi_post()
    
    if success1 or success2:
        print("\n✅ SerpAPI测试成功!")
        sys.exit(0)
    else:
        print("\n❌ SerpAPI测试失败!")
        print("\n可能的原因:")
        print("1. API密钥未设置或无效")
        print("2. API使用配额已用尽")
        print("3. API服务暂时不可用")
        print("\n建议:")
        print("1. 访问 https://serpapi.com 注册并获取API密钥")
        print("2. 在.env文件中添加 SERPAPI_API_KEY=your-api-key")
        print("3. 检查API密钥是否正确")
        print("4. 查看SerpAPI账户状态和使用配额")
        sys.exit(1)

if __name__ == "__main__":
    main()