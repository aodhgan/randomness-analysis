import { createPublicClient, http, parseAbi } from 'viem'
import { mainnet } from 'viem/chains'

export const RANDOM_ADDRESS = '0xFDfD6DCF1FDdB00f174a36fa950Fd6946F1f2AbF'

export const client = createPublicClient({
  chain: mainnet,
  transport: http('https://happy-testnet-sepolia.rpc.caldera.xyz/http'), 
  pollingInterval: 500,
})