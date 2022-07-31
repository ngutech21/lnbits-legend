from ssl import VerifyMode
from time import sleep

import httpx
from lnbits.extensions.scheduler.models import JobConfig
from lnurl import Lnurl, LnurlResponse
from lnbits.core.services import pay_invoice
from lnbits import bolt11
from loguru import logger
from typing import Final


async def pay_jobconfig_invoice(config: JobConfig):
    print(f"payinvoice {config}")
    lnurl = Lnurl(config.lnurl)
    print(f"conf {config.lnurl}  url {lnurl.url}")

    async with httpx.AsyncClient(verify=False) as client:
        resp: httpx.Response = await client.get(lnurl.url)

        AMOUNT_MSAT: Final = config.amount * 1_000
        for i in range(5):
            print(f"payment {i}")
            result = LnurlResponse.from_dict(resp.json())
            print(f"callback {result.callback}")

            # get invoice
            invoiceResp: httpx.Response = await client.get(
                f"{result.callback}?amount={AMOUNT_MSAT}"
            )
            if invoiceResp.status_code != 200:
                logger.warning("invalid request")
                continue

            json = invoiceResp.json()
            invoice = json["pr"]
            decoded: bolt11.Invoice = bolt11.decode(invoice)
            validAmount: int = decoded.amount_msat == AMOUNT_MSAT

            logger.debug(
                f"bol1.decoded {decoded.payment_hash}  {decoded.amount_msat} valid {AMOUNT_MSAT}"
            )
            if not validAmount:
                logger.warning(f"invalid amount {config}")
                continue

            print(f"invoiceresp {invoiceResp}")
            await pay_invoice(
                wallet_id=config.wallet,
                payment_request=invoice,
                description=f"payment {i}",
            )
            sleep(2)
