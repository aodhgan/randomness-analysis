import { createPublicClient, http, parseAbi } from 'viem'
import { mainnet } from 'viem/chains'

export const RANDOM_ADDRESS = '0xd7dafcdc292906540cc3357e9fd913390256b978'

export const client = createPublicClient({
  chain: mainnet,
  transport: http('https://rpc.testnet.happy.tech/http'), 
  pollingInterval: 500,
})