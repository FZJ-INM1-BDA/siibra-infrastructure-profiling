#! /bin/bash

regions="eu-central,us-west,us-east,ap-southeast"
LOCUST_FILENAME=${LOCUST_FILENAME:-conf/bigbrain.txt}

IFS=","

for region in $regions
do
    echo $region
    LOCUST_TARGET="data-vm"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-datavm/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done

for region in $regions
do
    echo $region
    LOCUST_TARGET="siibra-api"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-siibraapi/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done

for region in $regions
do
    echo $region
    LOCUST_TARGET="siibra-explorer"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-siibraexplorer/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done



