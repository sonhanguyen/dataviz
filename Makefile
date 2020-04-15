docker_file ?= Dockerfile
.PHONY: test render build

build:
	docker build -f $(docker_file) -t $(tag) .

TEST=test

clean:
	rm $(TEST)/*_rmd.* || exit 0
	
test:
	make clean
	DOCKER_FILE=$(docker_file) ./render $(TEST)

render:
	DOCKER_FILE= ./render $(dir)
