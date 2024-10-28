#Przykład otrzymania wartości wprowadzonej przy użyciu funkcji input().
wyraz=input()

#W celu poprawnego działania kodu w ramach GitHub Classroom warto dodatkowo użyć funkcję strip()
#To pozwoli na usunięcie spacji oraz innych "spacjopodobnych" znaków (tabulacja \t', przejście do nowej linii '\n' lub '\r' etc.) z "głowy" i "ogona" (lewej i prawej części wyrazu).
wyraz=wyraz.strip()

#Wydruk na ekranie (w konsoli)
print ('Ten wyraz został wprowadzony:', wyraz)
