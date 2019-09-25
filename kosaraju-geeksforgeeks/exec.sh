echo -e "\n**GeeksforGeeks Kosaraju Algorithm**\n"
echo -e "    ~$ bash exec.sh <RUNNING_TIMES> <VERTICES_RANGE> <EDGES_MAX_PROB>\n"

echo -n "Setting env variables..."
if [ -n "$1" ]; then
  export RUNNING_TIMES="$1"
else
  export RUNNING_TIMES="10"
fi

if [ -n "$2" ]; then
  export VERTICES_RANGE="$2"
else
  export VERTICES_RANGE="10"
fi

if [ -n "$3" ]; then
  export EDGES_MAX_PROB="$3"
else
  export EDGES_MAX_PROB="1.0"
fi
echo " OK"

echo -n "Compiling C++ code..."
g++ -I /usr/local/boost_1_70_0/ -o main main.cpp
echo " OK"

echo -e "Running...\n"
time ./main