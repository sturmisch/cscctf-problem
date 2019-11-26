#!/bin/bash

if [[ "$(whoami)" != "root" ]] || groups | grep -q docker && [[ "$?" != "0" ]]; then
	echo "You must be root or in docker group to use this."
	exit 1
fi

rootdir=$(pwd)
for compose in $(find $rootdir -name docker-compose.yml); do
	targetdir=$(sed 's/docker-compose.yml//g' <<< $compose)
	cd $targetdir
	docker-compose -f ./docker-compose.yml up --build -d
	cd $rootdir
done