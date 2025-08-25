#! /bin/bash

regions="eu-central,us-west,us-east,ap-southeast"
run_num=${run_num:-0}

IFS=","
LOCUST_FILENAME="conf/bigbrain_cdn.txt"
for region in $regions
do
    echo $region
    LOCUST_TARGET="cdn-data-vm"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-datavm-cdn-$run_num/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done

for region in $regions
do
    echo $region
    LOCUST_TARGET="cdn-siibra-api"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-siibraapi-cdn-$run_num/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done

for region in $regions
do
    echo $region
    LOCUST_TARGET="cdn-siibra-explorer"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-siibraexplorer-cdn-$run_num/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done

