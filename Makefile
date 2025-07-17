# Local analysis by pytest, coverage run pytest, flake8, and badge generation.
#
# This Makefile presumes an activated virtual environment of Python and an
# internet connection for pytest's checks on pubchempy's interaction with NIH.
# In contast to e.g., the coverage badge by coveralls, the setup here does not
# rely on a separate account, nor a GitHub token to work.  By flag `-l`, the
# badges are created locally, independent of genbadge's default to reach out
# for shields.io.

default:
	@echo "Tap the tabulator key twice to display the options available."

analysis_setup:
# For now, the partial overlap with `requirements/dev.txt` is intentional.
	pip install coverage flake8 genbadge[all] pyclean pytest

coverage_analysis:
	coverage run --include=src/* -m pytest -v
coverage_badge:
	coverage report && coverage xml && coverage html
	genbadge coverage -i coverage.xml -lv

flake8_analysis:
	-rm -r reports
	-rm flake8stats.txt
	mkdir reports

	flake8 src/* --exit-zero --statistics --count \
		--tee --format=html --htmldir=reports/ --output-file flake8stats.txt \
		--max-line-length 90

	@echo ""
	@echo "For a more detailed report, see file reports/index.html."
flake8_badge:
	genbadge flake8 -i flake8stats.txt -lv

pytest_analysis:
	pytest --rootdir=src --cache-clear --junitxml=junit.xml -v
pytest_badge:
	genbadge tests -i junit.xml -lv

remove_all_but_the_badges:
	-rm -r __pycache__
	-rm -r tests/__pycache__
	-rm *.xml

	-rm .coverage
	-rm -r htmlcov

	-rm -r reports
	-rm flake8stats.txt

	-pyclean .
