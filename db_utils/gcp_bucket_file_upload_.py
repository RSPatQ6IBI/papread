from google.cloud import storage
from gcp_bucket_fetch_filelist_ import list_files_in_folder
# Uploads a file using the google-cloud-storage library
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

if __name__ == "__main__":
    paper_name_ = "20260518_175506_Hot Swapping for Online Adaptation of Optimization Hyperparameters_Ref_1.pdf"
    bucket_name_ =  "my_gcp_audio_bucket_1409"
    source_file_name_ = "reference_pdf_download_repo_/"+paper_name_
    folder_path_ = "third-author-bucket/"
    destination_blob_name_= "third-author-bucket/"+paper_name_
    filelist_gcpbucket_ = list_files_in_folder(bucket_name=bucket_name_, folder_path=folder_path_)
    match_score_ = [False] 
    match_score_ = [True if paper_name_ in y else False for y in filelist_gcpbucket_]
    print(match_score_, any(match_score_))
    if any(match_score_): 
        print('File Already Exists -- >>') 
    else:
        upload_blob(bucket_name=bucket_name_, source_file_name=source_file_name_, destination_blob_name=destination_blob_name_)
    
    