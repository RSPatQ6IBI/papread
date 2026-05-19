from google.cloud import storage
the_filelist_gcpbucket_ = []
def list_files_in_folder(bucket_name, folder_path):
    """Lists all files in a specific GCP bucket folder."""
    # Initialize the client
    storage_client = storage.Client()
    
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # List blobs with the specified prefix (folder path)
    # Ensure folder_path ends with '/' to target a specific directory
    blobs = bucket.list_blobs(prefix=folder_path)

    print(f"Files in {bucket_name}/{folder_path}:")
    for blob in blobs:
        # Filter out the folder itself if it appears in the results
        if not blob.name.endswith('/'):
            print(blob.name)
            the_filelist_gcpbucket_.append(blob.name)
    return the_filelist_gcpbucket_

# Usage
if __name__ == "__main__":
    bucket_name_ =  "my_gcp_audio_bucket_1409"
    folder_path_= "third-author-bucket/"
    filelist_gcpbucket_ = list_files_in_folder(bucket_name=bucket_name_, folder_path=folder_path_)
