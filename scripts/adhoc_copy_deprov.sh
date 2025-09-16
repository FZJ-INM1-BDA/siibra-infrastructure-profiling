#! /bin/bash

if [[ -z "$LINODE_TOKEN" ]]
then
    echo "LINODE_TOKEN env var must be defined"
    exit 1
fi

if [[ -z "$LINODE_IP" ]]
then
    echo "LINODE_IP must be defined"
    exit 1
fi

if [[ -z "$LINODE_REGION" ]]
then
    echo "LINODE_REGION must be defined"
    exit 1
fi

if [[ -z "$LINODE_ID" ]]
then
    echo "LINODE_ID must be defined"
    exit 1
fi

if [[ -z "$TARGET_DIR" ]]
then
    echo "TARGET_DIR must be defined"
    exit 1
fi


yml='
- name: "Set variable"
  hosts: localhost

  tasks:
  - name: Add remote VM
    add_host:
      hostname: "'$LINODE_IP'"
      groups: remotevms
    changed_when: false
    
  - name: Set facts
    set_fact:
    
      LINODE_TOKEN: '$LINODE_TOKEN'
      LINODE_REGION: "'$LINODE_REGION'"
      LINODE_IDS: 
      - "'$LINODE_ID'"
      LINODE_IDS_IPV4S:
        "'$LINODE_ID'": "'$LINODE_IP'"
      LINODE_IDS_REGION:
        "'$LINODE_ID'": "'$LINODE_REGION'"
      TARGET_DIR: "'$TARGET_DIR'"

- name: "Copy result"
  import_playbook: "./ansible/playbooks/copyresult.playbook.yml"

- name: "Deprov"
  import_playbook: "./ansible/playbooks/deprovnode.playbook.yml"
'

echo -n "$yml" > tmp.playbook.yml
ansible-playbook -i ansible/inventory.yml tmp.playbook.yml
rm tmp.playbook.yml
