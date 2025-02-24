# Random Analysis
Collects values each block from Random.sol and analyses for random value uniformity.

## Usage
### Collection
Periodically runs a chron job as a workflow to call `random()` from the last recorded block in `checkpoint.txt` and records output `blockNumber, randomValue` tuples in `randomness-results.csv`.

Helpers are also provided:
- Running `tsx utils/getRandomAtBlock.ts` will get the value at a defined block (constant in file)

### Analysis
#### Setup Python env (if required)
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

#### Run missed blocks check
- `python3 analysis/checkBlockNumbers.py `

#### Run Uniformity/Quality analysis
- `python3 analysis/uniform.py <log_file_name>.csv`

#### Example Results Interpretation
With sample size 3286:
Bit Deviations
Each bit is expected to be “1” about half the time. With 𝑛 = 3286
n=3286, that means each bit should be 1 around 3286/2≈1643 times in an ideally uniform distribution.

A mean absolute deviation of 22.29 means that on average, each bit’s count of “1”s differs from 1643 by about ~22. That’s roughly 22/1643 ≈ 1.3% off from the ideal 50%. This is not a very large deviation.
The max deviation of 79 means the worst-case bit was off from 1643 by 79, i.e. about 4.8%. Still, for real-world randomness (especially if this is on-chain or system-based), this can be perfectly acceptable.