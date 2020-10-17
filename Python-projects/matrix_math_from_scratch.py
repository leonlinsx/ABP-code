# jetbrains academy project
# matrix math without using numpy
import sys, textwrap

class MatrixCalc:
    
    def __init__(self):
        pass 
    
    def main(self):
        self.menu()
        choice = input("Your choice:").strip().lower()
        if not choice in ("0", "1", "2", "3", "4", "5", "6"):
            print("Invalid choice, pick again\n")
            self.main()
        elif choice == '0':
            sys.exit()
        elif choice == '1':
            self.matrix_add()
        elif choice == '2':
            self.matrix_mult_constant()
        elif choice == '3':
            self.matrix_mult()  
        elif choice == '4':
            self.matrix_transpose()
        elif choice == '5':
            self.matrix_det()   
        elif choice == '6':
            self.matrix_inv()                      
    
    # menu sections
    def menu(self):
        # https://www.kite.com/python/answers/how-to-properly-indent-multiline-strings-in-python
        print(textwrap.dedent("""\
                                1. Add matrices
                                2. Multiply matrix by a constant
                                3. Multiply matrices
                                4. Transpose matrix
                                5. Calculate a determinant
                                6. Inverse matrix
                                0. Exit"""))
    
    def menu_transpose(self):
        print(textwrap.dedent("""\
                                1. Main diagonal
                                2. Side diagonal
                                3. Vertical line
                                4. Horizontal line"""))
    
    # n by m matrices
    def read_dim(self, text):
        try:
            n, m = [int(i) for i in input(text).split()]
            return n, m
        except:
            print("Invalid dimension, pick again\n")
    
    # take n rows of input, separated by spaces    
    def read_elem(self, n, m):
        temp_list = []
        for i in range(n):
            temp_list.append([float(i) for i in input().split()])
        return temp_list
    
    def matrix_transpose(self):
        print("")
        self.menu_transpose()
        
        choice = input("Your choice:").strip().lower()
        if not choice in ("1", "2", "3", "4"):
            print("Invalid choice, pick again\n")
            self.matrix_transpose()
        else:
            An, Am = self.read_dim("Enter matrix size:")
            print("Enter matrix")
            A = self.read_elem(An, Am)
        if choice == '1': 
            # https://stackoverflow.com/a/52342301/13944490
            A_T = list(zip(*A))
        elif choice == '2':
            A_T = list(zip(*A))
            A_T.reverse()
            A_T = [row[::-1] for row in A_T]
        elif choice == '3':
            A_T = [row[::-1] for row in A]
        elif choice == '4':
            A_T = list(zip(*A))
            A_T = [row[::-1] for row in A_T]
            A_T = list(zip(*A_T))
        
        # another solution
        # if choice == '1':
        #     transposed = [[mat[i][j] for i in range(n_rows)] for j in range(n_cols)]
        # if choice == '2':
        #     transposed = [[mat[i][j] for i in range(n_rows - 1, -1, -1)] for j in range(n_cols - 1, -1, -1)]
        # if choice == '3':
        #     transposed = [[mat[i][j] for j in range(n_cols - 1, -1, -1)] for i in range(n_rows)]
        # if choice == '4':
        #     transposed = [[mat[i][j] for j in range(n_cols)] for i in range(n_cols - 1, -1, -1)]     
        
        print("The result is:")
        for row in A_T:
            print(*row)

        print("")
        return self.main()        
             
    def matrix_add(self):
        An, Am = self.read_dim("Enter size of first matrix:")
        print("Enter first matrix:")
        A = self.read_elem(An, Am)
        Bn, Bm = self.read_dim("Enter size of second matrix:")
        print("Enter second matrix:")
        B = self.read_elem(Bn, Bm)
        
        if An != Bn or Am != Bm:
            print("The operation cannot be performed.")
        else:
        # https://www.geeksforgeeks.org/python-program-add-two-matrices/
        # grader doesn't like numpy
        # zip(A, B) combines each row in A and B as a tuple
        # zip(*t) combines each elem in that tuple, element wise, as a tuple
        # sum then adds the elems in that tuple together
            C = [map(sum, zip(*t)) for t in zip(A, B)]
            for row in C:
                print(*row)
            
        print("")
        return self.main() 
        
    def matrix_mult_constant(self):
        An, Am = self.read_dim("Enter size of matrix:")
        print("Enter matrix:")
        A = self.read_elem(An, Am) 
        mult = float(input("Enter constant:"))
        # loop over rows an cols element wise
        B = [[mult * elem for elem in row] for row in A]
        print("The result is:")
        for row in B:
            print(*row)
        
        print("")
        return self.main()
    
    def matrix_mult(self):
        An, Am = self.read_dim("Enter size of first matrix:")
        print("Enter first matrix:")
        A = self.read_elem(An, Am)
        Bn, Bm = self.read_dim("Enter size of second matrix:")
        print("Enter second matrix:")
        B = self.read_elem(Bn, Bm)
        
        if Am != Bn:
            print("The operation cannot be performed.")
        else:
            # https://stackoverflow.com/a/10508239/13944490
            C = []
            B_T = list(zip(*B))
            for row_a in A:
                temp_row = []
                for col_b in B_T:
                    elem = sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
                    temp_row.append(elem)
                C.append(temp_row)
        print("The result is:")
        for row in C:
            print(*row)
            
        print("")
        return self.main()
    
    # define zeros and copy_matrix for help in calculating recursive determinant    
    def zeros_matrix(self, rows, cols):
        A = []
        while len(A) < rows:
            A.append([])
            while len(A[-1]) < cols:
                A[-1].append(0.0)
        return A 
    
    def copy_matrix(self, A):
        # get matrix dimensions
        rows = len(A)
        cols = len(A[0])
        
        # initialise zeros_matrix
        B = self.zeros_matrix(rows, cols)
        
        # copy values into the copy
        for i in range(rows):
            for j in range(cols):
                B[i][j] = A[i][j]
        return B 
    
    def det_recursive(self, A, det=0):
        # https://integratedmlai.com/find-the-determinant-of-a-matrix-with-pure-python-without-numpy-or-scipy/
        
        # error catch the 1x1 case
        if len(A) == 1:
            return A[0][0]
        
        # solve the 2x2 version first
        if len(A) == 2 and len(A[0]) == 2:
            val = (A[0][0] * A[1][1]) - (A[0][1] * A[1][0])
            return val 
        
        # solve for nxn recursively
        # for each column in A 
        for col in list(range(len(A))):
            # find the submatrix by first making a copy
            A_c = self.copy_matrix(A)
            # remove the first row (laplace expansion) 
            A_c = A_c[1:]
            
            # for each row in A_c
            for i in range(len(A_c)):
                # slice out (remove) the focus column's column from the copy as well (laplace expansion) 
                A_c[i] = A_c[i][:col] + A_c[i][col + 1:]
                
            # alternate signs     
            sign = (-1) ** (col % 2)
            # call it recursively
            sub_det = self.det_recursive(A_c)
            det += sign * A[0][col] * sub_det 
            
        return det
    
    def matrix_det(self):
        An, Am = self.read_dim("Enter matrix size:")
        # error catch; only square matrices have determinants
        if An != Am:
            print("Matrix has to be square, try again")
            self.matrix_det()
            
        print("Enter matrix")
        A = self.read_elem(An, Am)
        
        det = self.det_recursive(A)   
        print("The result is:")
        print("{:f}".format(det))
            
        print("")
        return self.main()
        
    def matrix_identity(self, n):
        # https://stackoverflow.com/questions/40269725/trying-to-construct-identity-matrix
        return [[0] * i + [1] + [0] * (n - i - 1) for i in range(n)]
    
    def matrix_inv(self):
        An, Am = self.read_dim("Enter matrix size:")
        # error catch; only square matrices have inverses
        if An != Am:
            print("Matrix has to be square, try again")
            self.matrix_inv()
        
        print("Enter matrix")
        A = self.read_elem(An, Am)
        
        det_A = self.det_recursive(A)
        
        # error catch; Matrix is singular with determinant zero and is not invertible
        if det_A == 0:
            print("This matrix doesn't have an inverse.")
            print("")
            return self.main()
        
        # get the length, copy of A, identity matrix, and copy of identity matrix
        n = len(A)
        A_c = self.copy_matrix(A)
        I = self.matrix_identity(n)
        I_c = self.copy_matrix(I)
        
        # create a list of the indices to slice later
        indices = list(range(n))
        # do row reduction across the diagonal to reduce the matrix
        for diag in range(n):
            # get the diagonal number, to use as a factor for reducing the other elements of the current row in A_c and I_c 
            diag_factor = 1.0 / A_c[diag][diag]
            # diag is also a reference to the row number 
            for j in range(n):
                A_c[diag][j] *= diag_factor
                I_c[diag][j] *= diag_factor
            # now need to reduce row-wise to get to reduced matrix echelon form
            # operate on all rows except the current diag reference row, which was reduced just above
            # slice out that row  
            for i in (indices[0:diag] + indices[diag + 1:]):
                # diag is also a reference to the col number 
                row_factor = A_c[i][diag]
                # reduce the A_c and I_c copy matrices
                for j in range(n):
                    A_c[i][j] -= row_factor * A_c[diag][j] 
                    I_c[i][j] -= row_factor * I_c[diag][j]    

        print("The result is:")
        for row in I_c:
            print(*row)
            
        print("")
        return self.main()
        
# initialise and call         
matrix_calc = MatrixCalc()
matrix_calc.main()        

      
