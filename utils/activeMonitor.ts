import { client, RANDOM_ADDRESS, contractAbi } from './setup';

console.log("blockNumber,randomValue")
client.watchBlocks({
  onBlock: async (block) => {
    try {
      const randomValue = await client.readContract({
        address: RANDOM_ADDRESS,
        abi: contractAbi,
        functionName: 'random',
      })
      console.log(`${block.number},${randomValue.toString()}`)
    } catch (err) {
      console.error('Error calling random():', err)
    }
  },
})
