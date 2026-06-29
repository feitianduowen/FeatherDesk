""""bilibili 搜索适配器"""


def run(keyword: str):
    """在bilibili搜索关键词。

    Args:
        keyword: 搜索关键词。

    流程:
        1. 构造b站搜索结果页 URL
        2. 直接导航到结果页
    """
    query = url_quote(keyword)
    goto(f"https://search.bilibili.com/all?keyword={query}")
    log(f"Bilibili 搜索完成: {keyword}")


# Selector fallback notes for interactive search mode:
# search_input: .nav-search-input -> input[placeholder*='搜索']
# search_button: .nav-search-btn -> .search-btn
