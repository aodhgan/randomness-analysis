import { client, RANDOM_ADDRESS, contractAbi } from './setup';

async function run(){
    const blockNumber = 8366864n;
    
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

run().then(() => {
    console.log("done")
}).catch((err) => {
    console.error('Error:', err)
})

