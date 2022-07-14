class Event:
    type = 'type'
    event_type = 'event_type'
    contract_address = 'contract_address'
    transaction_hash = 'transaction_hash'
    log_index = 'log_index'
    block_number = 'block_number'


class EventTypes:
    swap = 'SWAP'
    mint = 'MINT'
    burn = 'BURN'
    deposit = 'DEPOSIT'
    borrow = 'BORROW'
    withdraw = 'WITHDRAW'
    repay = 'REPAY'
    liquidate = 'LIQUIDATE'


class StreamerTypes:
    events = "events"
    lending_events = "lending_events"
    trava_lp_events = "trava_lp_events"
    all = [events, lending_events, trava_lp_events]


class LendingTypes:
    ethereum = "ethereum"
    bsc = "bsc"
    ftm = "ftm"
