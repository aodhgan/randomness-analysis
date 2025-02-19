import { client, RANDOM_ADDRESS, contractAbi } from './utils/setup';

const startBlock = 8321277 - 50000;
const endBlock = 8321277;

async function run(){
    // for each block in the range, call random() and print the result
    for (let blockNumber = BigInt(startBlock); blockNumber <= endBlock; blockNumber++) {
        try {
            const randomValue = await client.readContract({
              address: RANDOM_ADDRESS,
              abi: contractAbi,
              functionName: 'random',
              blockNumber: blockNumber,
            })
            console.log(`${blockNumber},${randomValue.toString()}`)
          } catch (err) {
            console.error('Error calling random():', err)
          }
    }
}
run().then(() => {
    console.log("done")
}).catch((err) => {
    console.error('Error:', err)
})

