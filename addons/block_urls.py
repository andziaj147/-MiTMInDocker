
import re
import os
from mitmproxy import http
from mitmproxy import ctx

class BlockResource:
    def __init__(self):
        # define a new list for holding all compiled regexes. Compilation is done once when the addon
        # is loaded
        self.urls = []

        url_path = "/home/mitmproxy/.mitmproxy/urls.txt"
        # read the configuration file having all string regexes
        for re_url in open(url_path):
            self.urls.append(re.compile(re_url.strip()))

        # log how many URLS we have read
        ctx.log.info(f"{len(self.urls)} urls read")

    def response(self, flow):
        # test if the request URL is matching any of the regexes
        if any(re.search(url, flow.request.url) for url in self.urls):
            ctx.log.info(f"found match for {flow.request.url}")
            flow.response = http.Response.make(
                200,  # (optional) status code
                '<html><body><img src="https://static1.makeuseofimages.com/wordpress/wp-content/uploads/2020/10/Pharming-Attack-Hacker-1.jpg"/></body></html>',
                {"Content-Type": "text/html"} 
            )

addons = [
    BlockResource()
]
