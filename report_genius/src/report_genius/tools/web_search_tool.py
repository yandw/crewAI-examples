import os
import json
import requests
from typing import List, Optional, Any

from crewai.tools import BaseTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from pydantic import Field, ConfigDict


class WebSearchTool(BaseTool):
    """Tool for performing web searches using either Serper API or SerpAPI.
    
    This tool supports two different search APIs:
    1. Serper API (https://serper.dev) - Default option
    2. SerpAPI (https://serpapi.com) - Alternative option
    
    The tool will automatically select the API based on available API keys in environment variables.
    If both API keys are available, it will use the specified api_type or default to Serper API.
    If one API fails (e.g., returns an error), it will automatically try the other API if its key is available.
    
    Environment Variables:
        SERPER_API_KEY: API key for Serper API
        SERPAPI_API_KEY: API key for SerpAPI
    """

    name: str = "web_search"
    description: str = "Useful for searching the web for information about recent events, data, or any topic that requires up-to-date information."
    search: Optional[Any] = Field(default=None)
    api_type: str = Field(default="serper")
    serper_api_key: Optional[str] = Field(default=None)
    serpapi_api_key: Optional[str] = Field(default=None)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, api_type: str = None):
        """Initialize the web search tool.
        
        Args:
            api_type: The API to use for web search. Options: 'serper' or 'serpapi'. Defaults to 'serper'.
        """
        super().__init__()
        
        # Set API type based on available keys
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.serpapi_api_key = os.getenv("SERPAPI_API_KEY")
        
        # Determine which API to use
        if api_type:
            self.api_type = api_type
        elif self.serpapi_api_key and not self.serper_api_key:
            self.api_type = "serpapi"
        else:
            self.api_type = "serper"  # Default to Serper API
            
        # Initialize search wrapper if Serper API is selected and key is available
        if self.api_type == "serper" and self.serper_api_key:
            self.search = GoogleSerperAPIWrapper()
        else:
            self.search = None

    def _run(self, query: str) -> str:
        """Execute the web search with the given query.

        Args:
            query: The search query string.

        Returns:
            A string containing the search results or an error message if the API key is missing.
        """
        # 检查API类型和密钥
        if self.api_type == "serper":
            if not self.serper_api_key:
                # 如果没有Serper API密钥但有SerpAPI密钥，则自动切换到SerpAPI
                if self.serpapi_api_key:
                    self.api_type = "serpapi"
                    return self._run_serpapi_search(query)
                return (
                    "Error: SERPER_API_KEY not found in environment variables. "
                    "Please add your Serper API key to the .env file."
                )
            
            # 尝试使用Serper API，如果失败且有SerpAPI密钥，则尝试SerpAPI
            serper_result = self._run_serper_search(query)
            if "Error performing Serper API web search" in serper_result and self.serpapi_api_key:
                print("Serper API failed, switching to SerpAPI...")
                return self._run_serpapi_search(query)
            return serper_result
            
        elif self.api_type == "serpapi":
            if not self.serpapi_api_key:
                # 如果没有SerpAPI密钥但有Serper API密钥，则自动切换到Serper API
                if self.serper_api_key:
                    self.api_type = "serper"
                    return self._run_serper_search(query)
                return (
                    "Error: SERPAPI_API_KEY not found in environment variables. "
                    "Please add your SerpAPI key to the .env file."
                )
            return self._run_serpapi_search(query)
        else:
            return f"Error: Unsupported API type '{self.api_type}'. Use 'serper' or 'serpapi'."
    
    def _run_serper_search(self, query: str) -> str:
        """Execute search using Serper API."""
        if not self.search:
            self.search = GoogleSerperAPIWrapper()
            
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing Serper API web search: {str(e)}"
    
    def _run_serpapi_search(self, query: str) -> str:
        """Execute search using SerpAPI."""
        try:
            # 设置API请求参数
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "engine": "google",
                "api_key": self.serpapi_api_key,
                "gl": "us",  # 地理位置（国家）
                "hl": "en",  # 语言
                "num": 10    # 结果数量
            }
            
            # 发送请求
            response = requests.get(url, params=params)
            
            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                
                # 提取搜索结果
                organic_results = result.get("organic_results", [])
                if not organic_results:
                    return "No results found for the query."
                
                # 格式化结果
                formatted_results = []
                for i, res in enumerate(organic_results[:5], 1):  # 只取前5个结果
                    title = res.get("title", "No title")
                    link = res.get("link", "No link")
                    snippet = res.get("snippet", "No description")
                    formatted_results.append(f"{i}. {title}\n   URL: {link}\n   Description: {snippet}\n")
                
                return "\n".join(formatted_results)
            else:
                return f"Error performing SerpAPI web search: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error performing SerpAPI web search: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Asynchronously execute the web search.

        Args:
            query: The search query string.

        Returns:
            A string containing the search results.
        """
        # 异步方法目前只是调用同步版本
        # 这样可以确保异步和同步方法的行为一致，包括自动切换API的功能
        return self._run(query)