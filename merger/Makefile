build:
	docker build -t merger .

run:
	docker run -v $(PWD)/../data:/data merger > ../web/events-$(shell date +%Y-%m-%d-%H:%M).html
	cd ../web && ln -sf events-$(shell date +%Y-%m-%d-%H:%M).html index.html
