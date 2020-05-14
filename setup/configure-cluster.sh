#!/bin/bash

USERS=""

for user in $USERS; do
  base=$(echo $user | cut -d '@' -f 1)
  kubectl create ns $base
  kubectl create rolebinding $base -n $base --clusterrole edit --user "$user"
done
  
