from distutils.command.upload import upload
import requests
import pandas as pd
import time

api_key = "THIS IS WHERE API KEY GOES"

channel_id = "UC16niRr50-MSBwiO3YDb3RA"


def get_details_video(video_id):
        #collecting view, likes     
        url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+api_key
        response_video_stats = requests.get(url_video_stats).json()

        view_count = response_video_stats['items'][0]['statistics']['viewCount']
        like_count = response_video_stats['items'][0]['statistics']['likeCount']

        return view_count, like_count



def get_videos(df):
#make the API call 
    pageToken = ""
    url = "https://www.googleapis.com/youtube/v3/search?key="+api_key+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=10000&"+pageToken

    response = requests.get(url).json()
    time.sleep(1)


    for video in response["items"]:
        if video["id"]["kind"] == "youtube#video":
            video_id = video["id"]["videoId"]
            video_title = video["snippet"]["title"]
            upload_date = video["snippet"]['publishedAt']
            upload_date = str(upload_date).split("T")[0]

            view_count, like_count = get_details_video(video_id)

            #save the data into the dataframe created above
            df = df.append({
                "video_id": video_id,
                "video_title":video_title,
                "upload_date":upload_date,
                "view_count":view_count,
                "like_count":like_count},
                ignore_index=True)
    return df




# this is to build the dataframe. 
df = pd.DataFrame(columns=["video_id","video_title","upload_date","view_count","like_count"])   

df = get_videos(df)

print(df)