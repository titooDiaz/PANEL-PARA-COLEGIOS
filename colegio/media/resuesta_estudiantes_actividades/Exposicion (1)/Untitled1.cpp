//JHEIBER JHOANDRY MESA BENÍTEZ
// este programa permite realizar operaciones simples entre dos matrices

#include<iostream>
#include<locale.h>

using namespace std;

const int maxfilas=100;
const int maxcol=100;

int llenar(int sizefilas, int sizecol, int array[maxfilas][maxcol]);
int mostrar(int sizefilas, int sizecol, int array[maxfilas][maxcol]);
int suma(int sizefilas, int sizecol, int a[maxfilas][maxcol],	int b[maxfilas][maxcol],int r[maxfilas][maxcol]);
int resta(int sizefilas, int sizecol, int a[maxfilas][maxcol],	int b[maxfilas][maxcol],int r[maxfilas][maxcol]);
int multiplicacion(int sizefilas, int sizecol, int sizecomun, int a[maxfilas][maxcol],	int b[maxfilas][maxcol],int r[maxfilas][maxcol]);

int main(){

		setlocale(LC_ALL, "");

		int f,c,fm,cm, menu;



	int a[maxfilas][maxcol]={0};
	int b[maxfilas][maxcol]={0};
	int r[maxfilas][maxcol]={0};


	cout<< "\t\t\t\t Operaciones con Matrices" << endl;
	cout<< endl;
	inicio:
	cout<< "(1) sumar                (2) restar                (3) multiplicación             (0) cerrar el programa"<< endl;

	cin >> menu;

	switch(menu){

		case 0:
			cout<< "hasta luego...";
			goto fin;
			break;

		case 1:

		cout<<"Dame el tamaño de las matrices (serán del mismo tamaño)"<< endl;
		cout<< "Filas: ";
		cin>>f;
		cout<< "Columnas: ";
		cin>>c;

		cout<< "Digita el primer array: "<< endl;
		llenar(f,c,a);

		cout<< "Digita tu segundo array: "<< endl;
		llenar(f,c,b);


		cout<< "Tu primer array es: "<< endl;
		mostrar(f,c,a);

		cout<< endl<< "Tu segundo array es: "<< endl;
		mostrar(f,c,b);

		cout << endl<< "La suma de los array es: "<<endl;
		suma(f,c,a,b,r);
		mostrar(f,c,r);


		cout<< endl << "perfect!, como seguimos?" << endl;
		goto inicio;


	break;


		case 3:
			multiplicacion:
		cout<<"Dame el tamaño de tu primera matriz"<< endl;
		cout<< "Filas: ";
		cin>>f;
		cout<< "Columnas: ";
		cin>>c;

		cout<<"Dame el tamaño de tu segunda matriz"<< endl;
		cout<< "Filas: ";
		cin>>fm;
		cout<< "Columnas: ";
		cin>>cm;

		if(c!= fm){

			cout<< "El numero de columnas de tu primera matriz debe ser igual al número de filas de tu segunda matriz: "<< endl;
			goto multiplicacion;
		}

		cout<< "Digita tu primer array: "<< endl;
		llenar(f,c,a);

		cout<< "Digita tu segundo array: "<< endl;
		llenar(fm,cm,b);


		cout<< "Tu primer array es: "<< endl;
		mostrar(f,c,a);

		cout<< endl<< "Tu segundo array es: "<< endl;
		mostrar(fm,cm,b);

		cout << endl<< "La Multiplicación de los array es: "<<endl;
		// f = filas de array 1
		// cm = columnas array 2
		// c = comun
		multiplicacion(f, cm, c, a, b, r);
		mostrar(f,cm,r);

			cout<< endl << "perfect!, como seguimos?" << endl;
			goto inicio;

	break;


		case 2:

		cout<<"Dame el tamaño de las matrices (serán del mismo tamaño)."<< endl;
		cout<< "Filas: ";
		cin>>f;
		cout<< "Columnas: ";
		cin>>c;

		cout<< "Digita tu primer array: "<< endl;
		llenar(f,c,a);

		cout<< "Digita tu segundo array: "<< endl;
		llenar(f,c,b);


		cout<< "Tu primer array es: "<< endl;
		mostrar(f,c,a);

		cout<< endl<< "Tu segundo array es: "<< endl;
		mostrar(f,c,b);

		cout << endl<< "La resta de los array es: "<<endl;
		resta(f,c,a,b,r);
		mostrar(f,c,r);

		cout<< endl << "perfect!, como seguimos?" << endl;

		goto inicio;
	break;

	}
	fin:
	return 0;
}

int llenar(int sizefilas, int sizecol, int array[maxfilas][maxcol]){

	for(int i=0; i<sizefilas; i++){

		for (int j=0; j<sizecol; j++){
		cout<<endl <<  "Posición " << i+1 <<"," <<j+1<<": ";
		cin >> array[i][j];

		}

	}

	return array[maxfilas][maxcol];

}
int suma(int sizefilas, int sizecol, int a[maxfilas][maxcol],	int b[maxfilas][maxcol] ,int r[maxfilas][maxcol]){

	for(int i=0; i<sizefilas; i++){

		for (int j=0; j<sizecol; j++){

			r[i][j]=a[i][j]+b[i][j];
		}

	}

	return r[maxfilas][maxcol];

}

int resta(int sizefilas, int sizecol, int a[maxfilas][maxcol],	int b[maxfilas][maxcol],int r[maxfilas][maxcol]){

	for(int i=0; i<sizefilas; i++){

		for (int j=0; j<sizecol; j++){

			r[i][j]=a[i][j]-b[i][j];
		}

	}

	return r[maxfilas][maxcol];

}

// f = filas de array 1
// cm = columnas array 2
// c = comun
int multiplicacion(int sizefilas, int sizecol,int sizecomun, int a[maxfilas][maxcol],	int b[maxfilas][maxcol],int r[maxfilas][maxcol]){

		for(int i=0; i<sizefilas; i++){

			for (int j=0; j<sizecol; j++){

				for (int k=0; k<sizecomun; k++){

					r[i][j]=r[i][j]+(a[i][k]*b[k][j]);

				}
			}

		}

	return r[maxfilas][maxcol];

}

int mostrar(int sizefilas, int sizecol, int array[maxfilas][maxcol]){


	for(int i=0; i<sizefilas; i++){

			for(int j=0; j<sizecol; j++){

				cout << array[i][j]<< " ";
			}
			cout<< endl;
		}


		return array[maxfilas][maxcol];

}
