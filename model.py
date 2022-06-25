import numpy as np
import cv2
import jinja2
from pycaret.classification import *

H_bin = 16
S_bin = 32
V_bin = 16

def skin_hist(img, H_bin, S_bin, V_bin):
    H_r = np.zeros(H_bin)
    H_b = np.zeros(H_bin)
    S = np.zeros(S_bin)
    V = np.zeros(V_bin)
    
    h_range = 32/H_bin
    s_range = 128/S_bin
    v_range = 256/V_bin                

    img = np.array(img)  
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    for i in range(img.shape[0]): # height
        for j in range(img.shape[1]): # width
            Cr = YCrCb[i][j][1]
            Cb = YCrCb[i][j][2]

            h = hsv[i][j][0]
            s = hsv[i][j][1]
            v = hsv[i][j][2]

            h_r_cond = (h < 16) or (h >= 240)
            h_b_cond = (h >= 154) and (h < 186)
            s_cond = (s >= 29) and (s < 157)
            CrCb_cond = (Cr >= 135) and (Cr <= 180) and (Cb >= 85) and (Cb <= 155)

            if((h_r_cond or h_b_cond) and s_cond and CrCb_cond):                 
                if(h_r_cond):
                    if(h < 16):
                        h += 256
                    h -= 240
                    H_r[int(h / h_range)] += 1
                    
                else:
                    h -= 154
                    H_b[int(h / h_range)] += 1

                s -= 29
                S[int(s / s_range)] += 1
                V[int(v / v_range)] += 1

    H = np.concatenate((H_r, H_b))
    H = H / H.sum()
    S = S / S.sum()
    V = V / V.sum()

    return H, S, V

def inference(img):
    H, S, V = skin_hist(img, H_bin, S_bin, V_bin)
    data = np.concatenate((H, S, V))
    
    h_col = ["h_bin_{}".format(i) for i in range(2*H_bin)]
    s_col = ["s_bin_{}".format(i) for i in range(S_bin)]
    v_col = ["v_bin_{}".format(i) for i in range(V_bin)]
    columns = h_col + s_col + v_col

    inference_data = pd.DataFrame(data=[data], columns=columns)
    
    saved_model = load_model('model')
    result = predict_model(saved_model, data=inference_data)
    
    return result["Label"][0]
        
        