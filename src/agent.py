from forta_agent import Finding, FindingType, FindingSeverity, get_web3_provider
import forta_agent


EMPTY_DATA = '0x'
ZERO_VALUE = '0x0'
words = ["you", "looser","scam", "lmao", "nitwit", "fuck","suck","fucking","cunt","bullshit",
         "bitch","gay","ass","bastard","faggot","shit","stupid","asshole","virgin","penis","exploit","exploiter",
         "exploitation","exploiter","exploiting","exploited","exploitative","exploitable","hacker","hack",
         "hacked","hacker","hacking","cheated","cheating","cheat","whale","fishing","attack","attackable","attacking","attacker","attacked", ]


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # The contract was called. This doesn't fit
    if len(transaction_event.logs) > 0:
        return findings

    # the amount of ether sent must be greater than 0
    if transaction_event.transaction is not None and transaction_event.transaction.value == 0:
        return findings

    # if more, then it is a function call in contact. we need a regular transfer of ether
    if transaction_event.traces is not None and len(transaction_event.traces) > 1:
        return findings

    # empty data
    if transaction_event.transaction.data is None or transaction_event.transaction.data == EMPTY_DATA:
        return findings

    text_msg = tx_data_to_text(transaction_event.transaction.data)

    if text_msg is None or text_msg == "":
        return findings

    findings.append(Finding({
        'name': 'A text message has been sent',
        'description': 'A text message was detected inside the transaction',
        'alert_id': 'forta-text-messages-agent',
        'type': FindingType.Info,
        'severity': get_severity(text_msg),
        'metadata': {
            'message': text_msg,
            'from': transaction_event.transaction.from_,
            'to': transaction_event.transaction.to,
            'tx_hash': transaction_event.hash,
        }
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
        return web3_provider.toText(data)
    except:
        return None
