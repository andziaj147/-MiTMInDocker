import re
from mitmproxy import http
from mitmproxy import ctx

class RedirectFlow:
    
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

    def request(self,flow):
        # pretty_host takes the "Host" header of the request into account,
        # which is useful in transparent mode where we usually only have the IP
        # otherwise.
        if any(re.search(url, flow.request.pretty_host) for url in self.urls):
            flow.request.host = "mitmproxy.org"
            ctx.log.info(f"URL:{flow.request.pretty_host} redirected.") 
        

addons = [
    RedirectFlow()
]