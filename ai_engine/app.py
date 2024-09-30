from ai_engine.engine.engine import startup_engine


sample_event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-central-1:288761749700:tasks-data-completed-dev:b0f4c590-2dae-46f0-b674-0397444cc0ae', 'Sns': {'Type': 'Notification', 'MessageId': '86dfe6ae-f000-533d-adc4-b9c208d5eb91', 'TopicArn': 'arn:aws:sns:eu-central-1:288761749700:tasks-data-completed-dev', 'Subject': None, 'Message': '{"task_id": "5fab7da4-0a25-4b26-ad66-aab79a6e6eea"}', 'Timestamp': '2024-09-24T17:27:49.676Z', 'SignatureVersion': '1', 'Signature': 'IH2jcXJQC133LzFF1yQAdCp5H6Ibuf2hPMo04LX1ADcX1VGJFquz6N+P7oX943bByGVBB9PC7TXaVsJE0fiaBWWeWu9LPiW3NAfvn/fhpdfVWVC4B9nC8sum8WPnvHge/+A+4eDhGk93mqYtVgL5xfhsQhns/sCSIi+UzjCwIknHr8KbM5whXisPfl9rEkrG2ev4NBWvHRVB7JKbR+8ewD/9zXpy5MJkmB5eFpwaClBLl39v4SSs0scYRLYH1Vv57LOymHWtD7vgihQkJ4jG08P1wYCFP+HBGdRcg/gRmZ9mdr7tQ5JmprvlwoCOsG9Tul8791qJ+70k5CMkIl7PUg==', 'SigningCertUrl': 'https://sns.eu-central-1.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem', 'UnsubscribeUrl': 'https://sns.eu-central-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-central-1:288761749700:tasks-data-completed-dev:b0f4c590-2dae-46f0-b674-0397444cc0ae', 'MessageAttributes': {}}}]}


def handler(event: dict, context):
    return startup_engine(sample_event)