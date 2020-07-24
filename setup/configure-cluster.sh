#!/bin/bash

USERS="ssakhuja@aramse.io dmuchene@aramse.io sma@aramse.io"

for user in $USERS; do
  base=$(echo $user | cut -d '@' -f 1)
  kubectl create ns $base
  kubectl create rolebinding $base -n $base --clusterrole edit --user "$user"
  kubectl create clusterrolebinding $base-view --clusterrole view --user "$user"
done
  
