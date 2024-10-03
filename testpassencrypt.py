import numpy as np

def inversemat(matrix):
    pass

encryptionkey = np.array([[-1,0,-4,-8],
                          [2,1,1,6],
                          [5,6,0,7],
                          [-6,-6,5,-4]])

# passwordmat = np.array([[None]*4]*4)
# inp = [i for i in input('Enter Password : ')]
# inplen = len(inp)
# if inplen > 20:
#     print('no')
# else:
#     for i in range(len(passwordmat)):
#         for j in range(len(passwordmat[i])):
#             if len(inp) == 0:
#                 passwordmat[i][j] = 0
#             else:
#                 passwordmat[i][j] = inp.pop(0)
#     print(passwordmat)
    
# i = 0
# for pwrow in passwordmat:
#     for pw in pwrow:
#         if i >= inplen:
#             break
#         print(pw,end='')
#         i += 1