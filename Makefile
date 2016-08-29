requirements:
	pip install -r requirements/common.txt
	pip install -r requirements/development.txt

test:
	python manage.py test mutopia.tests -v2

coverage:
	coverage run                                \
        --source=mutopia                        \
        --branch                                \
        manage.py test mutopia.tests            \
        -v2 &&                                  \
    coverage html &&                            \
    coverage report

docs:
	(cd docs; make html)

.PHONY: test coverage docs requirements
