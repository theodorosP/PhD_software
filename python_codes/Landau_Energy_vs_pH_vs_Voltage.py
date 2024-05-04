import matplotlib.pyplot as plt
import Landau_Energy

obj = Landau_Energy.fix_data( 0, 7 )
pH, V, Landau_Energy = obj.get_plotting_data()

plt.figure(figsize=(10, 6))
contour = plt.contourf(V, pH , Landau_Energy, cmap='viridis')
plt.colorbar(contour, label='eV / $\mathring{A}^2$')
plt.xlabel(r'($\Phi$ V vs SHE)')
plt.ylabel('pH')
#plt.title('?? per H(V, pH)')
#plt.savefig("Landau_Energy")
plt.show()
