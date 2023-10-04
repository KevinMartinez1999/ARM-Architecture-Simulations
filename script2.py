import multiprocessing # Import the multiprocessing module for parallel processing
import subprocess # Import the subprocess module to run shell commands
import os # Import the os module to interact with the operating system

l3_cache = ['2MB', '4MB', '8MB', '16MB'] # Shared L3 cache size
l2_cache = ['256kB', '512kB', '1MB', '2MB'] # Unified L2 cache size
#l1d_cache = ['32kB', '64kB', '128kB', '256kB'] # L1 data cache size
#l1i_cache = ['32kB', '64kB', '128kB', '256kB'] # L1 instruction cache size
#fetch_width = ['2', '4', '8', '16'] # CPU fetch width
decode_width = ['2', '4', '8', '16'] # CPU decode width
ALU_per_core = ['2', '4', '8', '16'] # Number of execution units for integer ALU instructions
branch_pred = ['0', '1', '2', '10'] # Branch predictor type

def simulate_combination(i, j, k, x, y):
    # Run gem5 with the current combination of cache sizes
    command = "gem5/build/X86/gem5.opt gem5/configs/learning_gem5/part1/prueba1.py --l3_size='{}' --l2_size='{}' --decode_width='{}' --ALU_per_core='{}' --branch_pred='{}'".format(i, j, k, x, y)
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Move the stats.txt file to another directory
    dir = 'm5out/'
    for filename in os.listdir(dir):
        if filename.endswith('.txt'):
            # Copy file to another directory
            path = os.path.join(dir, filename)
            os.rename(path, 'DB_stats/sim_l3_cache={}_l2_cache={}_decode_width={}_ALU_per_core={}_branch_pred={}.txt'.format(i, j, k, x, y))

if __name__ == "__main__":
    num_cores = 4  # Set the number of CPU cores to utilize
    pool = multiprocessing.Pool(processes=num_cores) # Create a multiprocessing Pool
    # Generate all possible combinations of parameters
    parameter_combinations = [(i, j, k, x, y) for i in l3_cache for j in l2_cache for k in decode_width for x in ALU_per_core for y in branch_pred]
    pool.starmap(simulate_combination, parameter_combinations) # Execute simulations in parallel
    pool.close() # Close the pool
    pool.join() # Combine the results