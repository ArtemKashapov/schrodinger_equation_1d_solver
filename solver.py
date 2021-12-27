import numpy as np, matplotlib.pyplot as plt, scipy.integrate as integrate
import warnings
import eel
warnings.filterwarnings('ignore')


class TISE:
    def __init__(self, x_min, x_max, n_point, n_sol, e_min, e_max, de, const_b=2, potential=0) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.n_point = n_point
        self.n_sol = n_sol
        self.const_b = const_b
        self.x_array = np.linspace(self.x_min, self.x_max, num=self.n_point)
        self.e_min = e_min
        self.e_max = e_max
        self.de = de
        self.potential = potential
    
    def get_pot(self, x):
        if self.potential == 1:
            return - np.exp(-x)
        elif self.potential == 2:
            return - 1 / (np.exp(x - 5) + 1)
        elif self.potential == 3:
            return - np.exp(x) / x
        elif self.potential == 4:
            return - 1 / (np.exp(x) - 1)
        elif self.potential == 5:
            return np.exp(-2 * (x - 1)) - 2 * np.exp(-(x - 1))
        elif self.potential == 6:
            return (1 - 2 * x) / x ** 2
        elif self.potential == 7:
            return - 1 / x + x
        elif self.potential == 8:
            return x ** (-12) - 2 * x ** (-6)
        elif self.potential == 9:
            return - 1 / x
        else:
            return x ** 2 / 2

    def solve(self):
        numerov = Numerov(x_min=self.x_min, x_max=self.x_max, e_min=self.e_min, e_max=self.e_max, de=self.de, const_b=self.const_b, n_sol=self.n_sol, potential=self.potential)
        try:
            self.x_array, self.psi, self.eigs = numerov.get_sol()
            self.normalize()
            return len(self.eigs)
        except:
            return 0
    
    def normalize(self):
        norm_psi = list()
        for eig_func in self.psi:
            integral = integrate.simpson(np.abs(eig_func)**2, self.x_array)
            norm_psi.append(eig_func / integral)
        self.psi = norm_psi

    def plot_pot(self):
        plt.figure(figsize=(16, 9))
        plt.plot(self.x_array, self.get_pot(self.x_array), ls='-', lw=2, c='red')
        plt.grid()
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.show()
    
    def plot_solutions(self):
        f = self.get_pot(self.x_array)
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(self.x_array, f, color="black", lw=4, ls='--')
        ax.set_xlabel("x", fontsize=14)
        ax.set_ylabel("F(x)", fontsize=14)
        ax.grid()
        ax2 = ax.twinx()
        try:
            for ind, sol in enumerate(self.psi):
                ax2.plot(self.x_array, sol, lw=4, label=f'E={self.eigs[ind]}')
            ax2.set_ylabel("$\Psi(x)$", fontsize=14)
            ax2.legend()
            plt.show()
        except:
            print('error: 2')
        

# The Numerov class implements algorithm presented in the paper (check link in the top left of the gui)
class Numerov():
    def __init__(self, x_min, x_max, e_min, e_max, de, n_point=1024, const_b=2, n_sol=4, precision=1e-6, potential=0):
        self.x_min = x_min
        self.x_max = x_max
        self.n_point = n_point
        self.const_b =const_b
        self.n_sol = n_sol
        self.x_array = np.linspace(x_min, x_max, n_point)
        self.dx = self.x_array[1] - self.x_array[0]
        self.precision = precision
        self.potential = potential

        self.e_min = e_min
        self.e_max = e_max
        self.de = de
        self.pot = TISE(x_min=x_min, x_max=x_max, n_point=n_point, n_sol=n_sol, e_min=self.e_min, e_max=self.e_max, de=self.de, const_b=const_b, potential=self.potential).get_pot(self.x_array)

        self.eps = e_min
        try:
            self.c = np.where(self.pot >= self.eps)[0][0]
            if self.c < 2:
                self.c = 2
            elif self.c > self.n_point - 2:
                self.c = self.n_point - 2
        except:
            self.c = self.n_point - 2

        self.small_a = 1e-5

    def factor(self, ind):
        return self.const_b * (self.eps - self.pot[ind])

    # Forward relation (check link in the top left of the gui)
    def forward_relation(self):
        y = np.zeros(self.c)
        y[0] = 0
        y[1] = self.small_a
        for i in range(2, self.c):
            cf = (1 + self.dx ** 2 / 12 * self.factor(i))
            y[i] = 2 * (1 - 5 * self.dx ** 2 / 12 * self.factor(i-1)) * y[i-1] - (1 + self.dx ** 2 / 12 * self.factor(i-2)) * y[i-2]
            y[i] = y[i] / cf
            gl = (y[-1] - y[-2]) / (self.dx * y[-1])
        return y, gl

    # Backward relation (check link in the top left of the gui)
    def backward_relation(self):
        y = np.zeros(self.n_point - self.c + 1)
        y[-1] = 0
        y[-2] = self.small_a
        for j in range(3, self.n_point - self.c + 2):
            i = -j
            cf = (1 + self.dx ** 2 / 12 * self.factor(i))
            y[i] = 2 * (1 - 5 * self.dx ** 2 / 12 * self.factor(i+1)) * y[i+1] - (1 + self.dx ** 2 / 12 * self.factor(i+2)) * y[i+2]
            y[i] = y[i] / cf
        y = y / np.max(y)
        gr = (y[1] - y[0]) / (self.dx * y[1])
        return y, gr

    # Algorithm according to Numerov
    def numerov_algorithm(self):
        try:
            self.c = np.where(self.pot >= self.eps)[0][0]
        except:
            self.c = self.n_point - 2
        if self.c < 2:
            self.c = 2
        yl, gl = self.forward_relation()

        yr, gr = self.backward_relation()
        yr = yr * yl[-1]
        err = gl - gr
        return np.concatenate([yl, yr[1:]]), err

    # My custom function 
    def find_eigenvalues(self):
        de0 = self.de
        self.eps = self.e_min
        loss_this = self.numerov_algorithm()[1]

        e_eig = []

        while self.eps < self.e_max and len(e_eig) < self.n_sol:
            eel.setProgress(str(100 - int((self.e_max - self.eps) / (self.e_max - self.e_min) * 100)))
            de = de0
            loss_prev = loss_this
            self.eps += de
            loss_this = self.numerov_algorithm()[1]

            if np.sign(loss_prev) != np.sign(loss_this):
                de = -de / 2
                while np.abs(de) > self.precision:
                    self.eps += de
                    loss_prev, loss_this = loss_this, self.numerov_algorithm()[1]
                    if np.sign(loss_prev) != np.sign(loss_this):
                        de = -de / 2
                if np.abs(np.abs(self.backward_relation()[1]) - np.abs(self.forward_relation()[1])) < 1.0:
                    e_eig.append(self.eps)
                de = de0
                self.eps += de
                loss_this = self.numerov_algorithm()[1]
        
        eel.setProgress(str(100))
        return e_eig

    def get_sol(self):
        eigs = self.find_eigenvalues()

        psi = list()
        for eig in eigs:
            self.eps = eig
            psi.append(self.numerov_algorithm()[0])
        return self.x_array, psi, eigs
