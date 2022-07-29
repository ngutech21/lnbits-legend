from time import sleep
import requests
from lnbits.extensions.scheduler.models import JobConfig
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
from lnurl import Lnurl, LnurlResponse
from lnbits.core.services import pay_invoice
from lnbits import bolt11
from loguru import logger

async def pay_jobconfig_invoice(config: JobConfig):
    amount: int = 21000
    print(f"payinvoice {config}")
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    lnurl = Lnurl(config.lnurl)
    print(f"conf {config.lnurl}  url {lnurl.url}")
    resp = requests.get(lnurl.url, verify=False)
    
    for i in range(5):
        print(f"payment {i}")
        result = LnurlResponse.from_dict(resp.json())
        print(f"callback {result.callback}")
        
        #get invoice
        invoiceResp: requests.Response = requests.get(f"{result.callback}?amount={amount}", verify=False)
        if invoiceResp.status_code != 200:
            logger.warning("invalid request")
            continue
           
            
        json = invoiceResp.json()
        invoice = json['pr']
        decoded: bolt11.Invoice = bolt11.decode(invoice)
        validAmount: int = decoded.amount_msat == amount
                
        print(f"bol1.decoded {decoded.payment_hash}  {decoded.amount_msat} valid {validAmount}")
        
        print(f"invoiceresp {invoiceResp}")
        await pay_invoice(wallet_id=config.wallet, payment_request=invoice,description=f"payment {i}")
        sleep(2)
        


