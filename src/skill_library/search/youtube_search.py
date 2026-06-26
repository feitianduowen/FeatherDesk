"""YouTube 搜索适配器。"""
def run(keyword: str):
    """在google搜索关键词。

    Args:
        keyword: 搜索关键词。

    流程:
        1. 构造google搜索结果页 URL
        2. 直接导航到结果页
    """
    goto(f"https://www.youtube.com/results?search_query={keyword}")
    log(f"yotube搜索完成: {keyword}")



# def run(keyword: str):
#     """在 YouTube 搜索视频。

#     Args:
#         keyword: 搜索关键词。
#     """
#     goto("https://www.youtube.com")
#     wait_for_navigation()
#     fill("input[name='search_query']", keyword)
#     click("button#search-icon-legacy")
#     wait_for_navigation()
#     log(f"YouTube 搜索完成: {keyword}")


# 选择器备选方案:
# search_input: input[name='search_query'] → #search → input[id='search']
# search_button: button#search-icon-legacy → button[aria-label='搜索']
