//
// HACER UN PROGRMA QUE NOS PERMITA HACER OEPRACIONES CON ARRAY DE DOS DIMENSIONES
// 1. suma
// 2. Restar
// 3. Multiplicacion
// Miguel Angel Diaz Riatiga
//
#include <iostream>
#include<locale.h>

using namespace std;

//definir variables contantes
const int MaxRowsCols =100;

// variables
int n1,m1, n2, m2;
int array1[MaxRowsCols][MaxRowsCols] = {0};
int array2[MaxRowsCols][MaxRowsCols] = {0};
int arrayf[MaxRowsCols][MaxRowsCols] = {0};
int arrayf2[MaxRowsCols][MaxRowsCols] = {0};
int bucle;


// Funciones
int n,m;
int llenar(int n, int m, int arrayf[MaxRowsCols][MaxRowsCols]);
void mostrar(int n, int m, int arrayf[MaxRowsCols][MaxRowsCols]);
void suma(int n, int m, int arrayf[MaxRowsCols][MaxRowsCols], int arrayf2[MaxRowsCols][MaxRowsCols]);
void resta(int n, int m, int arrayf[MaxRowsCols][MaxRowsCols], int arrayf2[MaxRowsCols][MaxRowsCols]);
void multiplicar(int n, int m1, int m2, int arrayf[MaxRowsCols][MaxRowsCols], int arrayf2[MaxRowsCols][MaxRowsCols]);

int main() {
	//caracteres especiales de idiomas
	setlocale(LC_ALL,"");

	cout << "Desea continuar con el programa? \n--------------------------\n(1) para seguir \n(otro numero) para cerrar. \n";
	cin >> bucle;

	while (bucle == 1){
        cout << "\n";
		cout << "Menu:\n--------------------------\n(1) suma \n(2) resta \n(3) multiplicacion\n";
		cin >> bucle;

		if (bucle == 1){
			// llenar array 1
			cout << "Nota: \nPor defecto vamos a definir el mismo tamno para los dos arrays. ( es una suma) \n -------------------------\n";
			cout << "Empezaras a llenar el array 1\n";
			cout << "Filas array\n";
			cin >> n1; // numero de filas

			cout << "Columanas array\n";
			cin >> m1; // Numero de columnas

			llenar(n1,m1,array1);


			cout << "Empezaras a llenar el array 2\n";
			llenar(n1,m1,array2);

			// MOSTRAR:
			// mostar array 1
			cout << "array 1: \n";
			mostrar(n1,m1,array1);

			cout << "\n";
			// mostar array 2
			cout << "array 2: \n";
			mostrar(n1,m1,array2);

			//suma:
			cout << "suma: \n";
			suma(n1,m1,array1, array2);
		}else if( bucle == 2){
			// llenar array 1
			cout << "Nota: \nPor defecto vamos a definir el mismo tamno para los dos arrays. ( es una resta) \n -------------------------\n";
			cout << "Empezaras a llenar el array 1\n";
			cout << "Filas array\n";
			cin >> n1; // numero de filas

			cout << "Columanas array\n";
			cin >> m1; // Numero de columnas

			llenar(n1,m1,array1);


			cout << "Empezaras a llenar el array 2\n";
			llenar(n1,m1,array2);

			// MOSTRAR:
			// mostar array 1
			cout << "array 1: \n";
			mostrar(n1,m1,array1);

			cout << "\n";
			// mostar array 2
			cout << "array 2: \n";
			mostrar(n1,m1,array2);

			//suma:
			cout << "resta: \n";
			resta(n1,m1,array1, array2);

		}else if(bucle == 3){

			// llenar array 1
			cout << "Nota: \nPor defecto vamos a definir el mismo tamno de columnas del array uno para las filas del array 2. ( es una multiplicacion) \n -------------------------\n";
			cout << "Empezaras a llenar el array 1\n";
			cout << "Filas array\n";
			cin >> n1; // numero de filas

			cout << "Columanas array\n";
			cin >> m1; // Numero de columnas

			llenar(n1,m1,array1);


			cout << "Empezaras a llenar el array 2\n";
			cout << "\n Numero de filas: " <<n1;
			cout << "\n Numero de columnas: ";
			cin >> m2; // Numero de columnas
			llenar(m1,m2,array2);


			// MOSTRAR:
			// mostar array 1
			cout << "array 1: \n";
			mostrar(n1,m1,array1);

			cout << "\n";
			// mostar array 2
			cout << "array 2: \n";
			mostrar(m1,m2,array2);

			//multiplicar:
			cout << "multiplicacion: \n";
			multiplicar(n1,m1,m2,array1, array2);

		}

		// fuera de la logica...
		cout << "Desea continuar con el programa? \n--------------------------\n(1) para seguir \n(otro numero) para cerrar. \n";
		cin >> bucle;
	}

	cout << "Adios! :)";
	return 0;
}


// Funcion de llenar un vector de dos dimensiones de forma n *m
int llenar(int n, int m, int arrayf[][MaxRowsCols]){
	int num;
	for (int i=0; i<n; i++){
		for (int j=0; j<m; j++){
			cout << "\n numero en posicion ( " << i+1 << "," << j+1 <<" ): ";
			cin >> num;
			arrayf[i][j] = num ;
		}
	}
	return arrayf[MaxRowsCols][MaxRowsCols];
}



// Funcion de mostrar
void mostrar(int n, int m, int arrayf[][MaxRowsCols]){
	for (int i=0; i<n; i++){
		cout << "[";
		for (int j=0; j<m; j++){
			cout << arrayf[i][j] << " ";
		}
		cout << "] \n";
	}
}


// funcion de sumar
void suma(int n, int m, int arrayf[][MaxRowsCols], int arrayf2[][MaxRowsCols]){
	for (int i=0; i<n; i++){
		cout << "[";
		for (int j=0; j<m; j++){
			cout << arrayf[i][j]+arrayf2[i][j] << " ";
		}
		cout << "] \n";
	}
}

// funcion de resta
void resta(int n, int m, int arrayf[][MaxRowsCols], int arrayf2[][MaxRowsCols]){
	for (int i=0; i<n; i++){
		cout << "[";
		for (int j=0; j<m; j++){
			cout << arrayf[i][j]-arrayf2[i][j] << " ";
		}
		cout << "] \n";
	}
}



// funcion de multiplicacion
void multiplicar(int n, int m,int m2, int arrayf[][MaxRowsCols], int arrayf2[][MaxRowsCols]){
	int cont;
	cont =0;
	for (int i = 0; i < n; i++) {
		cout << "[";
        for (int j = 0; j < m2; j++) {
            for (int k = 0; k < m; k++) {
                cont += arrayf[i][k] * arrayf2[k][j];
            }
            cout << cont << " ";
            cont = 0;
        }
        cout << "]\n";
    }
}
