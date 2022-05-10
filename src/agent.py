from forta_agent import Finding, FindingType, FindingSeverity, \
    get_transaction_receipt, transaction, transaction_event, get_web3_provider

from word_cache import WordCache

EMPTY_DATA = '0x'
ZERO_VALUE = 0


def provide_handle_transaction(get_transaction_receipt):
    def handle_transaction(transaction_event):
        findings = []

        receipt = get_transaction_receipt(transaction_event.hash)

        # The contract was called. This doesn't fit
        if len(receipt.logs) > 0 :
            return findings

        # To send a message, you need to send at least a little Ether
        if receipt.transaction.value == ZERO_VALUE:
            return findings

        # empty
        if receipt.transaction.data is None or receipt.transaction.data == EMPTY_DATA:
            return findings

        text_msg = tx_data_to_text(receipt.transaction.data)

        findings.append(Finding({
            'name': 'A text message has been sent',
            'description': 'A text message was detected inside the transaction',
            'alert_id': 'forta-text-messages-agent',
            'type': FindingType.Info,
            'severity': get_severity(text_msg),
            'metadata': {
                'message': text_msg,
                'from' : receipt.transaction.from_,
                'to' : receipt.transaction.to
            }
        }))


        return findings

    return handle_transaction


def get_severity(text_msg):
    word = WordCache()

    if word.exists_assault_world(text_msg):
        return FindingSeverity.High
    else:
        return FindingSeverity.Medium


def tx_data_to_text(data):
    web3_provider = get_web3_provider()
    return web3_provider.toText(data)


real_handle_transaction = provide_handle_transaction(get_transaction_receipt)


def handle_transaction(transaction_event):
    return real_handle_transaction(transaction_event)
