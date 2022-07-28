import requests
from lnbits.extensions.scheduler.models import JobConfig
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from lnurl import Lnurl, LnurlResponse

def pay_invoice(config: JobConfig):
    print("payinvoice {config}")
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    lnurl = Lnurl(config.lnurl)
    print(f"url {lnurl.url}")
    try:
        resp = requests.get(lnurl.url, verify=False)
    except requests.exceptions.SSLError:
        print("ssl error")
        pass
    
    lnurlResp = LnurlResponse.from_dict(resp.json())
    print(lnurlResp)



    