# forta-text-messages-agent
Search for text messages inside transactions

## Supported Chains
- Ethereum

## Alerts
- forta-text-messages-agent
  - Fire when a transaction contains empty logs, value > 0, input_data is not empty
  - Severity is always set to "medium" if input_data contains UTF-8 text, "high" if input_dat contains one of the keywords (e.g. hack, scam, or the word insult (the list of words is in the file assault_word.txt))
  - Type is always set to "Info"
  - description contains a "input_data" in UTF-8

## Test Data

The agent behaviour can be verified with the following transactions:

- 0xce1cf623814118aae3e1caaac7bb409fcdd1e48f0794e11b86500260e13d6bb4 (input_data '2018-01-15-T-04-30-14-930Z')
- 0x4989fa9d76a0f1a54236e6fb59823827ce98e063047b909308ed7552a739fef0 (input_data 'you are such a looser for making scam contracts lmao hope you burn in hell one day jeet')
