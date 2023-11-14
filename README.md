# Spotify Playlist Analysis Project

This project focuses on analyzing music playlists from Spotify using the Spotify API and various Python libraries such as pandas, aiohttp, asyncio, seaborn, and matplotlib.

## Overview

The goal of this project is to provide insights into user playlists by extracting and analyzing track features and artist information. Users input a Spotify playlist link, and the system processes the data, conducting analyses on track features and artists. The gathered data, with user consent, is stored in a database for further user-specific analysis.

## Features

- **Spotify API Integration:** Utilizes the Spotify API to retrieve information about tracks and artists from a given playlist link.
- **Data Analysis:** Employs pandas, seaborn, and matplotlib for in-depth analysis of track features and artist data.
- **Asynchronous Processing:** Utilizes aiohttp and asyncio to efficiently handle asynchronous tasks, ensuring a smooth user experience.
- **Database Integration:** Stores user data securely in a database, paving the way for additional user-specific analyses.
- **Predictive Modeling (Future Plan):** Aims to implement predictive models to anticipate the track features of the next song added to a playlist.

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/spotify-playlist-analysis.git
   cd spotify-playlist-analysis
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Spotify API:**
   - Obtain your Spotify API credentials and set them in the appropriate environment variables.

4. **Run the Application:**
   ```bash
   python main.py
   ```

5. **Input Spotify Playlist Link:**
   - Enter a Spotify playlist link in the provided form.

6. **Explore the Insights:**
   - Gain valuable insights into the track features and artists of the playlist.

## Future Plans

The future development of this project includes:

- **Predictive Models:** Implementing predictive models to forecast the track features of the next song added to a playlist.
- **Enhanced User Experience:** Incorporating additional features and visualizations for a more interactive and informative user experience.

Feel free to contribute, suggest improvements, or report issues. Happy analyzing! 🎵📊
