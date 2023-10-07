import os
import subprocess
import multiprocessing

TYPE_OF_SIMULATION = "h264_dec"

# Escapar los caracteres "=" en los nombres de archivo
def escape_equal_sign(filename):
    return filename.replace("=", "\=")

# Ruta de las carpetas
base_dir = "database/{}".format(TYPE_OF_SIMULATION)
gem5_mcpat_dir = "gem5_mcpat"
mcpat_dir = "mcpat-master"
log_results_dir = "log_results/{}".format(TYPE_OF_SIMULATION)

def get_xml_files(stats_file):
    base_name = os.path.splitext(stats_file)[0]; s_file = escape_equal_sign(stats_file)
    config_file = "{}_config.json".format(base_name); c_file = escape_equal_sign(config_file)

    if "_stats" in c_file:
        c_file = c_file.replace("_stats", "")
    xml_output_file = "{}_config.xml".format(base_name)
    command = "python2 {}/gem5toMcPAT_cortexA76.py {}/{} {}/{} {}/ARM_A76_2.1GHz.xml".format(gem5_mcpat_dir, base_dir, s_file, base_dir, c_file, gem5_mcpat_dir)
    
    try:
        _ = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Error al ejecutar el comando: {}".format(command))
    xml_output_file = escape_equal_sign(xml_output_file)
    xml_output_file = xml_output_file.replace("_stats", "")
    command2 = "mv {} {}/xml_files/".format(xml_output_file, log_results_dir)

    try:
        _ = subprocess.run(command2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Error al mover el archivo {} a la carpeta log_results/{}/xml_files/".format(xml_output_file, TYPE_OF_SIMULATION))
    run_mcpat(base_name)

def run_mcpat(base_name):
    xml_dir = "log_results/{}/xml_files".format(TYPE_OF_SIMULATION)
    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml"):
            filename = escape_equal_sign(filename)
            base = base_name.replace("_stats", ""); base = escape_equal_sign(base)
            command = "./mcpat-master/mcpat -infile log_results/{}/xml_files/{} > log_results/{}/{}.log".format(TYPE_OF_SIMULATION, filename, TYPE_OF_SIMULATION, base)
            try:
                _ = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                print("Error al ejecutar el comando: {}".format(command))

if __name__ == "__main__":
    # Obtener la lista de archivos *_stats.txt y *_config.json
    stats_files = [file for file in os.listdir(base_dir) if file.endswith("_stats.txt")]
    config_files = [file for file in os.listdir(base_dir) if file.endswith("_config.json")]

    # Verificar si hay archivos que coinciden
    if not stats_files or not config_files:
        print("No se encontraron archivos *_stats.txt o *_config.json en la carpeta database/h2654_dec.")
        exit(1)

    # Ejecutar en paralelo
    num_cores = 4
    pool = multiprocessing.Pool(processes=num_cores)
    pool.map(get_xml_files, stats_files)
    pool.close()
    pool.join()
