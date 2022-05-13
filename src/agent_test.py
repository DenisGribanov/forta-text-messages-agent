from unittest.mock import Mock
from forta_agent import FindingSeverity, FindingType, create_transaction_event, Transaction, TransactionEvent
from agent import provide_handle_transaction

mock_get_transaction_receipt = Mock()
handle_transaction = provide_handle_transaction(mock_get_transaction_receipt)



#2018-01-15-T-04-30-14-930Z
#https://etherscan.io/tx/0xce1cf623814118aae3e1caaac7bb409fcdd1e48f0794e11b86500260e13d6bb4
MESSAGE_1 = '0x323031382d30312d31352d542d30342d33302d31342d3933305a'

#you are such a looser for making scam contracts lmao hope you burn in hell one day jeet
#https://etherscan.io/tx/0x4989fa9d76a0f1a54236e6fb59823827ce98e063047b909308ed7552a739fef0
MESSAGE_2 = '0x796f752061726520737563682061206c6f6f73657220666f72206d616b696e67207363616d20636f6e747261637473206c6d616f20686f706520796f75206275726e20696e2068656c6c206f6e6520646179206a656574'

TX_HASH = "0x4989fa9d76a0f1a54236e6fb59823827ce98e063047b909308ed7552a739fef0"
ZERO_ETHER = "0x0"
NOT_EQUAL_TO_ZERO = "0x2bc6cb30ec2000"

#CALL CONTRACT DATA
#https://etherscan.io/tx/0xfba4c700815a9fee055889b06ec00b1b3fb89ed3c4a33a3bba2e32711c757dc0
CALL_CONTRACT_DATA ="0xe63d38ed000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000001000000000000000000000000e4c808592a4f60b09350c20151b5f17ee2437564000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000470de4df820000"

ADDRESS_TO= "0xd152f549545093347a162dce210e7293f1452150"
ADDRESS_FROM = "0x0036491206cbf7abd6ee9610b15426cf1b4a6f34"

class TestMessagesAgent:

    def test_returns_empty_findings_if_logs_not_empty(self):
        mock_get_transaction_receipt.return_value = Mock(logs=[{}])
        tx_event = create_transaction_event({})

        findings = handle_transaction(tx_event)
        print(findings)
        assert len(findings) == 0

    def test_returns_empty_findings_if_sent_zero_ether(self):

        t = Transaction({'value' : ZERO_ETHER, 'hash': TX_HASH})


        mock_get_transaction_receipt.return_value = Mock(logs=[], transaction = t)

        tx_event = create_transaction_event({})

        findings = handle_transaction(tx_event)
        print(findings)
        assert len(findings) == 0

    def test_returns_empty_findings_if_sent_empty_data(self):
        t = Transaction({'value': NOT_EQUAL_TO_ZERO, 'hash': TX_HASH})

        mock_get_transaction_receipt.return_value = Mock(logs=[], transaction=t)

        tx_event = create_transaction_event({})

        findings = handle_transaction(tx_event)
        print(findings)
        assert len(findings) == 0

    def test_returns_empty_findings_if_not_utf_data(self):
        t = Transaction({'value': NOT_EQUAL_TO_ZERO, 'hash': TX_HASH, 'data' : CALL_CONTRACT_DATA})

        mock_get_transaction_receipt.return_value = Mock(logs=[], transaction=t)

        tx_event = create_transaction_event({})

        findings = handle_transaction(tx_event)
        print(findings)
        assert len(findings) == 0

    def test_returns_severity_medium_findings(self):
        t = Transaction({'value': NOT_EQUAL_TO_ZERO,
                         'hash': TX_HASH,
                         'data' : MESSAGE_1})

        mock_get_transaction_receipt.return_value = Mock(logs=[], transaction=t)

        tx_event = create_transaction_event({})

        findings = handle_transaction(tx_event)

        assert len(findings) == 1
        finding = findings[0]
        assert finding.severity == FindingSeverity.Medium

    def test_returns_severity_high_findings(self):
        t = Transaction({'value': NOT_EQUAL_TO_ZERO,
                         'hash': TX_HASH,
                         'data' : MESSAGE_2,
                         'from' : ADDRESS_FROM,
                         'to':  ADDRESS_TO
                         })

        mock_get_transaction_receipt.return_value = Mock(logs=[], transaction=t)

        tx_event = create_transaction_event({})

        findings = handle_transaction(tx_event)

        assert len(findings) == 1
        finding = findings[0]
        assert finding.metadata['to'] == ADDRESS_TO
        assert finding.metadata['from'] == ADDRESS_FROM
        assert finding.severity == FindingSeverity.High