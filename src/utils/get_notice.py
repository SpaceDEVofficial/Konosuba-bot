import re
import html
from .api_get import _request_api
class notice:

    def __init__(self):
        self.request = _request_api
    def remove_tag(self,content):
       first = content.replace("<br>","\n")
       cleanr =re.compile('<.*?>')
       cleantext = re.sub(cleanr, '', first)
       final = html.unescape(cleantext)
       return final
    async def _get_notice(self):
        api_content = await self.request(url="https://forum.nexon.com/api/v1/board/907/stickyThreads")
        #resp = self.remove_tag(content=api_content)
        return api_content
