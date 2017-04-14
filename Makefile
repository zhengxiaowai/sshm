clean:
	find . -name \*.pyc -delete
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

.PHONY:
	newclient
	clean
