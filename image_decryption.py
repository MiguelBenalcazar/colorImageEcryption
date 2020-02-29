import cv2 
import numpy as np
import chaos_systems as cs
import time
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import *
from tqdm import tqdm


def read_img():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    color_img = cv2.imread(root.filename)
    return color_img, root.filename


def decipher_img(color_img, h_window_size, w_window_size):
   
    b, g, r = cv2.split(color_img)
    h = color_img.shape[0]
    w = color_img.shape[1]
    h_rounds = 0
    h_res = 0
    w_rounds = 0
    w_res = 0

    initial_conditions_position = [0.01, 0.01, 1]
    initial_conditions_cipher = [0.1, 0.01, 1]
            
    db_position = 0.001
    db_cipher = 0.0001

    if h % h_window_size != 0:
        h_rounds = int(h / h_window_size) + 1
        h_res = int(h % h_window_size)
    else:
        h_rounds = int(h / h_window_size)

    if w % w_window_size != 0:
        w_rounds = int(w / w_window_size) + 1
        w_res = int(w % w_window_size)
    else:
        w_rounds = int(w / w_window_size)
    
    w_aux = 0
    h_aux = 0
    
    b_cipher = b
    g_cipher = g
    r_cipher = r

    pbar = tqdm(total= w_rounds * h_rounds)

    for i in range(w_rounds):
        w_aux = (w_window_size - w_res) if (i == w_rounds - 1 and w_res != 0) else 0
        for j in range(h_rounds):

            h_aux = (h_window_size - h_res) if (j == h_rounds - 1 and h_res != 0) else 0
            
            h_cut_start = h_window_size * j 
            h_cut_end = h_window_size * (j + 1) - h_aux
            w_cut_start = w_window_size * i - w_aux 
            w_cut_end = w_window_size * (i + 1) - w_aux

            b_aux = b[h_cut_start:h_cut_end , w_cut_start:w_cut_end]
            h_new, w_new = b_aux.shape[0], b_aux.shape[1]
            # print(h_new, w_new)
            b_aux = np.array(b_aux).reshape(1, h_new *  w_new)

            g_aux = g[h_cut_start:h_cut_end , w_cut_start:w_cut_end]
            g_aux = np.array(g_aux).reshape(1, h_new * w_new)

            r_aux = r[h_cut_start:h_cut_end , w_cut_start:w_cut_end]
            r_aux = np.array(r_aux).reshape(1, h_new * w_new)


            b_aux_cipher_process = []
            g_aux_cipher_process = []
            r_aux_cipher_process = []
            b_result_random = np.zeros((1, h_new * w_new * 8), dtype=int)
            g_result_random = np.zeros((1, h_new * w_new * 8), dtype=int)
            r_result_random = np.zeros((1, h_new * w_new * 8), dtype=int)
            b_total_subimage_cipher = []
            g_total_subimage_cipher = []
            r_total_subimage_cipher = []
            b_original_subimage = []
            g_original_subimage = []
            r_original_subimage = []


            
            b_random_position, g_random_position, r_random_position, initial_conditions_position = cs.iterator_random_position(cs.lorenz, db_position, initial_conditions_position, h_new * w_new * 8)
            b_random_cipher, g_random_cipher, r_random_cipher, initial_conditions_cipher = cs.iterator_random_cipher(cs.chenz, db_cipher, initial_conditions_cipher, h_new * w_new )
            

            for k in range(len(b_aux[0])):
                #blue
                xor = b_random_cipher[k] ^ b_aux[0][k] 
                b_total_subimage_cipher.append(xor)

                #green
                xor = g_random_cipher[k] ^ g_aux[0][k]  
                g_total_subimage_cipher.append(xor)

                #red
                xor = r_random_cipher[k] ^ r_aux[0][k] 
                r_total_subimage_cipher.append(xor)
            

            for k in range(len(b_aux[0])):
                #blue matrix
                d2b = decimal2binary(b_total_subimage_cipher[k])
                b_aux_cipher_process = np.concatenate((b_aux_cipher_process, d2b), axis=0)
                #green matrix
                d2b = decimal2binary(g_total_subimage_cipher[k])
                g_aux_cipher_process = np.concatenate((g_aux_cipher_process, d2b), axis=0)
                #red matrix
                d2b = decimal2binary(r_total_subimage_cipher[k])
                r_aux_cipher_process = np.concatenate((r_aux_cipher_process, d2b), axis=0)
            
            
            '''
                                                                       RANDOM POSITION SHUFFLING
            '''
       
            for k in range(len(b_random_position)):
                b_result_random[0][b_random_position[k]] = b_aux_cipher_process[k]
                g_result_random[0][g_random_position[k]] = g_aux_cipher_process[k]
                r_result_random[0][r_random_position[k]] = r_aux_cipher_process[k]
            
          
            b_aux_ = b_result_random[0].reshape((h_new * w_new, 8))
            g_aux_ = g_result_random[0].reshape((h_new * w_new, 8))
            r_aux_ = r_result_random[0].reshape((h_new * w_new, 8))

            for k in range(len(b_aux_)):
                #blue
                b2d = binary2decimal(b_aux_[k])
                b_original_subimage.append(b2d)
                #green
                b2d = binary2decimal(g_aux_[k])
                g_original_subimage.append(b2d)
                #red
                b2d = binary2decimal(r_aux_[k])
                r_original_subimage.append(b2d)

            b_original_subimage = np.array(b_original_subimage).reshape((h_new , w_new))
            g_original_subimage = np.array(g_original_subimage).reshape((h_new , w_new))
            r_original_subimage = np.array(r_original_subimage).reshape((h_new , w_new))

            b_cipher[h_cut_start:h_cut_end , w_cut_start:w_cut_end] = b_original_subimage
            g_cipher[h_cut_start:h_cut_end , w_cut_start:w_cut_end] = g_original_subimage
            r_cipher[h_cut_start:h_cut_end , w_cut_start:w_cut_end] = r_original_subimage
            pbar.update(1)

    original = cv2.merge((b_cipher, g_cipher, r_cipher ))
    pbar.close()
    return original, b_cipher, g_cipher, r_cipher




def decimal2binary(decimal_number):
    data = []
    data_aux = [0, 0, 0, 0, 0, 0, 0, 0]
    while decimal_number >= 2:
        data.append(int(decimal_number % 2))
        decimal_number = decimal_number / 2 
    data.append(int(decimal_number))  
    for i in range(len(data)):
        data_aux[7 - i] = data[i]
    return np.array(data_aux)


def binary2decimal(binary_number):
    data = binary_number.tolist()
    acum = 0
    for i in range(8):
        acum = acum + data[i] * 2**(7-i)
    return acum
        

def convert_image_binary_array(sub_img):
    h = sub_img.shape[0]
    w = sub_img.shape[1]
    img_arr_bin = []
    img_arr = np.array(sub_img).reshape(1, h * w)

    for i in img_arr[0]:
        img_arr_bin = np.concatenate((img_arr_bin, decimal2binary(i)), axis = 0)
    return img_arr_bin



def main():
    img, path =read_img()
    res, b_cipher, g_cipher, r_cipher = decipher_img(img, 16, 16)
    

    plt.hist(b_cipher.ravel(),256,[0,256], color='b') 
    plt.hist(g_cipher.ravel(),256,[0,256], color='g')
    plt.hist(r_cipher.ravel(),256,[0,256], color='r')
    plt.savefig(path.split('.jpg')[0] + '_hist_original.jpg')
    cv2.imwrite(path.split('.jpg')[0] + '_decipher.png', res)
    print("data has been saved, please checked it")


if __name__ == "__main__":
    main()






