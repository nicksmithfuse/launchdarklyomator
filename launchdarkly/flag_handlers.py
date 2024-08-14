from .handlers.market_scan_account_handler import setup_ui as market_scan_setup

FLAG_HANDLERS = {
    "fi.storeConfig.marketScan.accountNumber": market_scan_setup,
}

def get_handler(flag_key):
    return FLAG_HANDLERS.get(flag_key)