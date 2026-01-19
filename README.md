# 📈 YouTube Growth Tracker

Dead simple YouTube channel comparison tool. No BS predictions, no ML magic—just raw API data turned into actionable insights.

Built this because I got tired of manually tracking channel metrics across competitors. Now it's yours.

## 🎯 What It Does

- Compares subscriber counts, views, and video performance across multiple channels
- Calculates engagement rates (likes + comments / views)
- Tracks upload frequency patterns
- Exports everything to CSV for your own analysis

Perfect for:
- Content creators tracking competition
- Agencies managing multiple channels
- Anyone who needs "who's growing faster?" answers

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials))

### Installation

```bash
# Clone it
git clone https://github.com/yourusername/youtube-growth-tracker.git
cd youtube-growth-tracker

# Install deps (just requests, that's it)
pip install -r requirements.txt

# Set your API key as an environment variable
export YOUTUBE_API_KEY="your_api_key_here"

# Or on Windows
set YOUTUBE_API_KEY=your_api_key_here
```

### Usage

```python
from tracker import YouTubeGrowthTracker
import os

tracker = YouTubeGrowthTracker(os.getenv('YOUTUBE_API_KEY'))

channels = [
    'UC_x5XG1OV2P6uZZ5FSM9Ttw',  # Channel 1
    'UCXuqSBlHAE6Xw-yeJA0Tunw',  # Channel 2
]

data = tracker.compare_channels(channels)
tracker.export_to_csv(data, 'my_comparison.csv')
```

Or just run the example:

```bash
python tracker.py
```

## 📊 What You Get

```
🎯 MrBeast
   Subscribers: 245,000,000
   Total Views: 42,000,000,000
   Videos: 741
   Avg Views/Video: 85,234,567
   Engagement Rate: 4.23%
   Upload Freq: 0.25 videos/day
```

Plus a CSV with all the data for deeper analysis.

## 🛠️ Features

### Safety First
- HTTP status code checking on all API calls (200 = good, anything else = error handling)
- Graceful error handling (no crashes on bad channel IDs)
- Network timeout protection
- Rate limit friendly (doesn't spam the API)

### Built-In Metrics
- Subscriber count tracking
- Average views per video (recent uploads)
- Engagement rate calculation
- Upload frequency analysis
- Total channel stats

## 🔑 API Key Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing)
3. Enable YouTube Data API v3
4. Create credentials → API Key
5. Set as an environment variable

**Free tier**: 10,000 quota units/day (enough for ~100 channel comparisons)

## 📦 Dependencies

Just the essentials:
- `requests` - For API calls (that's literally it)
- `os`, `csv`, `datetime` - Built into Python

No bloat. No unnecessary packages.

## 📝 Notes

- Uses standard `requests.get()` with proper status code checks
- YouTube API endpoints: `/channels`, `/videos`, `/search`
- Quota cost: ~18 units per channel comparison
- Recent videos = last 10 uploads (configurable)
- Timestamps are in ISO format for easy tracking over time

## 🤝 Contributing

Found a bug? Want a feature? PRs welcome. Keep it simple, though—this tool does one thing well.

## 📄 License

MIT - Do whatever you want with it.

## 💡 Ideas for Extension

- Add matplotlib charts for visual comparison
- Historical tracking (save snapshots over time)
- Growth rate calculations (week-over-week, month-over-month)
- Automated reporting
- Multi-platform support (TikTok, Instagram, etc.)

Built with ☕ by a dev who believes in shipping useful tools, not vaporware.

---

**Questions?** Open an issue. I actually read them.
