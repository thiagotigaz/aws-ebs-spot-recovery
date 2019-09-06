import argparse
import logging

from supercloud.aws_util import AwsUtil
from supercloud.ec2_manager import Ec2Manager

REGION = 'region_name'

PROFILE_NAME = 'profile_name'

AVAILABILITY_ZONE = 'AvailabilityZone'

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def create_argparse():
    parser = argparse.ArgumentParser(description='supercloud spot ebs helper')
    group = parser.add_argument_group(title='action')
    group.add_argument('-p', '--profile', type=str, help='Aws profile for fetching boto3 session.')
    group.add_argument('-r', '--region', type=str, help='Aws region for fetching boto3 session.')
    parser.add_argument('-d', '--dryrun', action='store_true', help='When set, run aws commands with dryrun.')
    parser.add_argument('-i', '--instance', type=str, help='InstanceId of instance where volume should be attached to.')
    parser.add_argument('-v', '--volume', action='store_true', help='Find volume by tracker tag and attach it to the instance. If '
                                                         'volume is not  present, script will create a new one and tag '
                                                         'it with service tag.')
    parser.add_argument('-mv', '--mount-volume', type=str, help='Attach given volumeId to the instance.')
    parser.add_argument('-me', '--mount-eip', type=str, help='Attach given eip alloc to the instance.')
    parser.add_argument('-e', '--eip', action='store_true',
                        help='Find eip by service tag and attach it to the instance. If eip is not  present, script '
                             'will alloc a new one and tag it with service tag.')
    parser.add_argument('service', type=str, help='Tag used to search for the volume or eip.')

    return parser.parse_args()


def get_aws_args(args):
    aws_args = {}
    if args.profile is not None:
        aws_args[PROFILE_NAME] = args.profile
    if args.region is not None:
        aws_args[REGION] = args.region
    return aws_args


def main():
    try:
        args = create_argparse()
        aws_args = get_aws_args(args)
        LOG.info(args)
        print(args)
        session = AwsUtil.get_session(**aws_args)
        ec2_manager = Ec2Manager(session, args.dryrun)
        if args.instance:
            instance = ec2_manager.find_instance_by_id(args.instance)
        else:
            instance = ec2_manager.find_running_instance()
        instance_az = instance.placement[AVAILABILITY_ZONE]

        # Handles EIP alloc/association
        eip_alloc = ec2_manager.find_or_create_eipalloc(args.service) if args.eip else args.mount_eip
        if eip_alloc:
            LOG.info('Attaching eip {} to instance {}'.format(eip_alloc, instance.id))
            ec2_manager.attach_eip(eip_alloc, instance)

        # Handles ebs migration/mount
        if args.volume :
            volume = ec2_manager.find_or_create_volume(args.service, instance_az)
            if volume.availability_zone == instance_az:
                LOG.info('The {} is in the same AZ({}) as instance {}. Going to mount it to instance.'
                         .format(volume.id, instance_az, instance.id))
            else:
                LOG.info('The {} is on AZ {} while {} is on AZ {}. Going to migrate volume before mounting.'
                         .format(instance.id, instance_az, volume.id, volume.availability_zone))
                volume = ec2_manager.clone_volume(volume, instance_az)
        if args.mount_volume:
            volume = ec2_manager.find_volume_by_id(args.mount_volume)

        if volume:
            ec2_manager.mount_volume(volume, instance.id)
    except Exception as ex:
        LOG.error(ex)
        raise


if __name__ == "__main__":
    main()
