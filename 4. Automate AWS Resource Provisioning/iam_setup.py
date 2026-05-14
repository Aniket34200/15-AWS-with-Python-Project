import boto3
import json

iam = boto3.client('iam')

def create_user(username):
    try:
        response = iam.create_user(UserName=username)
        print(f"User {username} created.")
        return response
    except Exception as e:
        print(e)

def attach_policy(username):
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"

    iam.attach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

    print("Policy attached.")

if __name__ == "__main__":
    user = "demo-user"
    create_user(user)
    attach_policy(user)