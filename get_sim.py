import multiprocessing # Import the multiprocessing module for parallel processing
import subprocess # Import the subprocess module to run shell commands

# Define the parameters to be varied in the simulation
l3_cache = ['1MB', '2MB', '4MB', '8MB'] # Shared L3 cache size
l2_cache = ['128kB', '256kB', '512kB', '1MB'] # Unified L2 cache size
#l1d_cache = ['32kB', '64kB', '128kB', '256kB'] # L1 data cache size
#l1i_cache = ['32kB', '64kB', '128kB', '256kB'] # L1 instruction cache size
#fetch_width = ['2', '4', '8', '16'] # CPU fetch width
decode_width = [1, 2, 4, 8] # CPU decode width
num_fu_intALU = [2, 4, 8, 16] # Number of execution units for integer ALU instructions
#branch_pred = [0, 1, 2, 10] # Branch predictor type

'''
simulate_combination() runs gem5 with a specific combination of cache sizes:
    i: L3 cache size
    j: L2 cache size
    k: CPU decode width
    x: Number of execution units for integer ALU instructions
    y: Branch predictor type
'''
def simulate_combination(params):
    i, j, k, x = params
    file = (
        "l3_cache={}_"
        "l2_cache={}_"
        "decode_width={}_"
        "num_fu_intALU={}"
        .format(i, j, k, x)
    )  # Path to the new stats.txt file
    # Run gem5 with the current combination of cache sizes
    command = ""
    #command = "/home/administrador/gem5/build/ARM/gem5.fast --stats-file={}_stats.txt --json-config={}_config.json /home/administrador/Documentos/prueba/codigos/CortexA76/CortexA76.py --cmd=/home/administrador/Documentos/prueba/codigos/workloads/mp3_dec/mp3_dec '--options=-w mp3dec_outfile.wav /home/administrador/Documentos/prueba/codigos/workloads/mp3_dec/mp3dec_testfile.mp3 ' --l3_size={} --l2_size={} --decode_width={} --num_fu_intALU={}".format(file, file, i, j, k, x)
    #command = "/home/administrador/gem5/build/ARM/gem5.fast --stats-file={}_stats.txt --json-config={}_config.json /home/administrador/Documentos/prueba/codigos/CortexA76/CortexA76.py --cmd=/home/administrador/Documentos/prueba/codigos/workloads/h264_dec/h264_dec '--options=/home/administrador/Documentos/prueba/codigos/workloads/h264_dec/h264dec_testfile.264 h264dec_outfile.yuv ' --l3_size={} --l2_size={} --decode_width={} --num_fu_intALU={}".format(file, file, i, j, k, x)
    #command = "/home/administrador/gem5/build/ARM/gem5.fast --stats-file={}_stats.txt --json-config={}_config.json /home/administrador/Documentos/prueba/codigos/CortexA76/CortexA76.py --cmd=/home/administrador/Documentos/prueba/codigos/workloads/mp3_enc/mp3_enc '--options=/home/administrador/Documentos/prueba/codigos/workloads/mp3_enc/mp3enc_testfile.wav mp3enc_outfile.mp3 ' --l3_size={} --l2_size={} --decode_width={} --num_fu_intALU={}".format(file, file, i, j, k, x)
    command = "/home/administrador/gem5/build/ARM/gem5.fast --stats-file={}_stats.txt --json-config={}_config.json /home/administrador/Documentos/prueba/codigos/CortexA76/CortexA76.py --cmd=/home/administrador/Documentos/prueba/codigos/workloads/h264_enc/h264_enc '--options=/home/administrador/Documentos/prueba/codigos/workloads/h264_enc/h264enc_configfile.cfg ' --l3_size={} --l2_size={} --decode_width={} --num_fu_intALU={}".format(file, file, i, j, k, x)
    try:
        _ = subprocess.run(command, shell=True)
    except:
        print("Error in {}".format(command))
    
'''
The main() function generates all possible combinations of parameters and runs:
    simulate_combination() in parallel using the multiprocessing.Pool() method.
'''
if __name__ == "__main__":
    num_cores = 12  # Set the number of CPU cores to utilize
    manager = multiprocessing.Manager() # Create a multiprocessing Manager object
    lock = manager.Lock() # Create a lock to synchronize file access
    #lock = multiprocessing.Lock()  # Create a lock to synchronize file access
    pool = multiprocessing.Pool(processes=num_cores) # Create a multiprocessing Pool
    # Generate all possible combinations of parameters
    parameter_combinations = [
        (i, j, k, x)
        for i in l3_cache
        for j in l2_cache
        for k in decode_width
        for x in num_fu_intALU
    ]
    pool.map(simulate_combination, [params for params in parameter_combinations])
    pool.close() # Close the pool
    pool.join() # Combine the results
    print("Simulation complete! Check the m5out directory for the results.")
