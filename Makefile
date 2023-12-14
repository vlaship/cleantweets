build:
	# delete container and image
	docker container rm -f clean-tweets || true
	docker image rm -f clean-tweets || true
	# build image
	docker build -t clean-tweets .
	# create container
	docker create --name clean-tweets clean-tweets python3 /app/cleantweets.py --delete --days 10 --verbose --config my_settings.ini

run:
	docker start -a clean-tweets
