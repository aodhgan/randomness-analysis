import { client, RANDOM_ADDRESS } from './setup';
import { contractToAbi } from './randomAbi.js';

async function run(){
    const blockNumber = 344287n;
    
    try {
        const randomValue = await client.readContract({
            address: RANDOM_ADDRESS,
            abi: contractToAbi.Random,
            functionName: 'random',
            blockNumber: blockNumber,
        })
        console.log(`${blockNumber},${randomValue.toString()}`)
        } catch (err) {
        console.error('Error calling random():', err)
        }
}

run().then(() => {
    console.log("done")
}).catch((err) => {
    console.error('Error:', err)
})

