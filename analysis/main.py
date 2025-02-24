#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
from scipy.stats import chi2

def main(csv_file):
    """
    Reads a CSV containing columns: blockNumber,randomValue
    Performs bit-level uniformity checks on randomValue (256-bit assumed).
    """

    df = pd.read_csv(csv_file)
    random_hex = df["randomValue"].values

    # Convert each hex string to an integer
    random_ints = [int(hval, 16) for hval in random_hex]
    n = len(random_ints)

    print(f"Loaded {n} random values from '{csv_file}'.\n")

    # ---------------------------------------------------
    # 2. Bit-Level Counts
    # ---------------------------------------------------
    num_bits = 256  # adjust if your randoms are not 256-bit
    bit_counts = np.zeros(num_bits, dtype=int)

    for val in random_ints:
        for bit_pos in range(num_bits):
            if (val >> bit_pos) & 1:
                bit_counts[bit_pos] += 1

    # bit_counts[i] tells how many times the i-th bit is '1'
    # across all random values.

    # ---------------------------------------------------
    # 3. Deviation from Expected 50%
    # ---------------------------------------------------
    expected_ones = n / 2.0
    deviations = bit_counts - expected_ones  # signed difference
    abs_devs = np.abs(deviations)

    mean_deviation = np.mean(abs_devs)
    max_deviation = np.max(abs_devs)

    print("=== Bit Deviation Summary ===")
    print(f"Mean absolute deviation from 50%: {mean_deviation:.2f}")
    print(f"Max absolute deviation from 50% : {max_deviation:.2f}\n")

    # ---------------------------------------------------
    # 4. Chi-Squared Tests (per bit)
    # ---------------------------------------------------
    # For each bit we have two categories: {0,1}.
    # Observed counts: bit_counts[i] for '1', (n - bit_counts[i]) for '0'.
    # Expected counts (if uniform): n/2 for '1', n/2 for '0'.
    # Chi-square statistic with 1 degree of freedom:
    # chi2_val = sum( (obs - exp)^2 / exp ) for obs in {bit_counts[i], n - bit_counts[i]}
    # We'll compute the p-value for each bit.

    p_values = []
    for bit_pos in range(num_bits):
        observed_1 = bit_counts[bit_pos]
        observed_0 = n - observed_1

        # Expected 1s
        expected_1 = n / 2.0
        expected_0 = n / 2.0

        # Chi-square for 2 categories (dof=1):
        chi_sq = ((observed_1 - expected_1)**2 / expected_1) + \
                 ((observed_0 - expected_0)**2 / expected_0)

        # p-value = 1 - CDF of chi-square at chi_sq, with dof=1
        # For 1 dof: p = 1 - chi2.cdf(chi_sq, df=1)
        p_val = 1.0 - chi2.cdf(chi_sq, df=1)
        p_values.append(p_val)

    # ---------------------------------------------------
    # 5. Results and Interpretation
    # ---------------------------------------------------
    p_values = np.array(p_values)
    avg_p = np.mean(p_values)
    min_p = np.min(p_values)
    max_p = np.max(p_values)

    print("=== Per-Bit Chi-Squared Test Results ===")
    print(f"Average p-value across all {num_bits} bits: {avg_p:.4f}")
    print(f"Minimum p-value among bits: {min_p:.4e}")
    print(f"Maximum p-value among bits: {max_p:.4f}")

    # If you want, you can also list bits that fail a certain p-value threshold, e.g., 0.01
    threshold = 0.01
    failing_bits = np.where(p_values < threshold)[0]
    if len(failing_bits) > 0:
        print(f"\nBits with p-value < {threshold} (indicating possible non-uniformity):")
        print(failing_bits)
    else:
        print(f"\nNo bits with p-value < {threshold} based on the chi-squared test.")

    print("\nDone.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <random_values.csv>")
        sys.exit(1)

    csv_file = sys.argv[1]
    main(csv_file)
