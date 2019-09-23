echo -e "\n**Boost Tarjan Algorithm**\n"

echo "Setting env variables..."
if [ -n "$1" ]; then
  echo "VERTICES_RANGE: OK"
  export VERTICES_RANGE="$1"
else
  echo "VERTICES_RANGE: ERROR"
  exit 1
fi

if [ -n "$2" ]; then
  echo "EDGES_MAX_PROB: OK"
  export EDGES_MAX_PROB="$2"
else
  echo "EDGES_MAX_PROB: ERROR"
  exit 1
fi

echo -n "Compiling C++ code..."
g++ -I /usr/local/boost_1_70_0/ -o main main.cpp
echo " OK"

echo "Running..."
./main