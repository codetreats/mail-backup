#!/bin/bash
set -e
cd $(dirname "$0")
BASEDIR=$(pwd)

CONFIG=$1
if [[ $CONFIG == "" ]] ; then
  CONFIG=config.cfg
fi

echo "Use config: $CONFIG"

chmod +x $CONFIG
. $CONFIG

assert_var() {
     MSG=$1
     VAR=$2

     if [[ $VAR == "" ]]
     then
          echo $MSG
          exit 1
     fi
}

export CONTAINER_NAME
export CONFIG_DIR
export MAIL_FOLDER
export UNSYNCED_FOLDER
export PIPELINE_PORT

assert_var "export CONTAINER_NAME not set" $export CONTAINER_NAME
assert_var "export CONFIG_DIR not set" $export CONFIG_DIR
assert_var "export MAIL_FOLDER not set" $export MAIL_FOLDER
assert_var "export UNSYNCED_FOLDER not set" $export UNSYNCED_FOLDER
assert_var "export PIPELINE_PORT not set" $export PIPELINE_PORT


mkdir -p $MAIL_FOLDER
mkdir -p $UNSYNCED_FOLDER

# remove old container
if [[ $(docker ps -q --filter "name=$CONTAINER_NAME"  | wc -l) -gt 0 ]]
then
     echo "Remove $CONTAINER_NAME"
     docker rm -f $CONTAINER_NAME
fi

docker image prune -f

# build image
cd $BASEDIR/container
docker build -t mail-backup:master .

# start
cd $BASEDIR
mkdir -p tmp/$CONTAINER_NAME
cp docker-compose.yml tmp/$CONTAINER_NAME/
cd tmp/$CONTAINER_NAME

docker-compose up --detach