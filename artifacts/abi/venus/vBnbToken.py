VBnbToken = [
    {
        "inputs": [
            {
                "internalType": "contract ComptrollerInterface",
                "name": "comptroller_",
                "type": "address"
            },
            {
                "internalType": "contract InterestRateModel",
                "name": "interestRateModel_",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "initialExchangeRateMantissa_",
                "type": "uint256"
            },
            {"internalType": "string", "name": "name_", "type": "string"},
            {"internalType": "string", "name": "symbol_", "type": "string"},
            {"internalType": "uint8", "name": "decimals_", "type": "uint8"},
            {"internalType": "address payable", "name": "admin_", "type": "address"}
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "cashPrior",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "interestAccumulated",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "borrowIndex",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "totalBorrows",
                "type": "uint256"
            }
        ],
        "name": "AccrueInterest",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "borrowAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "accountBorrows",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "totalBorrows",
                "type": "uint256"
            }
        ],
        "name": "Borrow",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "error",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "info",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "detail",
                "type": "uint256"
            }
        ],
        "name": "Failure",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "liquidator",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "repayAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "vTokenCollateral",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "seizeTokens",
                "type": "uint256"
            }
        ],
        "name": "LiquidateBorrow",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "minter",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "mintAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "mintTokens",
                "type": "uint256"
            }
        ],
        "name": "Mint",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldAdmin",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newAdmin",
                "type": "address"
            }
        ],
        "name": "NewAdmin",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract ComptrollerInterface",
                "name": "oldComptroller",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "contract ComptrollerInterface",
                "name": "newComptroller",
                "type": "address"
            }
        ],
        "name": "NewComptroller",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract InterestRateModel",
                "name": "oldInterestRateModel",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "contract InterestRateModel",
                "name": "newInterestRateModel",
                "type": "address"
            }
        ],
        "name": "NewMarketInterestRateModel",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldPendingAdmin",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newPendingAdmin",
                "type": "address"
            }
        ],
        "name": "NewPendingAdmin",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "oldReserveFactorMantissa",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newReserveFactorMantissa",
                "type": "uint256"
            }
        ],
        "name": "NewReserveFactor",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "redeemer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "redeemAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "redeemTokens",
                "type": "uint256"
            }
        ],
        "name": "Redeem",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "payer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "repayAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "accountBorrows",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "totalBorrows",
                "type": "uint256"
            }
        ],
        "name": "RepayBorrow",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "benefactor",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "addAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newTotalReserves",
                "type": "uint256"
            }
        ],
        "name": "ReservesAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "admin",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "reduceAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newTotalReserves",
                "type": "uint256"
            }
        ],
        "name": "ReservesReduced",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {"payable": True, "stateMutability": "payable", "type": "fallback"},
    {
        "constant": False,
        "inputs": [],
        "name": "_acceptAdmin",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "reduceAmount", "type": "uint256"}],
        "name": "_reduceReserves",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract ComptrollerInterface",
                "name": "newComptroller",
                "type": "address"
            }
        ],
        "name": "_setComptroller",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract InterestRateModel",
                "name": "newInterestRateModel",
                "type": "address"
            }
        ],
        "name": "_setInterestRateModel",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "newPendingAdmin",
                "type": "address"
            }
        ],
        "name": "_setPendingAdmin",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "newReserveFactorMantissa",
                "type": "uint256"
            }
        ],
        "name": "_setReserveFactor",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "accrualBlockNumber",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "accrueInterest",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "admin",
        "outputs": [{"internalType": "address payable", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOfUnderlying",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "borrowAmount", "type": "uint256"}],
        "name": "borrow",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "borrowBalanceCurrent",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "borrowBalanceStored",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "borrowIndex",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "borrowRatePerBlock",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "comptroller",
        "outputs": [
            {
                "internalType": "contract ComptrollerInterface",
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "exchangeRateCurrent",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "exchangeRateStored",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "getAccountSnapshot",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getCash",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "contract ComptrollerInterface",
                "name": "comptroller_",
                "type": "address"
            },
            {
                "internalType": "contract InterestRateModel",
                "name": "interestRateModel_",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "initialExchangeRateMantissa_",
                "type": "uint256"
            },
            {"internalType": "string", "name": "name_", "type": "string"},
            {"internalType": "string", "name": "symbol_", "type": "string"},
            {"internalType": "uint8", "name": "decimals_", "type": "uint8"}
        ],
        "name": "initialize",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "interestRateModel",
        "outputs": [
            {
                "internalType": "contract InterestRateModel",
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isVToken",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "borrower", "type": "address"},
            {
                "internalType": "contract VToken",
                "name": "vTokenCollateral",
                "type": "address"
            }
        ],
        "name": "liquidateBorrow",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "mint",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pendingAdmin",
        "outputs": [{"internalType": "address payable", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "redeemTokens", "type": "uint256"}],
        "name": "redeem",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "redeemAmount", "type": "uint256"}],
        "name": "redeemUnderlying",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "repayBorrow",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "borrower", "type": "address"}],
        "name": "repayBorrowBehalf",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "reserveFactorMantissa",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "liquidator", "type": "address"},
            {"internalType": "address", "name": "borrower", "type": "address"},
            {"internalType": "uint256", "name": "seizeTokens", "type": "uint256"}
        ],
        "name": "seize",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "supplyRatePerBlock",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalBorrows",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "totalBorrowsCurrent",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalReserves",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "dst", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "src", "type": "address"},
            {"internalType": "address", "name": "dst", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
