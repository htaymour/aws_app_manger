import boto3
import yaml
import system
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
s3 = boto3.resource('s3')

def bucket_names():
    global bucket_list
    bucket_list = []
    for bucket in boto3.resource('s3').buckets.all():
        bucket_list.append(s3_resource.Bucket(bucket.name))
    print (bucket_list)

def get_bucket():
    global bucket_name
    global bucket_list
    bucket_names()
    with open(r'.aws\bucket.txt') as b:
        # get the bucket name from file
        bucket_name = b.readline()
    b.close()
    for bucket in bucket_list:
        if bucket.name.lower() == bucket_name.lower():
            return()
    print("bucket name in file bucket.txt is not found on aws s3. Please correct bucket name. Bucket list as below :")
    for bucket in bucket_list: print(bucket.name)
    exit()


  
def get_yaml():
    global bucket_name
    yaml_file_name = "ota_index.yaml"
    try:
        s3_resource.Object(bucket_name, yaml_file_name).download_file(f'bucket_index.yaml') 
        return ('Connected')
    except:
        pass
    return ('NO CONNECTION')
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    # error_code = e.response['Error']['Code']    


def list_files(path):
    file_list = []
    for my_bucket_object in bucket_list[0].objects.all():
        if my_bucket_object.key.startswith(path):
            #print(my_bucket_object.key)
            file_list.append(my_bucket_object.key)
    return (file_list)

def list_dict_files():
    global file_dict
    with open(r'bucket_index.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML values to Python the dictionary format
        file_dict = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    return(file_dict)

def list_app_files(path):
    global file_dict
    global file_list
    file_list = []
    list_dict_files()
    for x in range(len(file_dict['apps'])):
        file_name = file_dict['apps'][x]['filename']
        if file_name.startswith(path):
            #print(file_name)
            file_list.append(file_name)
    return(file_list)

def copy_to_dir(source_file_name, dest_file_name):
    global bucket_name
    #try:
    copy_source = {
        'Bucket': bucket_name,
        'Key': source_file_name  }
    s3_resource.Object(bucket_name, dest_file_name).copy(copy_source)

def del_from_dir(source_file_name):
    global bucket_name
    try:
        s3_resource.Object(bucket_name, source_file_name).delete()
        return ('OK')
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        return (error_code)

def move_to_dir(source_file_name, dest_file_name):
    global bucket_name
    copy_to_dir(source_file_name, dest_file_name)
    status = del_from_dir(source_file_name)
    if status == 'OK' : status = 'Transfer successful'
    else : status = 'Transfer error'
    return(status)
   

def __init__(self):
    bucket_names()
    get_bucket()
