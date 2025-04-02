import csv

def find_gaps(blocks):
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
    block_numbers = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if it exists
        for row in reader:
            block_numbers.append(int(row[0]))
    return block_numbers

# Read block numbers from file
file_path = "randomness-results.csv"
block_data = read_block_numbers_from_csv(file_path)

total_blocks = len(block_data)
missing, longest_streak, longest_streak_blocks = find_gaps(block_data)
missing_count = len(missing)
missing_percentage = (missing_count / total_blocks) * 100 if total_blocks > 0 else 0

if missing:
    print("Missing block numbers:", missing)
    print(f"Overall percentage of missed blocks: {missing_percentage:.2f}%")
    print(f"Longest streak of missing blocks: {longest_streak}")
    print(f"Longest streak block numbers: {longest_streak_blocks}")
else:
    print("No gaps found. The block numbers are strictly sequential.")
