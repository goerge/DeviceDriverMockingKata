call python -m coverage run --omit=test_* -m unittest discover %*
call python -m coverage html
