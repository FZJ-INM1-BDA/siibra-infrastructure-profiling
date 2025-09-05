
regions="eu-central,us-west,us-east,ap-southeast"
LOCUST_FILENAME="conf/guided_workflow.txt"
GUIDED_WORKFLOW_COUNT=${GUIDED_WORKFLOW_COUNT:-0}
IFS=","

for region in $regions
do
    echo $region
    LOCUST_TARGET="none"
    
    ansible-playbook -i ansible/inventory.yml \
        -e TARGET_DIR=../../run-result/geoprofile-guided-workflow-$GUIDED_WORKFLOW_COUNT/ \
        -e LOCUST_TARGET=$LOCUST_TARGET \
        -e LINODE_TOKEN=$LINODE_TOKEN \
        -e LOCUST_FILENAME=$LOCUST_FILENAME \
        -e LINODE_REGION=$region \
        ansible/playbooks/workflow.profile.playbook.yml
done
