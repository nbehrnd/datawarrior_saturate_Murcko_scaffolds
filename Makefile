.PHONY: test

test:
	pytest-3 -xv test.py
	rm -r ./__pycache__
