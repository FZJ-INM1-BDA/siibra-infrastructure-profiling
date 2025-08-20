# /bin/bash

LOCUST_TARGET="data-vm"
ansible-playbook -i ansible/inventory.yml \
    -e TARGET_DIR=../../run-result/stressprofile-datavm/ \
    -e LINODE_TOKEN=$LINODE_TOKEN \
    -e LOCUST_TARGET=$LOCUST_TARGET \
    -e LINODE_MULT=8 \
    -e LINODE_REGION=eu-central \
    ansible/playbooks/workflow.profile.playbook.yml
    
LOCUST_TARGET="siibra-api"
ansible-playbook -i ansible/inventory.yml \
    -e TARGET_DIR=../../run-result/stressprofile-siibraapi/ \
    -e LINODE_TOKEN=$LINODE_TOKEN \
    -e LOCUST_TARGET=$LOCUST_TARGET \
    -e LINODE_MULT=8 \
    -e LINODE_REGION=eu-central \
    ansible/playbooks/workflow.profile.playbook.yml
    
LOCUST_TARGET="siibra-explorer"
ansible-playbook -i ansible/inventory.yml \
    -e TARGET_DIR=../../run-result/stressprofile-siibraexplorer/ \
    -e LINODE_TOKEN=$LINODE_TOKEN \
    -e LOCUST_TARGET=$LOCUST_TARGET \
    -e LINODE_MULT=8 \
    -e LINODE_REGION=eu-central \
    ansible/playbooks/workflow.profile.playbook.yml
