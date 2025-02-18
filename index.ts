import { createPublicClient, http, parseAbi } from 'viem'
import { mainnet } from 'viem/chains'

export const RANDOM_ADDRESS = '0xFDfD6DCF1FDdB00f174a36fa950Fd6946F1f2AbF'

export const client = createPublicClient({
  chain: mainnet,
  transport: http('https://happy-testnet-sepolia.rpc.caldera.xyz/http'), 
  pollingInterval: 500,
})


export const contractAbi = parseAbi([
  'function random() view returns (bytes32)',
  'function randomForTimestamp(uint256) view returns (bytes32)',
])
// console.log("blockNumber,randomValue")
// client.watchBlocks({
//   onBlock: async (block) => {
//     try {
//       const randomValue = await client.readContract({
//         address: RANDOM_ADDRESS,
//         abi: contractAbi,
//         functionName: 'random',
//       })
//       console.log(`${block.number},${randomValue.toString()}`)
//     } catch (err) {
//       console.error('Error calling random():', err)
//     }
//   },
// })
