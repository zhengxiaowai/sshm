format:
	autopep8 -ir ./sshr/

clean:
	find . -name \*.pyc -delete
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

.PHONY:
	format
	clean
