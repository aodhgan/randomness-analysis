import fs from 'node:fs';
import path from 'node:path';
import { client, RANDOM_ADDRESS } from './utils/setup.js';
import { contractToAbi } from './utils/randomAbi.js';

async function runMonitor() {
    const checkpointFilePath = path.join(process.cwd(), 'checkpoint.txt');
    const checkpointsFilePath = path.join(process.cwd(), 'checkpoints.txt');
    const resultsFilePath = path.join(process.cwd(), 'randomness-results.csv');
    const missedBlocksFilePath = path.join(process.cwd(), 'missed-blocks.csv');
    
    let startBlock: bigint;
    const lastCheckpoint = fs.readFileSync(checkpointFilePath, 'utf8');
    startBlock = BigInt(lastCheckpoint.trim());
    const latestBlock = (await client.getBlock({ blockTag: 'latest' })).number;
    
    console.log(`Starting from block ${startBlock} up to ${latestBlock}`);
    
    
    let csvData = '';
    
    for (let blockNumber = startBlock; blockNumber <= latestBlock; blockNumber++) {
        try {
        const randomValue = await client.readContract({
            address: RANDOM_ADDRESS,
            abi: contractToAbi.Random,
            functionName: 'random',
            blockNumber: blockNumber
        });
        csvData += `${blockNumber},${randomValue.toString()}\n`;
        console.log(`${blockNumber},${randomValue.toString()}`);
        } catch (err) {
            console.error(`Error calling random() at block ${blockNumber}:`, err);
            try {
                fs.appendFileSync(missedBlocksFilePath, `${blockNumber}\n`);
                console.log(`Recorded missed block ${blockNumber}`);
            } catch (fsErr) {
                console.error(`Error writing to missed blocks file for block ${blockNumber}:`, fsErr);
            }
        }
    }
    
    // Append the new data to your CSV file
    fs.appendFileSync(resultsFilePath, csvData);
    
    // Update the checkpoint file to store the last block we processed
    fs.writeFileSync(checkpointFilePath, latestBlock.toString());
    fs.writeFileSync(checkpointsFilePath, `${latestBlock.toString()}\n`);

    console.log("Done.");
}

runMonitor().catch(err => {
  console.error('Error in runMonitor:', err);
});
