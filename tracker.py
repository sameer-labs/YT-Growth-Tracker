import os
import csv
import requests
from datetime import datetime

# -----------
# FETCH API
# -----------

class YouTubeGrowthTracker:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set YOUTUBE_API_KEY env var or pass it directly.")
        self.base_url = "https://www.googleapis.com/youtube/v3"

    # -----------
    # CHANNEL STATS
    # -----------

    def get_channel_stats(self, channel_id):
        url = f"{self.base_url}/channels"
        params = {
            "part": "statistics,snippet,contentDetails",
            "id": channel_id,
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return None
            
            data = response.json()

            if data.get("pageInfo", {}).get("totalResults", 0) == 0:
                print(f"⚠️  No channel found with ID: {channel_id}")
                return None

            channel = data["items"][0]
            stats = channel["statistics"]
            snippet = channel["snippet"]  

            return {
                "channel_id": channel_id,
                "channel_name": snippet["title"],
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "videos": int(stats.get("videoCount", 0)),
                "timestamp": datetime.now().isoformat() 
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")  
            return None
        except Exception as e:
            print(f"❌ Error fetching channel stats: {str(e)}")
            return None
        
    # -----------
    # VIDEO STATS
    # -----------

    def get_recent_videos(self, channel_id, max_results=10):
        search_url = f"{self.base_url}/search"
        search_params = {
            "part": "id",
            "channelId": channel_id,  # FIXED: was "channel id" with a space
            "order": "date",
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key
        }

        try:
            search_response = requests.get(search_url, params=search_params)

            if search_response.status_code != 200:
                print(f"❌ Search API Error {search_response.status_code}")
                return []
            
            search_data = search_response.json()
            
            if not search_data.get("items"):
                return []
            
            video_ids = [item["id"]["videoId"] for item in search_data["items"]]

            videos_url = f"{self.base_url}/videos"
            video_params = {
                "part": "statistics,snippet",
                "id": ",".join(video_ids),
                "key": self.api_key
            }

            videos_response = requests.get(videos_url, params=video_params)

            if videos_response.status_code != 200:
                print(f"❌ Videos API Error {videos_response.status_code}")
                return []
            
            videos_data = videos_response.json()
            
            videos = []
            for video in videos_data.get('items', []):
                stats = video['statistics']
                snippet = video['snippet']
                
                videos.append({
                    'video_id': video['id'],
                    'title': snippet['title'],
                    'published_at': snippet['publishedAt'],
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0))
                })
            return videos
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Error fetching videos: {str(e)}")
            return []
    
    # -----------
    # ENGAGEMENT RATE
    # -----------    

    def calculate_engagement_rate(self, video_stats):
        """Calculate engagement rate (likes + comments) / views"""
        if not video_stats or video_stats["views"] == 0:
            return 0.0
        return ((video_stats['likes'] + video_stats['comments']) / video_stats['views']) * 100

    # -----------
    # COMPARISON
    # -----------

    def compare_channels(self, channel_ids):
        results = []

        for channel_id in channel_ids:
            print(f"🔍 Fetching data for channel: {channel_id}")
            channel_stats = self.get_channel_stats(channel_id)

            if not channel_stats:
                print(f"⏭️  Skipping {channel_id} - could not fetch stats\n")
                continue
        
            recent_videos = self.get_recent_videos(channel_id, max_results=10)

            if recent_videos:
                avg_views = sum(v['views'] for v in recent_videos) / len(recent_videos)
                avg_engagement = sum(self.calculate_engagement_rate(v) for v in recent_videos) / len(recent_videos)

                upload_dates = []
                for v in recent_videos:
                    date_str = v['published_at'].replace('Z', '+00:00')
                    upload_dates.append(datetime.fromisoformat(date_str))

                if len(upload_dates) >= 2:
                    days_diff = (upload_dates[0] - upload_dates[-1]).days
                    upload_frequency = len(recent_videos) / max(days_diff, 1) if days_diff > 0 else len(recent_videos)
                else:
                    upload_frequency = 0
            else:
                avg_views = 0
                avg_engagement = 0
                upload_frequency = 0

            results.append({
                **channel_stats,
                'avg_views_per_video': avg_views,
                'avg_engagement_rate': avg_engagement,
                'upload_frequency_per_day': upload_frequency,
                'recent_video_count': len(recent_videos)
            })
            
            print(f"✅ Completed: {channel_stats['channel_name']}\n")
        
        return results

    # -----------
    # WRITE CSV
    # -----------      

    def export_to_csv(self, data, filename="channel_comparison.csv"):  # FIXED: was "comparsion"
        if not data:
            print("❌ No data to export")
            return
     
        fieldnames = data[0].keys()

        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"✅ Data exported to {filename}")  # FIXED: indentation
        except Exception as e:
            print(f"❌ Error exporting to CSV: {str(e)}")

# -----------
# MAIN CTRL
# ----------- 

def main():

    print("🚀 YouTube Growth Tracker")
    print("=" * 50)
    print() 

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        print("Set YOUTUBE_API_KEY environment variable or add it to your code")
        return     
    
    tracker = YouTubeGrowthTracker(api_key)

    channels_to_compare = [
        'UCkzzNLnuM-VsATWC53ehwOQ',  # FlameFrags
        'UCvYPobTo42NM36X7VC4dLhA'   # Wemmbu
    ]

    comparison_data = tracker.compare_channels(channels_to_compare)

    if comparison_data:
        print("\n📊 Comparison Results:")
        print("=" * 50)
        for channel in sorted(comparison_data, key=lambda x: x['subscribers'], reverse=True):
            print(f"\n🎯 {channel['channel_name']}")
            print(f"   Subscribers: {channel['subscribers']:,}")
            print(f"   Total Views: {channel['total_views']:,}")
            print(f"   Videos: {channel['videos']}")
            print(f"   Avg Views/Video: {channel['avg_views_per_video']:,.0f}")
            print(f"   Engagement Rate: {channel['avg_engagement_rate']:.2f}%")
            print(f"   Upload Freq: {channel['upload_frequency_per_day']:.2f} videos/day")
        
        print("\n" + "=" * 50)
        tracker.export_to_csv(comparison_data)
    else:
        print("\n❌ No data retrieved. Check your API key and channel IDs.")


if __name__ == '__main__':
    main()