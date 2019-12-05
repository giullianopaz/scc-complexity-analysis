// A C++ program to find strongly connected components in a given 
// directed graph using Tarjan's algorithm (single DFS) 
#include <iostream> 
#include <list> 
#include <stack>
#include <chrono>
#include <fstream>

#include <boost/config.hpp>
#include <boost/graph/strong_components.hpp>
#include <boost/graph/adjacency_list.hpp>

#define NIL -1 
using namespace std; 

// A class that represents an directed graph 
class Graph 
{ 
	int V; // No. of vertices 
	list<int> *adj; // A dynamic array of adjacency lists 

	// A Recursive DFS based function used by SCC() 
	void SCCUtil(int u, int disc[], int low[], 
				stack<int> *st, bool stackMember[], int *ptr_counter); 
public: 
	Graph(int V); // Constructor
	~Graph(); // Desstructor 
	void addEdge(int v, int w); // function to add an edge to graph 
	int SCC(); // prints strongly connected components 
}; 

Graph::Graph(int V) 
{ 
	this->V = V; 
	adj = new list<int>[V]; 
} 

Graph::~Graph() 
{ 
	delete [] adj;
} 

void Graph::addEdge(int v, int w) 
{ 
	adj[v].push_back(w); 
} 

// A recursive function that finds and prints strongly connected 
// components using DFS traversal 
// u --> The vertex to be visited next 
// disc[] --> Stores discovery times of visited vertices 
// low[] -- >> earliest visited vertex (the vertex with minimum 
//			 discovery time) that can be reached from subtree 
//			 rooted with current vertex 
// *st -- >> To store all the connected ancestors (could be part 
//		 of SCC) 
// stackMember[] --> bit/index array for faster check whether 
//				 a node is in stack 
void Graph::SCCUtil(int u, int disc[], int low[], stack<int> *st, 
					bool stackMember[], int *ptr_counter) 
{ 
	// A static variable is used for simplicity, we can avoid use 
	// of static variable by passing a pointer. 
	static int time = 0; 

	// Initialize discovery time and low value 
	disc[u] = low[u] = ++time; 
	st->push(u); 
	stackMember[u] = true; 

	// Go through all vertices adjacent to this 
	list<int>::iterator i; 
	for (i = adj[u].begin(); i != adj[u].end(); ++i) 
	{ 
		int v = *i; // v is current adjacent of 'u' 

		// If v is not visited yet, then recur for it 
		if (disc[v] == -1) 
		{ 
			SCCUtil(v, disc, low, st, stackMember, ptr_counter); 

			// Check if the subtree rooted with 'v' has a 
			// connection to one of the ancestors of 'u' 
			// Case 1 (per above discussion on Disc and Low value) 
			low[u] = min(low[u], low[v]); 
		} 

		// Update low value of 'u' only of 'v' is still in stack 
		// (i.e. it's a back edge, not cross edge). 
		// Case 2 (per above discussion on Disc and Low value) 
		else if (stackMember[v] == true) 
			low[u] = min(low[u], disc[v]); 
	} 

	// head node found, pop the stack and print an SCC 
	int w = 0; // To store stack extracted vertices 
	if (low[u] == disc[u]) 
	{ 
		while (st->top() != u) 
		{ 
			w = (int) st->top(); 
			// cout << w << " "; 
			stackMember[w] = false; 
			st->pop(); 
		} 
		w = (int) st->top(); 
		// cout << w << "\n"; 
        ++*ptr_counter;
		stackMember[w] = false; 
		st->pop(); 
	} 
} 

// The function to do DFS traversal. It uses SCCUtil() 
int Graph::SCC() 
{ 
	int *disc = new int[V]; 
	int *low = new int[V]; 
	bool *stackMember = new bool[V]; 
	stack<int> *st = new stack<int>();

    int counter = 0;

	// Initialize disc and low, and stackMember arrays 
	for (int i = 0; i < V; i++) 
	{ 
		disc[i] = NIL; 
		low[i] = NIL; 
		stackMember[i] = false; 
	} 

	// Call the recursive helper function to find strongly 
	// connected components in DFS tree with vertex 'i' 
	for (int i = 0; i < V; i++) 
		if (disc[i] == NIL) 
			SCCUtil(i, disc, low, st, stackMember, &counter);

    return counter;
}

// Gera numeros aleatorios
double doubleRand() {
    return double(rand()) / (double(RAND_MAX) + 1.0);
}

// Driver program to test above function 
int main() 
{
    typedef boost::adjacency_list < boost::vecS, boost::vecS, boost::directedS > BoostGraph;
	
    // Contador de arestas
    long long edges_counter = 0;
    
    // Quantidade de possibilidades de vertices
    int n_running_times = (int)atoi(getenv("RUNNING_TIMES"));
    int n_possible_vertices = (int)atoi(getenv("VERTICES_RANGE"));
    double edges_max_p = (double)atof(getenv("EDGES_MAX_PROB"));

    cout << "RUNNING_TIMES: " << n_running_times << endl;
    cout << "VERTICES_RANGE: " << n_possible_vertices << endl;
    cout << "EDGES_MAX_PROB: " << edges_max_p << endl;
    
    // Vetor com as possibilidades de valores de vertices -> 10e1...10e10
    int vertices[n_possible_vertices];
    for (int i = 0; i <= n_possible_vertices; ++i) {
        // vertices[i] = pow(10, i+1);
        vertices[i] = 10 * (i+1);
        // vertices[i] = 10 * (i+1)*10;
    }

    // for (int i = 0; i < 10; ++i){
    //     cout << vertices[i] << endl;
    // }
    // return(0);

    for (int x = 1; x <= n_running_times; ++x){
        cout << "\n################# "<< x << " #####################\n" << endl;
        
        // Percorre todas as combinacoes de vertices
        for (double edge_prob = 0.1; edge_prob <= edges_max_p; edge_prob = edge_prob + 0.1){
            
            cout << "\n==================================\n" << endl;
            for (int i = 0; i < n_possible_vertices; ++i){
                // Instancia grafo
                Graph g(vertices[i]);
                BoostGraph bg(vertices[i]);

                cout << "Edge Probability:   " << edge_prob << endl;
                cout << "Vertices:           " << vertices[i] << endl;
                cout << "Edges:              ";
                
                for(int v1 = 0; v1 < vertices[i]; ++v1){
                    for (int v2 = 0; v2 < vertices[i]; ++v2){
                        // Se o numero aleatorio for menor que edge_prob, cria aresta
                        if(doubleRand() < edge_prob){
                            // cout << v1 << " -> " << v2 << endl;
                            
                            g.addEdge(v1, v2);
                            boost::add_edge(v1, v2, bg);
                            edges_counter++;
                        }
                    }
                }
                cout << edges_counter << endl;
                
                int num_k = g.SCC();

                vector<int> c(vertices[i]);
                int num_b = boost::strong_components(
                    bg,
                    boost::make_iterator_property_map(
                        c.begin(), get(boost::vertex_index, bg), c[0]
                    )
                );

                if (num_k == num_b){
                    cout << "Boost = Kosaraju" << endl;
                    cout << num_b << " = " << num_k << endl;
                }
                else{
                    cout << "Boost != Kosaraju" << endl;
                    cout << num_b << " != " << num_k << endl;
                    exit(1);
                }

                cout << "\n----------------------------------\n" << endl;

                // cout << edge_prob << " " << vertices[i] << " " << duration.count() << " " << edges_counter << endl;
                edges_counter = 0;
            }
        }
        // FILE.close();
        // flush(FILE);
    }
    cout << "Every is OK!" << endl;
	return 0;
} 
