rm -rf build/ dist/ tcm_lib_search.spec
pyinstaller --paths modules/ --add-data data:data tcm_lib_search.py
pyinstaller --paths modules/ --add-data data:data --hidden-import sklearn.neighbors.typedefs extract_formula.py
# rm -rf build/ tcm_lib_search.spec
