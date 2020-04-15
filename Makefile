docker_file?=Dockerfile

.PHONY: test render build

build:
	docker build -f $(docker_file) -t $(tag) .

TEST=$(shell pwd)/test

clean:
	rm -rf $(TEST)/*/ $(TEST)/*_rmd.* || exit 0
	
test:
	make clean
	make render dir=$(TEST)

render:
	./render $(dir)
