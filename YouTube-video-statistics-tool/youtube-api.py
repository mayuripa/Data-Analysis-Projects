class YouTubeAPI:
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id

    def get_channel_videos(self):
        """Return video_id,video_title,video_publishTime from all the video of YouTube channel"""

        # Initialize an empty DataFrame to store the results
    
        df = pd.DataFrame(columns=['video_ID', 'video_title', 'video_publishTime'])
    
        # Set the initial page token to an empty string
        page_token = ""

        # Set the maximum number of results per page
        max_results = 50

        # Set the base URL for the YouTube API search endpoint
        base_url = 'https://www.googleapis.com/youtube/v3/search'

        # Set a flag to indicate whether there are more pages of results
        more_results = True

        while more_results:
            # Construct the full URL with the appropriate query parameters
            url = f"{base_url}?key={self.api_key}&channelId={self.channel_id}&part=snippet&type=video&maxResults={max_results}&pageToken={page_token}"

            # Make the request to the YouTube API
            try:
                response = requests.get(url).json()
            except Exception as e:
                # Log the error and retry the request
                print(f"Error making request: {e}")
                break

            # Check if the API returned an error
            if 'error' in response:
                # Log the error and retry the request
                print(f"API error: {response['error']['message']}")
                break

            # Extract the relevant information from the response
            for video in response['items']:
                if video['id']['kind'] == 'youtube#video':
                    video_ID = video['id']['videoId']
                    video_title = video['snippet']['title']
                    video_publishTime = video['snippet']['publishTime'].split('T')[0]

                # Create a temporary DataFrame with the new data
                temp_df = pd.DataFrame({'video_ID': [video_ID],
                                        'video_title': [video_title],
                                        'video_publishTime': [video_publishTime]})

                # Concatenate the temporary DataFrame with df
                df = pd.concat([df, temp_df], ignore_index=True)

            # Check if there is a next page of results
            if 'nextPageToken' in response:
                page_token = response['nextPageToken']
            else:
                more_results = False
        return df
    
    def get_video_stats(self, video_id_list):
        # Initialize an empty DataFrame to store the results
        df = pd.DataFrame(columns=['video_Id','video_viewCount', 'video_likeCount', 'video_favoriteCount', 'video_commentCount'])

        # Set the base URL for the YouTube API video endpoint
        base_url = 'https://www.googleapis.com/youtube/v3/videos'

        # Split the list of video IDs into chunks of 50
        for i in range(0, len(video_id_list), 50):
            video_ids = ",".join(video_id_list[i:i+50])

            # Construct the full URL with the appropriate query parameters
            url = f"{base_url}?id={video_ids}&part=statistics&key={self.api_key}"

            # Make the request to the YouTube API
            try:
                response = requests.get(url).json()
            except Exception as e:
                # Log the error and retry the request
                print(f"Error making request: {e}")

            # Check if the API returned an error
            if 'error' in response:
                # Log the error and retry the request
                print(f"API error: {response['error']['message']}")

            # Extract the relevant information from the response
            for video in response['items']:
                video_ID = video['id']
                video_viewCount = video['statistics']['viewCount']
                video_likeCount = video['statistics']['likeCount']
                video_favoriteCount = video['statistics']['favoriteCount']
                video_commentCount = video['statistics']['commentCount']

                # Create a temporary DataFrame with the new data
                temp_df = pd.DataFrame({'video_Id': [video_ID],
                                        'video_viewCount': [video_viewCount],
                                        'video_likeCount': [video_likeCount],
                                        'video_favoriteCount': [video_favoriteCount],
                                        'video_commentCount': [video_commentCount]})

                # Concatenate the temporary DataFrame with df
                df = pd.concat([df, temp_df], ignore_index=True)

        return df
    def get_comments(self,video_id_list):
        comment_df = pd.DataFrame(columns=['video_id','comment_desc'])

        for v in video_id_list:
            url_v_c='https://www.googleapis.com/youtube/v3/commentThreads?key='+api_key+'&videoId='+v+'&part=snippet,replies&maxResults=1000'
        
            try:
                response_c = requests.get(url_v_c).json()
            except Exception as e:
                # Log the error and retry the request
                print(f"Error making request: {e}") 
                
            if 'error' in response:
                # Log the error and retry the request
                print(f"API error: {response['error']['message']}")
                
                
            # Initialize temp_df inside the loop
            temp_df = pd.DataFrame(columns=['video_id','comment_desc','comment_publish'])
            for c in response_c['items']:
                video_id = c['snippet']['videoId']
                comment_desc = c['snippet']['topLevelComment']['snippet']['textDisplay']
                temp_df = temp_df.append({'video_id':video_id,
                                         'comment_desc':comment_desc}, ignore_index=True)
            # Append temp_df to comment_df after the inner loop
            comment_df = comment_df.append(temp_df, ignore_index=True)
        return comment_df


                
        


