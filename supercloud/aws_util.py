import boto3


class AwsUtil:

    @staticmethod
    def get_session(**kwargs):
        sess = boto3.session.Session(**kwargs)
        return sess
