from .base_flags import Flag, BASE_FLAGS

E2E_SPECIFIC_FLAGS = [
    Flag("fuseapp.storeConfig.allowPastCreditApplication", "Allow Past Credit Application"),
    Flag("fuseapp.storeConfig.desking.signDisclosureDocument", "Sign Disclosure Document"),
    Flag("fuseapp.storeConfig.deal.remotelySigning", "Remotely Signing"),
    Flag("fuseapp.storeConfig.desking.skipCreditPullCheck", "Skip Credit Pull Check"),
    Flag("fuseapp.storeConfig.desking.mockCbcContractsGeneration", "Mock CBC Contracts Generation"),
    Flag("fuseapp.financeSource.mockHardPullCbc", "Mock Hard Pull CBC"),
]

E2E_FLAGS = BASE_FLAGS + E2E_SPECIFIC_FLAGS