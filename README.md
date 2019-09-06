# aws-ebs-spot-recovery

The purpose of this app is to make a spot-instance STATEFUL, to do that  we retrieve or create eip and volumes during ec2 startup of spot instances. It uses a tag added to the resource to track if it exists, otherwise it creates the resource and tag it with the given service name.

If an instance dies and a new one is spun up in a different availability zone(AZ), the script will take a snapshot of the latest created volume that is tagged, create a new volume in the new AZ with the recent taken snapshot and attach it to the new spot instance.

In resume, this is literally AWS for the poor. 


Help:
```
usage: main.py [-h] [-p PROFILE] [-r REGION] [-d] [-i INSTANCE] [-v]
               [-mv MOUNT_VOLUME] [-me MOUNT_EIP] [-e]
               service

```

Sample usage:
```
python main.py -e -v stores-vm
```
This will mount the eip and volume that has the tag stores-vm on it, it it doesn't exist, it will create a new one and tag it.
