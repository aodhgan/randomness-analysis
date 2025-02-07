## Collect Data
npm i
tsx index.ts > log_file_name

## Run analysis
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python3 main.py log_file_name 

## Interpret results
With sample size 3286:
Bit Deviations
Each bit is expected to be “1” about half the time. With 𝑛 = 3286
n=3286, that means each bit should be 1 around 3286/2≈1643 times in an ideally uniform distribution.

A mean absolute deviation of 22.29 means that on average, each bit’s count of “1”s differs from 1643 by about ~22. That’s roughly 22/1643 ≈ 1.3% off from the ideal 50%. This is not a very large deviation.
The max deviation of 79 means the worst-case bit was off from 1643 by 79, i.e. about 4.8%. Still, for real-world randomness (especially if this is on-chain or system-based), this can be perfectly acceptable.