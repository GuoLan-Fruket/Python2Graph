#!/bin/bash

if [ $# -ge 1 ] && [ "$1" == "default" ]; then
    if [ $# -eq 1 ]; then
        echo "python3 src/py2graph.py --build --force"
        echo "    --calc-thread=1 --io-thread=8"
        echo "    --v-batch=400 --e-batch=200"
        time python3 src/py2graph.py --build --force  \
            --calc-thread=1 --io-thread=8             \
            --v-batch=400 --e-batch=200
    elif [ $# -eq 2 ]; then
        echo "python3 src/py2graph.py --build --force"
        echo "    -p $2"
        echo "    --calc-thread=1 --io-thread=8"
        echo "    --v-batch=400 --e-batch=200"
        time python3 src/py2graph.py --build --force  \
            -p $2                                     \
            --calc-thread=1 --io-thread=8             \
            --v-batch=400 --e-batch=200
    elif [ $# -eq 3 ]; then
        echo "python3 src/py2graph.py --build --force"
        echo "    -p $2 -c $3"
        echo "    --calc-thread=1 --io-thread=8"
        echo "    --v-batch=400 --e-batch=200"
        time python3 src/py2graph.py --build --force  \
            -p $2 -c $3                               \
            --calc-thread=1 --io-thread=8             \
            --v-batch=400 --e-batch=200
    elif [ $# -eq 4 ]; then
        echo "python3 src/py2graph.py --build --force"
        echo "    -p $2 -c $3 -d $4"
        echo "    --calc-thread=1 --io-thread=8"
        echo "    --v-batch=400 --e-batch=200"
        time python3 src/py2graph.py --build --force  \
            -p $2 -c $3 -d $4                         \
            --calc-thread=1 --io-thread=8             \
            --v-batch=400 --e-batch=200
    else
        echo "./build.sh default [project_path] [config_path] [diff_path]"
    fi
elif [ $# -eq 0 ]; then
    echo "./build.sh default [project_path]"
    echo "Or specify the arguments:"
    python3 src/py2graph.py --help
else
    echo "time python3 src/py2graph.py $@"
    time python3 src/py2graph.py $@
fi
