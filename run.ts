import fs from 'node:fs';
import path from 'node:path';
import { client, RANDOM_ADDRESS, contractAbi } from './index.js';

async function runMonitor() {
    // Path to the file that stores the *last block processed* (the checkpoint)
    const checkpointFilePath = path.join(process.cwd(), 'checkpoint.txt');
    
    // Path to file where you store appended results
    const resultsFilePath = path.join(process.cwd(), 'randomness-results.csv');
    
    // Read the last checkpoint; if none, pick a default block.
    let startBlock: bigint;
    const lastCheckpoint = fs.readFileSync(checkpointFilePath, 'utf8');
    startBlock = BigInt(lastCheckpoint.trim());
    const latestBlock = (await client.getBlock({ blockTag: 'latest' })).number;
    
    console.log(`Starting from block ${startBlock} up to ${latestBlock}`);
    
    // Generate data
    let csvData = '';
    
    for (let blockNumber = startBlock; blockNumber <= latestBlock; blockNumber++) {
        try {
        const randomValue = await client.readContract({
            address: RANDOM_ADDRESS,
            abi: contractAbi,
            functionName: 'random',
            blockNumber: blockNumber
        });
        csvData += `${blockNumber},${randomValue.toString()}\n`;
        console.log(`${blockNumber},${randomValue.toString()}`);
        } catch (err) {
        console.error('Error calling random():', err);
        }
    }
    
    // Append the new data to your CSV file
    fs.appendFileSync(resultsFilePath, csvData);
    
    // Update the checkpoint file to store the last block we processed
    fs.writeFileSync(checkpointFilePath, latestBlock.toString());

    console.log("Done.");
}

runMonitor().catch(err => {
  console.error('Error in runMonitor:', err);
});
