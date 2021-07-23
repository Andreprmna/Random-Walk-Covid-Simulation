import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

#inisialisasi ukuran ruangsimulasi
xminimal = 0
xmaksimal = 20
ymax = 20
yminimal = 0
x_ukuran = xmaksimal - xminimal
y_ukuran = ymax - yminimal
 
#inisiliasi variabel#
#asumsi iterasi untuk melakukan pemodelan
n_iterasi = 120   
 #total jumlah individu
jumlah_individu = 200 
#rasio individu yang terinfeksi    
terinfeksi = 0.05 
#waktu pemulihan 
pemulihan = 10  
#probabilitas individu bergerak   
bergerak = 0.80   
#status
belum_infect = -1
kebal = 0

#inisialisasi posisi individu
posisi_x = np.zeros((jumlah_individu,n_iterasi))
posisi_y = np.zeros((jumlah_individu,n_iterasi))



#infeksi 
individu_terinveksi = np.zeros((jumlah_individu,n_iterasi))
jumlah_infeksi=np.zeros(n_iterasi)
hari = np.arange(1,(n_iterasi+1),1)
hitung_hari=np.zeros(n_iterasi)

#fungsiuntukanimasigerakan        
def animate(j):
  p12.set_data(hitung_hari[:j+1],jumlah_infeksi[:j+1])
  for i in range (jumlah_individu):
    create['p'+str(i+1)].set_data(posisi_x[i][j],posisi_y[i][j])
    if (individu_terinveksi[i][j] > 0): 
        #memberi warna merah kepada yang individu terinfeksi
        create['p'+str(i+1)].set_color('red')
    elif (individu_terinveksi[i][j] < 0 ):
        #memberi warna biru kepada yang belum terinfeksi 
        create['p'+str(i+1)].set_color('blue')
    else:   
        #memberi warna biru untuk individu yang sudah pulih                    
        create['p'+str(i+1)].set_color('blue')
  return ((create['p'+str(k+1)] for k in range (jumlah_individu)),(p12))


#fungsi untuk melakukan update status dan juga menambahkan waktu recovery sehingga kita bisa mengidentifikasi nantinya berapa banyak jumlah pasien
def update_status(individu_terinveksi,jumlah_individu,pemulihan,j,posisi_x,posisi_y):
    for a in range(jumlah_individu):
        if individu_terinveksi[a][j]>0:
            for b in range(jumlah_individu):
                if (posisi_x[a][j] == posisi_x[b][j] and posisi_y[a][j] == posisi_y[b][j]):
                    if (individu_terinveksi[b][j]==-1) :
                        individu_terinveksi[b][j] = individu_terinveksi[b][j] + pemulihan           

                        
#program utama 
for j in range (0,n_iterasi):
    for i in range (0,jumlah_individu):
        if(j == 0): #set posisi mula mula individu 
            posisi_x[i][0] = np.random.randint(low=xminimal, high=xmaksimal) 
            posisi_y[i][0] = np.random.randint(low=xminimal, high=xmaksimal) 
            ran_infect = np.random.rand()
            #memberikan time recov kepada orang yang terkena infected diawal
            if(terinfeksi >= ran_infect): 
                individu_terinveksi[i][0] = pemulihan 
            else:
                individu_terinveksi[i][0] = belum_infect
        else:
            #tahaprecovery menuju kebal
            if(individu_terinveksi[i][j-1]>kebal): 
                individu_terinveksi[i][j]= individu_terinveksi[i][j-1]-1 
            if(individu_terinveksi[i][j-1]==belum_infect): 
                individu_terinveksi[i][j]=belum_infect
                #mencatat penyebaran virus ketika individu masih terinfeksi
            if(individu_terinveksi[i][j]>kebal): 
                jumlah_infeksi[j] = jumlah_infeksi[j] + 1
            ran_move = np.random.rand()
            if(bergerak>=ran_move):  #randommove sesuai dengan nilai probabilitas
                rand = np.random.rand()
                if rand <= 0.25:
                    posisi_x[i][j] = posisi_x[i][j-1] + 1
                    posisi_y[i][j] = posisi_y[i][j-1]
                elif rand <= 0.50:
                    posisi_x[i][j] = posisi_x[i][j-1]
                    posisi_y[i][j] = posisi_y[i][j-1] - 1
                elif rand <= 0.75:
                    posisi_x[i][j] = posisi_x[i][j-1] - 1
                    posisi_y[i][j] = posisi_y[i][j-1]
                else:
                    posisi_x[i][j] = posisi_x[i][j-1]
                    posisi_y[i][j] = posisi_y[i][j-1] + 1
            else: #jika tidak bergerak akan tetap dengan posisi sebelumnya
                posisi_x[i][j] = posisi_x[i][j-1]
                posisi_y[i][j] = posisi_y[i][j-1]
            #koreksi posisi dengan PBC
            if posisi_x[i][j] > xmaksimal:
                posisi_x[i][j] = posisi_x[i][j] - x_ukuran
            elif posisi_x[i][j] < 0:
                posisi_x[i][j] = posisi_x[i][j] + x_ukuran
            elif posisi_y[i][j] > ymax:
                posisi_y[i][j] = posisi_y[i][j] - y_ukuran
            elif posisi_y[i][j] < 0:
                posisi_y[i][j] = posisi_y[i][j] + y_ukuran

    update_status(individu_terinveksi,jumlah_individu,pemulihan,j,posisi_x,posisi_y)
    sum_terinfeksi = jumlah_infeksi[j]
    totalhari = j
    hitung_hari[j] = j
    print('Hari ke',j,sum_terinfeksi,'orang')\
    #iterasi akan stop ketika jumlah terinfeksi sudah menemukan angka 0
    if(sum_terinfeksi == 0 and j > 0): 
        break
        
print('Total Hari Kasus',totalhari)

print('paling banyak terinfeksi :', (max(jumlah_infeksi)))

#Buat figure animation
fig = plt.figure(num = 0, figsize = (15, 20))
create = dict()
ax01 = plt.subplot2grid((2, 2), (0, 0))
plt.xlabel('x')
plt.ylabel('y')
ax02 = plt.subplot2grid((2, 2), (0, 1))
plt.xlabel('Hari')
plt.ylabel('Jumlah Individu Terinveksi')

 
p12, = ax02.plot(hitung_hari,jumlah_infeksi,'-b')

for run in range (jumlah_individu):
  create['p'+str(run+1)], = ax01.plot(posisi_x[run][0],posisi_y[run][0],'o',c='b')
  if (individu_terinveksi[i][0] > 0):
        create['p'+str(run+1)], = ax01.plot(posisi_x[run][0],posisi_y[run][0],'o',c='r')
  elif (individu_terinveksi[i][0] < 0 ):
        create['p'+str(run+1)], = ax01.plot(posisi_x[run][0],posisi_y[run][0],'o',c='b')
#Animasi
anim = animation.FuncAnimation(fig, animate,frames=500, interval=250, blit=False,repeat=True)
plt.show()