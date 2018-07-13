# Only use these programs directly or explain yourself:
#  awk cat cmp cp diff echo egrep expr false grep install-info ln ls
#  mkdir mv printf pwd rm rmdir sed sleep sort tar test touch tr true

.PHONY: dev staging production
all: dev

.PHONY: common-conf
common-conf: docker/staging/conf/explorer.env docker/staging/conf/explorer.proc docker/staging/conf/elements.env docker/staging/conf/elements.proc docker/staging/conf/bitcoin.env docker/staging/conf/bitcoin.proc
	rm -rf docker/conf
	cp -r ./docker/staging/conf ./docker/conf

dev: common-conf
	cd docker/staging && docker-compose up --build
staging: common-conf
	cd docker/staging && docker-compose up -d --build
production: common-conf
	cd docker/staging && docker-compose up -d --build

.PHONY: stop clean docker-prune clean-db
stop:
	cd docker/staging ; docker-compose stop
# docker-compose rm -f
# cd docker && docker-compose down
docker-prune:
	docker system prune -a

clean-db:
	rm -f ../explorer-data/target/schema.json

clean: docker-prune clean-db
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -q)
