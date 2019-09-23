// C++ Implementation of Kosaraju's algorithm to print all SCCs 
#include <iostream> 
#include <list>
#include <string>
#include <chrono>
#include <stack>
#include <cstdlib>
#include <ctime>
#include <math.h>
#include <fstream>
using namespace std;

class Graph 
{ 
	int V; // No. of vertices 
	list<int> *adj; // An array of adjacency lists 

	// Fills Stack with vertices (in increasing order of finishing 
	// times). The top element of stack has the maximum finishing 
	// time 
	void fillOrder(int v, bool visited[], stack<int> &Stack); 

	// A recursive function to print DFS starting from v 
	void DFSUtil(int v, bool visited[]); 
public: 
	Graph(int V);
    ~Graph(void); 
	void addEdge(int v, int w); 

	// The main function that finds and prints strongly connected 
	// components 
	void printSCCs(); 

	// Function that returns reverse (or transpose) of this graph 
	Graph getTranspose(); 
}; 

Graph::Graph(int V) 
{ 
	this->V = V; 
	adj = new list<int>[V]; 
} 

Graph::~Graph(void) 
{ 
	delete[] adj; 
} 

// A recursive function to print DFS starting from v 
void Graph::DFSUtil(int v, bool visited[]) 
{ 
	// Mark the current node as visited and print it 
	visited[v] = true; 
	// cout << v << " "; 

	// Recur for all the vertices adjacent to this vertex 
	list<int>::iterator i; 
	for (i = adj[v].begin(); i != adj[v].end(); ++i) 
		if (!visited[*i]) 
			DFSUtil(*i, visited); 
} 

Graph Graph::getTranspose() 
{ 
	Graph g(V); 
	for (int v = 0; v < V; v++) 
	{ 
		// Recur for all the vertices adjacent to this vertex 
		list<int>::iterator i; 
		for(i = adj[v].begin(); i != adj[v].end(); ++i) 
		{ 
			g.adj[*i].push_back(v); 
		} 
	} 
	return g; 
} 

void Graph::addEdge(int v, int w) 
{ 
	adj[v].push_back(w); // Add w to v’s list. 
} 

void Graph::fillOrder(int v, bool visited[], stack<int> &Stack) 
{ 
	// Mark the current node as visited and print it 
	visited[v] = true; 

	// Recur for all the vertices adjacent to this vertex 
	list<int>::iterator i; 
	for(i = adj[v].begin(); i != adj[v].end(); ++i) 
		if(!visited[*i]) 
			fillOrder(*i, visited, Stack); 

	// All vertices reachable from v are processed by now, push v 
	Stack.push(v); 
} 

// The main function that finds and prints all strongly connected 
// components 
void Graph::printSCCs() 
{ 
	stack<int> Stack; 

	// Mark all the vertices as not visited (For first DFS) 
	bool *visited = new bool[V]; 
	for(int i = 0; i < V; i++) 
		visited[i] = false; 

	// Fill vertices in stack according to their finishing times 
	for(int i = 0; i < V; i++) 
		if(visited[i] == false) 
			fillOrder(i, visited, Stack); 

	// Create a reversed graph 
	Graph gr = getTranspose(); 

	// Mark all the vertices as not visited (For second DFS) 
	for(int i = 0; i < V; i++) 
		visited[i] = false; 

	// Now process all vertices in order defined by Stack 
	while (Stack.empty() == false) 
	{ 
		// Pop a vertex from stack 
		int v = Stack.top(); 
		Stack.pop(); 

		// Print Strongly connected component of the popped vertex 
		if (visited[v] == false) {   
            // cout << "\n==> ";
			gr.DFSUtil(v, visited); 
			// cout << endl; 
		} 
	} 
}

// Gera numeros aleatorios
double doubleRand() {
    return double(rand()) / (double(RAND_MAX) + 1.0);
}

// Driver program to test above functions 
int main() {
    // seed dos valores random
    srand(static_cast<unsigned int>(clock()));
    // Contador de arestas
    int edges_counter = 0;
    
    // Quantidade de possibilidades de vertices
    int n_possible_vertices = (int)atoi(getenv("VERTICES_RANGE"));
    double edges_max_p = (double)atof(getenv("EDGES_MAX_PROB"));

    cout << "VERTICES_RANGE: " << n_possible_vertices << endl;
    cout << "EDGES_MAX_PROB: " << edges_max_p << endl;
    
    // Vetor com as possibilidades de valores de vertices -> 10e1...10e10
    int vertices[n_possible_vertices];
    for (int i = 0; i < n_possible_vertices; ++i) {
        // vertices[i] = pow(10, i+1);
        vertices[i] = 10 * (i+1)*100*3;
    }

    // for (int i = 0; i < n_possible_vertices; ++i){
    //     cout << vertices[i] << endl;
    // }
    // return(0);
    
    // Arquivo de escrita
    ofstream FILE;
    FILE.open("out.txt");
    // Percorre todas as combinacoes de vertices
    for (double edge_prob = 0.1; edge_prob <= edges_max_p; edge_prob = edge_prob + 0.1){
        
        cout << "\n==================================\n" << endl;
        for (int i = 0; i < n_possible_vertices; ++i){
            // Instancia grafo
            Graph g(vertices[i]);

            cout << "Edge Probability:   " << edge_prob << endl;
            cout << "Vertices:           " << vertices[i] << endl;
            cout << "Edges:              ";
            
            for(int v1 = 0; v1 < vertices[i]; ++v1){
                for (int v2 = 0; v2 < vertices[i]; ++v2){
                    // Se o numero aleatorio for menor que edge_prob, cria aresta
                    if(doubleRand() < edge_prob){
                        // cout << v1 << " -> " << v2 << endl;
                        g.addEdge(v1, v2);
                        edges_counter++;
                    }
                }
            }
            cout << edges_counter << endl;
            cout << "Microseconds:       ";
            auto start = chrono::high_resolution_clock::now();
            // Encontra e mostra os SCCs
            g.printSCCs();
            auto stop = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

            cout << duration.count() << endl;
            cout << "\n----------------------------------\n" << endl;

            FILE << edge_prob << " " << vertices[i] << " " << duration.count() << endl;
        }
    }
    FILE.close();
	return 0; 
} 
