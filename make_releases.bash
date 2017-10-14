rm -rf build/ dist/ *.spec
pyinstaller --paths modules/ --add-data data:data tcm_lib_search.py
pyinstaller --paths modules/ \
            --add-data data:data \
            --add-data modules/jieba/dict.txt:jieba/ \
            --add-data modules/jieba/analyse/idf.txt:jieba/analyse/ \
            --hidden-import sklearn.neighbors.typedefs \
            extract_formula.py
# rm -rf build/ tcm_lib_search.spec
