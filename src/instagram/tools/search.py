import requests
import json
import os

from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set default User-Agent to avoid warnings
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

class SearchTools:

    @tool('search_internet') # This is a decorator
    @staticmethod
    def search_internet(query: str) -> str:
        """
        Use this tool to search the internet for information.
        Returns 5 results from Google search engine.
        """
        return SearchTools.search(query)

    @tool('search_instagram') # This is a decorator
    @staticmethod
    def search_instagram(query: str) -> str:
        """
        Use this tool to search Instagram.
        Returns 5 results from Instagram pages.
        """
        return SearchTools.search(f"site:instagram.com {query}", limit=5)

    @tool('open_webpage')
    @staticmethod
    def open_page(url: str) -> str:
        """
        Opens a webpage and extracts its content.
        """
        loader = WebBaseLoader(url)
        try:
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        except Exception as e:
            return f"Error loading page: {str(e)}"

    @staticmethod
    def search(query, limit=5):
        """
        Performs a Google search using Serper API.
        """
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "num": limit,
        })
        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT  # Use the User-Agent to avoid errors
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        try:
            results = response.json().get('organic', [])
        except json.JSONDecodeError:
            return "Error: Unable to process search results."

        if not results:
            return "No search results found."

        output = []
        for result in results:
            output.append(f"{result['title']}\n{result['snippet']}\n{result['link']}\n")

        return f"Search results for {query}:\n\n" + "\n".join(output)

# ✅ Main script execution
if __name__ == "__main__":
    print(SearchTools.open_page.invoke("https://www.python.org/"))
