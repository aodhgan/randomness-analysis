import { client, RANDOM_ADDRESS } from './setup';
import { contractToAbi } from './randomAbi.js';

console.log("blockNumber,randomValue")
client.watchBlocks({
  onBlock: async (block) => {
    try {
      const randomValue = await client.readContract({
        address: RANDOM_ADDRESS,
        abi: contractToAbi.Random,
        functionName: 'random',
      })
      console.log(`${block.number},${randomValue.toString()}`)
    } catch (err) {
      console.error('Error calling random():', err)
    }
  },
})
