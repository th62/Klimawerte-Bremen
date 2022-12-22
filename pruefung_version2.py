# -*- coding: utf-8 -*-
"""
Erstellt am: 27.09.2022 um 18:19:30
@Author: T. Haberland
"""
# %% Initialisieren
import datetime
import numpy as np
import matplotlib.pyplot as plt

# %% Daten einlesen, die gewuenschten Werte selektieren und in Arrays speichern
datum_lst = []
messwerte_lst = []
KLIMAFILE = np.genfromtxt("klimadaten.csv", skip_header=1, delimiter=';', autostrip=True, usecols=(1, 13), dtype=str)
for ROW in KLIMAFILE:
    DATUM = datetime.datetime.strptime(ROW[0], "%Y%m%d").date()
    if DATUM.year not in (1945, 1946):
        datum_lst.append(DATUM)
        messwerte_lst.append(float(ROW[1]))
klimadaten_1890_2021_arr = np.asarray([datum_lst, messwerte_lst]).transpose()
klimadaten_2000_2021_arr = klimadaten_1890_2021_arr[
    (klimadaten_1890_2021_arr[:, 0].astype('datetime64[Y]').astype(int) + 1970) >= 2000]
klimadaten_2021_arr = klimadaten_2000_2021_arr[klimadaten_2000_2021_arr[:, 0] >= np.datetime64('2021-01-01')]
# %%""" Aufgabe 1 """ Plot erstellen und ausgeben
fig = plt.figure(figsize=(12, 9))
x = klimadaten_2021_arr[:, 0]
y = klimadaten_2021_arr[:, 1]
fig.suptitle("Klimadaten für das Jahr: " + str(klimadaten_2021_arr[0, 0].year) + " in Bremen")
plt.xlabel('Im Zeitraum vom ' + klimadaten_2021_arr[0, 0].strftime("%d.%m.%Y") + ' bis zum ' + klimadaten_2021_arr[
    -1, 0].strftime("%d.%m.%Y") + ' in Bremen')
plt.ylabel('Tagesmittel in Grad Celsius', color="red")
plt.plot(x, y, label='Tagesmittel in Grad Celsius', color="red")
fig.tight_layout()
fig.legend(bbox_to_anchor=(0.9, 0.9))
fig.show()
fig.savefig("Klimadaten_Bremen_2021.pdf")
# %%""" Aufgabe 2 """ Die gewuenschten Werte ermitteln und als print ausgeben
print("Die minimalste Temperatur im Jahr 2021 betrug " + str(min(klimadaten_2021_arr[:, 1])) + " Grad, gemessen am " +
      klimadaten_2021_arr[np.argmin(klimadaten_2021_arr[:, 1]), 0].strftime("%d.%m.%Y."))
print("Die höchste Temperatur im Jahr 2021 betrug " + str(max(klimadaten_2021_arr[:, 1])) + " Grad, gemessen am " +
      klimadaten_2021_arr[np.argmax(klimadaten_2021_arr[:, 1]), 0].strftime("%d.%m.%Y."))
print("Und die durchschnittliche Temparatur im Jahr 2021 betrug {0:.2f}".format(
    np.mean(klimadaten_2021_arr[:, 1])) + " Grad.")
# %% """ Aufgabe 3 """ Die gewuenschten Werte ermitteln und in Liste speichern
monat = 1
avg_monate_2021_lst = []
while monat < 13:
    avg_monate_2021_lst.append(np.mean(
        klimadaten_2021_arr[(klimadaten_2021_arr[:, 0].astype('datetime64[M]').astype(int) % 12 + 1) == monat, 1]))
    monat += 1
# %% Plot fuer die Ausgabe
fig = plt.figure(figsize=(12, 9))
fig.suptitle("Durchschnittstemperatur für jeden Monat des Jahres " + str(klimadaten_2021_arr[0, 0].year) + " in Bremen")
color1 = "tab:blue"
color2 = "red"
x = np.arange(1, 13, 1)
plt.bar(x, avg_monate_2021_lst, color=color1)
for index, data in enumerate(avg_monate_2021_lst):
    plt.text(x=index + 0.6, y=data + 0.2, s=f"{round(data, 2)}", fontsize=18, color=color2)
monate = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
plt.xticks(x, monate, color=color1)
plt.xlabel("Monate", color=color1)
plt.ylabel("Temperaturdurchschnitt", color=color2)
fig.tight_layout()
fig.show()
fig.savefig("Durchschnittstemperaturen_Monate_Bremen_" + str(klimadaten_2021_arr[0, 0].year) + ".pdf")
# %%""" Aufgabe 4 """ Die gewuenschten Werte ermitteln in Liste speichern und in Array umwandeln
avg_monate_2000_2021_lst = []
jahr = 2000
monat = 1
while jahr <= 2021:
    avg_monate_2000_2021_lst.append(np.mean(klimadaten_2000_2021_arr[(
            ((klimadaten_2000_2021_arr[:, 0].astype('datetime64[Y]').astype(int) + 1970) == jahr) & (
            (klimadaten_2000_2021_arr[:, 0].astype('datetime64[M]').astype(int) % 12 + 1) == monat)), 1]))
    if monat == 12:
        monat = 1
        jahr += 1
    else:
        monat += 1
avg_monate_2000_2021_arr = np.asarray(avg_monate_2000_2021_lst).reshape(22, 12).transpose()
# [x.year for x in klimadaten_2000_2021_arr[364:367,0]]
# %% Plot fuer die Ausgabe
fig = plt.figure(figsize=(12, 9))
fig.suptitle("Monatsdurchschnittstemperaturen für jeden Monat der Jahre 2000-2021 in Bremen")
x = np.arange(1, 13, 1)
plt.boxplot(avg_monate_2000_2021_arr.transpose())
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
           ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
plt.ylabel("Temperatur in Grad Celsius")
fig.tight_layout()
fig.show()
fig.savefig("Monatsdurchschnittstemperaturen_2000-2021_Bremen.pdf")
# %%""" Aufgabe 5 """ Werte ermitteln und in Liste speichern
avg_jahre_1890_2021_lst = []
jahr = 1890
while jahr <= 2021:
    avg_jahre_1890_2021_lst.append(np.mean(klimadaten_1890_2021_arr[(klimadaten_1890_2021_arr[:, 0].astype(
        'datetime64[Y]').astype(int) + 1970) == jahr, 1]))
    jahr += 1
    if jahr == 1945:
        jahr = 1947
# %% Plot fuer die Ausgabe der gemessenen temperaturen
fig = plt.figure(figsize=(12, 9))
fig.suptitle("Jahresdurchschnittstemperaturen für die Jahre 1890 -2021 ohne 1945/46 in Bremen")
plt.plot(avg_jahre_1890_2021_lst, label='Gemessene Temperaturen')
plt.xlabel("Zeitraum 1890 - 2021")
plt.xticks(range(0, 131, 10),
           ['1890', '1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010',
            '2021'])
plt.ylabel("Temperatur in Grad Celsius")
# %% lineare Regression ueber die gemessenen Temperaturen und als Plot drueberlegen
lr = np.polyfit(range(0, 130), avg_jahre_1890_2021_lst, 1)
plt.plot(range(0, 130), np.polyval(lr, range(0, 130)), color="r", label='Temperaturen nach linearer Regression')
fig.subplots_adjust(top=0.60)
fig.legend(bbox_to_anchor=(0.76, 0.95), ncol=2)
fig.tight_layout()
fig.show()
fig.savefig("Jahresdurchschnittstemperaturen_1890-2021_ohne_1945-46_Bremen.pdf")
