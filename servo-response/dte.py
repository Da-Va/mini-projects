import argparse

import numpy as np
import matplotlib.pyplot as plt


def ARGS():
    parser = argparse.ArgumentParser()

    parser.add_argument('--resolution', default=100, type=int)

    return parser.parse_args()


def main(args):
    q_fw = 1.0
    q_bw = 1.0
    Tm, Ta = np.meshgrid(np.linspace(-1.0, 1.0, args.resolution), np.linspace(-1.0,1.0, args.resolution)) 

    fw_cond = np.sign(q_fw*Tm + Ta) == np.sign(Tm)
    bw_cond = np.sign(Tm + q_bw*Ta) == np.sign(Ta)

    Tb = Tm + Ta
    Tb *= 0
    Tb[bw_cond] = (1 - q_bw) * Ta[bw_cond]
    Tb[fw_cond] = (1 - q_fw) * Tm[fw_cond]

    plt.pcolor(Tm, Ta, -Tb + Ta + Tm)
    plt.colorbar()
    plt.xlabel('t_m')
    plt.ylabel('t_a')
    plt.show()

if __name__=='__main__':
    main(ARGS())