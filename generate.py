import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

import numpy as np
import scipy.sparse as spa
import osqp
from osqp import codegen
import shutil

# ========== 1. 你的 QP 问题（按需修改） ==========
n = 3
m = 5
P = spa.csc_matrix([[4.0, 1.0, 0.0],
                    [1.0, 2.0, 0.0],
                    [0.0, 0.0, 1.0]])
q = np.array([1.0, 1.0, 0.0])
A = spa.csc_matrix([[1.0, 1.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0],
                    [0.0, 0.0, 1.0]])
l = np.array([1.0, -np.inf, -np.inf, -1.0, -np.inf])
u = np.array([1.0,   0.7 ,   0.7 , np.inf,   1.0 ])

# ========== 2. 设置并生成 ==========
m = osqp.OSQP()
m.setup(P=P, q=q, A=A, l=l, u=u,
        eps_abs=1e-4, eps_rel=1e-4, max_iter=500, verbose=False)
m.update_settings(update_rule='lu')

codegen.generate_code(
    m,
    code_dir='./qp_embedded_out',
    project_type='',
    FLOAT=True,
    LONG=False,
    EMBEDDED=2
)

# 打包，方便下载
shutil.make_archive('qp_embedded_out', 'zip', '.', 'qp_embedded_out')
print("代码已生成，打包为 qp_embedded_out.zip")
