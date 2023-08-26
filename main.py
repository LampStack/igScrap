import json, httpx
from urllib.parse import quote

class igScrap:

    def __init__(self) -> None:
        pass

    def userInfo(self, username:str) -> dict:
        client = httpx.Client(
        headers={
            # this is internal ID of an instegram backend app. It doesn't change often.
            "x-ig-app-id": "936619743392459",
            # use browser-like features
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            }
        )
        result = client.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            )
        data = json.loads(result.content)
        return json.dumps(data["data"]["user"], indent=2, ensure_ascii=False)
    
    def postInfo(self, url_or_shortcode:str) -> dict:
        INSTAGRAM_APP_ID = "936619743392459"  # this is the public app id for instagram.com
        if "http" in url_or_shortcode:
            shortcode = url_or_shortcode.split("/p/")[-1].split("/")[0]
        else:
            shortcode = url_or_shortcode
        variables = {
            "shortcode": shortcode,
            "child_comment_count": 20,
            "fetch_comment_count": 100,
            "parent_comment_count": 24,
            "has_threaded_comments": True,
        }
        url = "https://www.instagram.com/graphql/query/?query_hash=b3055c01b4b222b8a47dc12b090e4e64&variables="
        result = httpx.get(
            url=url + quote(json.dumps(variables)),
            headers={"x-ig-app-id": INSTAGRAM_APP_ID},
        )
        data = json.loads(result.content)
        return json.dumps(data["data"]["shortcode_media"], indent=2, ensure_ascii=False)
