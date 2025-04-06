import numpy as mat
import skfuzzy as mantik
from skfuzzy import control as kontrol

# Giriş değişkenleri ve çıkış değişkeni tanımları
mesafe = kontrol.Antecedent(mat.arange(0, 50, 1), 'mesafe')
hiz = kontrol.Antecedent(mat.arange(0, 100, 1), 'hiz')
fren_basinci = kontrol.Consequent(mat.arange(0, 100, 1), 'fren_basinci')

# Üyelik fonksiyonları
mesafe['çok yakın'] = mantik.trimf(mesafe.universe, [0, 0, 10])
mesafe['yakın'] = mantik.trimf(mesafe.universe, [5, 15, 25])
mesafe['uzak'] = mantik.trimf(mesafe.universe, [20, 30, 40])
mesafe['çok uzak'] = mantik.trimf(mesafe.universe, [35, 50, 50])

hiz['çok yavaş'] = mantik.trapmf(hiz.universe, [0, 0, 20, 30])
hiz['yavaş'] = mantik.trapmf(hiz.universe, [20, 30, 45, 55])
hiz['hızlı'] = mantik.trapmf(hiz.universe, [45, 55, 70, 80])
hiz['çok hızlı'] = mantik.trapmf(hiz.universe, [70, 80, 100, 100])

fren_basinci['çok düşük'] = mantik.trimf(fren_basinci.universe, [0, 20, 40])
fren_basinci['düşük'] = mantik.trimf(fren_basinci.universe, [20, 40, 60])
fren_basinci['yüksek'] = mantik.trimf(fren_basinci.universe, [40, 60, 80])
fren_basinci['çok yüksek'] = mantik.trimf(fren_basinci.universe, [60, 100, 100])

# Kurallar
kural1 = kontrol.Rule(mesafe['çok yakın'] & hiz['çok yavaş'], fren_basinci['çok yüksek'])
kural2 = kontrol.Rule(mesafe['yakın'] & hiz['yavaş'], fren_basinci['çok düşük'])
kural3 = kontrol.Rule(mesafe['çok yakın'] & hiz['yavaş'], fren_basinci['çok yüksek'])
kural4 = kontrol.Rule(mesafe['yakın'] & hiz['yavaş'], fren_basinci['düşük'])
kural5 = kontrol.Rule(mesafe['uzak'] & hiz['yavaş'], fren_basinci['çok düşük'])
kural6 = kontrol.Rule(mesafe['çok yakın'] & hiz['hızlı'], fren_basinci['çok yüksek'])
kural7 = kontrol.Rule(mesafe['yakın'] & hiz['hızlı'], fren_basinci['düşük'])
kural8 = kontrol.Rule(mesafe['uzak'] & hiz['hızlı'], fren_basinci['çok düşük'])
kural9 = kontrol.Rule(mesafe['çok yakın'] & hiz['çok hızlı'], fren_basinci['çok yüksek'])
kural10 = kontrol.Rule(mesafe['yakın'] & hiz['çok hızlı'], fren_basinci['yüksek'])
kural11 = kontrol.Rule(mesafe['uzak'] & hiz['çok hızlı'], fren_basinci['düşük'])
kural12 = kontrol.Rule(mesafe['çok uzak'] & hiz['çok hızlı'], fren_basinci['çok düşük'])

# Kontrol sistemi oluşturulması
fren_kontrol = kontrol.ControlSystem([kural1, kural2, kural3, kural4, kural5, kural6, kural7, kural8, kural9, kural10, kural11, kural12])
frenleme = kontrol.ControlSystemSimulation(fren_kontrol)

# Kullanıcıdan hız ve mesafe girişi
v = int(input('Hızı gir (0-100 km/h): '))
s = int(input('Mesafeyi gir (m): '))

if v / 2 <= s:
    print("Frenin basılmasına gerek yoktur.")
else:
    frenleme.input['hiz'] = v
    frenleme.input['mesafe'] = s
    frenleme.compute()
    print("Fren basıncı:", frenleme.output['fren_basinci'])
    yeni_hiz = v - (v * frenleme.output['fren_basinci'] / 100)
    print("Yeni hız değeri:", yeni_hiz)
