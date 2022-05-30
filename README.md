# forta-text-messages-agent
Search for text messages inside transactions

## Supported Chains
- Ethereum, Optimism, BSC, Polygon, Fantom, Arbitrum, Avalanche

## Alerts
- alert id : 'forta-text-messages-possible-hack'
- Type is always set to "Info"
- Severity is "high" and alert_id "forta-text-messages-possible-hack" if input_data contains one of the keywords: 
  stolen, steal, stole, stealing, looser, scam, lmao, nitwit, fuck, suck, fucking, cunt, bullshit,
  bitch, gay, ass, bastard, faggot, shit, stupid, asshole, virgin, penis, exploit,
  exploiter, hijack, seize, robber, captor, kidnap, abduct, abductor, abducting, burglar,
  thief, kidnapper, pilferer, rogue, scoundrel, brat, yobbo, blighter, stinker,
  vermin, conman, fraud, crud, whore, hussy,exploitation, exploiter, exploiting, 
  exploited, exploitative, exploitable, hacker, hack,hacked, hacker, hacking, 
  cheated, cheating, cheat, whale, fishing, attack, attackable,attacking, attacker, attacked
 


## Test Data

The agent behaviour can be verified with the following transactions:

- 0xce1cf623814118aae3e1caaac7bb409fcdd1e48f0794e11b86500260e13d6bb4 (input_data '2018-01-15-T-04-30-14-930Z')
- 0x4989fa9d76a0f1a54236e6fb59823827ce98e063047b909308ed7552a739fef0 (input_data 'you are such a looser for making scam contracts lmao hope you burn in hell one day jeet')
