import csv
import os

def find_gaps(blocks):
    """Find gaps in a sequence of block numbers"""
    if not blocks or len(blocks) <= 1:
        return [], 0, []
        
    missing_blocks = []
    longest_streak = 0
    current_streak = 0
    longest_streak_blocks = []
    temp_streak_blocks = []
    
    for i in range(len(blocks) - 1):
        expected_next = blocks[i] + 1
        actual_next = blocks[i + 1]
        
        if actual_next != expected_next:
            missing_range = list(range(expected_next, actual_next))
            missing_blocks.extend(missing_range)
            current_streak += len(missing_range)
            temp_streak_blocks.extend(missing_range)
            
            if current_streak > longest_streak:
                longest_streak = current_streak
                longest_streak_blocks = temp_streak_blocks.copy()
        else:
            current_streak = 0
            temp_streak_blocks = []
    
    return missing_blocks, longest_streak, longest_streak_blocks

def read_block_numbers_from_csv(file_path):
    """Read block numbers from a CSV file"""
    block_numbers = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Ensure row is not empty
                    try:
                        block_numbers.append(int(row[0]))
                    except (ValueError, IndexError):
                        # Skip header or malformed rows
                        continue
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
    return block_numbers

def read_checkpoints(file_path):
    """Read checkpoint values from the checkpoints.txt file"""
    checkpoints = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        checkpoints.append(int(line))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
    return checkpoints

def analyze_latest_checkpoint_range():
    """Analyze the latest checkpoint range"""
    checkpoints_file = "checkpoints.txt"
    checkpoints = read_checkpoints(checkpoints_file)
    
    if len(checkpoints) < 2:
        print("Not enough checkpoints to analyze a range")
        return
    
    # Get the last two checkpoints
    start_block = checkpoints[-2]
    end_block = checkpoints[-1]
    
    analyze_block_range(start_block, end_block)
    
def analyze_block_range(start_block, end_block):
    """Analyze blocks within the specified range"""
    print(f"\nAnalyzing blocks from {start_block} to {end_block}")
    
    # Read all block numbers from CSV
    file_path = "randomness-results.csv"
    all_blocks = read_block_numbers_from_csv(file_path)
    
    # Filter blocks within the range
    blocks_in_range = [block for block in all_blocks if start_block <= block <= end_block]
    blocks_in_range.sort()  # Ensure blocks are sorted
    
    if not blocks_in_range:
        print(f"No blocks found in the range {start_block} to {end_block}")
        return
    
    # Calculate stats
    expected_blocks = set(range(start_block, end_block + 1))
    actual_blocks = set(blocks_in_range)
    missing_blocks = expected_blocks - actual_blocks
    
    # Traditional gap analysis on present blocks
    gaps, longest_streak, longest_streak_blocks = find_gaps(blocks_in_range)
    
    # Print results
    print(f"Expected number of blocks: {len(expected_blocks)}")
    print(f"Actual number of blocks: {len(actual_blocks)}")
    print(f"Missing blocks: {len(missing_blocks)}")
    
    if missing_blocks:
        # Calculate missing percentage
        missing_percentage = (len(missing_blocks) / len(expected_blocks)) * 100
        print(f"Percentage of missed blocks: {missing_percentage:.2f}%")
        
        # Only display up to 20 missing blocks to keep output reasonable
        display_blocks = list(missing_blocks)[:20]
        if len(missing_blocks) > 20:
            print(f"First 20 missing blocks: {display_blocks}...")
        else:
            print(f"Missing blocks: {display_blocks}")
        
        # Longest gap info
        if longest_streak > 0:
            print(f"Longest consecutive gap: {longest_streak} blocks")
            if longest_streak_blocks:
                print(f"Longest gap range: {min(longest_streak_blocks)} to {max(longest_streak_blocks)}")
    else:
        print("No missing blocks in this range!")

if __name__ == "__main__":
    print("==== LATEST CHECKPOINT RANGE ANALYSIS ====")
    analyze_latest_checkpoint_range()