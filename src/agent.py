from forta_agent import Finding, FindingType, FindingSeverity, get_web3_provider
import forta_agent

EMPTY_DATA = '0x'
EMPTY_MESSAGE = '0x0000000000000000000000000000000000000000'
REVERTRED = 'Reverted'
ZERO_VALUE = 0
MIN_TEXT_LEN = 3
words = ["you", "looser", "scam", "lmao", "nitwit", "fuck", "suck", "fucking", "cunt", "bullshit",
         "bitch", "gay", "ass", "bastard", "faggot", "shit", "stupid", "asshole", "virgin", "penis", "exploit",
         "exploiter",
         "exploitation", "exploiter", "exploiting", "exploited", "exploitative", "exploitable", "hacker", "hack",
         "hacked", "hacker", "hacking", "cheated", "cheating", "cheat", "whale", "fishing", "attack", "attackable",
         "attacking", "attacker", "attacked", ]

ALERT_ID_FOR_HIGH = 'forta-text-messages-possible-hack'
ALERT_ID_FOR_MEDIUM = 'forta-text-messages-agent'


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # The contract was called. This doesn't fit
    if len(transaction_event.logs) > 0:
        return findings

    # if more, then it is a function call in contact. we need a regular transfer of ether
    if transaction_event.traces is not None and (len(transaction_event.traces) > 1 or
                                                 len(transaction_event.traces) > 0 and (transaction_event.traces[
                                                     0].error == REVERTRED or transaction_event.traces[0].subtraces == 1)):
        return findings

    # empty data
    if transaction_event.transaction.data is None or transaction_event.transaction.data == EMPTY_DATA or \
            transaction_event.transaction.data == EMPTY_MESSAGE:
        return findings

    text_msg = tx_data_to_text(transaction_event.transaction.data)

    if text_msg is None or text_msg == "" or len(text_msg) < MIN_TEXT_LEN:
        return findings

    severity = get_severity(text_msg)

    alert_id = ALERT_ID_FOR_MEDIUM

    findings.append(Finding({
        'name': 'A text message has been sent',
        'description': text_msg,
        'alert_id': ALERT_ID_FOR_HIGH if severity == FindingSeverity.High else ALERT_ID_FOR_MEDIUM,
        'type': FindingType.Info,
        'severity': severity,
    }))

    return findings


def get_severity(text_msg):
    for word in words:
        if word in text_msg:
            return FindingSeverity.High
        else:
            continue

    return FindingSeverity.Medium


def tx_data_to_text(data):
    try:
        web3_provider = get_web3_provider()
        return web3_provider.toText(data).strip()
    except:
        return None
