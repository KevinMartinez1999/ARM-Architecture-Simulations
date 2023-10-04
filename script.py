import subprocess
import os

l2_cache = ['1kB', '2kB']
l1d_cache = ['1kB', '2kB']
l1i_cache = ['1kB', '2kB']

num_fil = 17
init_col = 46
fin_col = 54

cpi = []
for i in l2_cache:
    for j in l1d_cache:
        for k in l1i_cache:
            command = "gem5/build/X86/gem5.opt gem5/configs/learning_gem5/part1/prueba1.py --l2_size='{}' --l1d_size='{}' --l1i_size='{}'".format(i, j, k)
            resultado = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            #print(resultado.stdout)

            dir = 'm5out/'
            for filename in os.listdir(dir):
                if filename.endswith('.txt'):
                    path = os.path.join(dir, filename)

                    try:
                        with open(path, 'r') as arch:
                            lines = arch.readlines()
                            if num_fil <= len(lines):
                                fila_deseada = lines[num_fil - 1]
                                data = fila_deseada[init_col - 1:fin_col]
                                cpi.append(data)
                    except FileNotFoundError:
                        print(f"No se pudo encontrar el archivo: {path}")
                    except Exception as e:
                        print(f"Error inesperado: {str(e)}")

print("CPI: ", cpi)