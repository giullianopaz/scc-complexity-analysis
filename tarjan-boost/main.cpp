//=======================================================================
// Copyright 2001 Jeremy G. Siek, Andrew Lumsdaine, Lie-Quan Lee, 
//
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//=======================================================================
#include <vector>
#include <iostream>
#include <fstream>
#include <chrono>

#include <boost/config.hpp>
#include <boost/graph/strong_components.hpp>
#include <boost/graph/adjacency_list.hpp>

using namespace std;

// Gera numeros aleatorios
double doubleRand() {
    return double(rand()) / (double(RAND_MAX) + 1.0);
}

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
        // vertices[i] = 10 * (i+1)*100;
        vertices[i] = 10 * (i+1)*100*3;
    }

    // for (int i = 0; i < n_possible_vertices; ++i){
    //     cout << vertices[i] << endl;
    // }
    // return(0);

     // Arquivo de escrita
    ofstream FILE;
    FILE.open("out.txt");

    typedef boost::adjacency_list < boost::vecS, boost::vecS, boost::directedS > Graph;

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
                        boost::add_edge(v1, v2, g);
                        edges_counter++;
                    }
                }
            }
            cout << edges_counter << endl;
            cout << "Microseconds:       ";
            auto start = chrono::high_resolution_clock::now();
            
            // ----------------------------------------------------
            vector<int> c(vertices[i]);
            int num = boost::strong_components(
                g,
                boost::make_iterator_property_map(
                    c.begin(), get(boost::vertex_index, g), c[0]
                )
            );

            // cout << "Total number of components: " << num << endl;
            // vector < int >::iterator iter;
            // for (iter = c.begin(); iter != c.end(); ++iter)
            //     cout << "Vertex " << iter - c.begin() << " is in component " << *iter << endl;
            
            // ----------------------------------------------------

            auto stop = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

            cout << duration.count() << endl;
            cout << "\n----------------------------------\n" << endl;

            FILE << edge_prob << " " << vertices[i] << " " << duration.count() << endl;
        }
    }
    
    // Graph G(N);
    // boost::add_edge(0, 1, G);
    // boost::add_edge(1, 1, G);
    // boost::add_edge(1, 3, G);
    // boost::add_edge(1, 4, G);
    // boost::add_edge(3, 4, G);
    // boost::add_edge(3, 0, G);
    // boost::add_edge(4, 3, G);
    // boost::add_edge(5, 2, G);

    // vector<int> c(N);
    // int num = boost::strong_components(
    //     G,
    //     boost::make_iterator_property_map(
    //         c.begin(), get(boost::vertex_index, G), c[0]
    //     )
    // );

    // cout << "Total number of components: " << num << endl;
    // vector < int >::iterator i;
    // for (i = c.begin(); i != c.end(); ++i)
    //     cout << "Vertex " << i - c.begin() << " is in component " << *i << endl;
    
    FILE.close();
    return EXIT_SUCCESS;
}
