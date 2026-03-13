import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.cm as cm

#Load the data
df = pd.read_csv("https://raw.githubusercontent.com/abhisyanth1701/spotify-analytics/master/data/dataset.csv")
df=df.dropna()
df = df.drop_duplicates()

#Dashboard title
st.title("🎵🎶Spotify Music Trends Analyzer")
st.markdown("Analysing trends, genres and features and the moods of 114,000 songs!")

#section 1- Top 10 Most popular songs
st.header("📊📊Top 10 Most Popular Songs")

top10=df.sort_values("popularity", ascending=False).drop_duplicates(subset="track_name").head(10)

fig, ax=plt.subplots(figsize=(10,6))
sns.barplot(data=top10,x="popularity",y="track_name",hue="track_name",palette="Blues_d",legend=False,ax=ax)
ax.set_title("Top 10 Most Popular Songs")
ax.set_xlabel("Popularity Score")
ax.set_ylabel("Track Name")
plt.tight_layout()
st.pyplot(fig)

# Section 2 - Genre vs Music Features
st.header("📊 Genre vs Music Features")

top_genres = df["track_genre"].value_counts().head(10).index
df_genres = df[df["track_genre"].isin(top_genres)]
genre_features = df_genres.groupby("track_genre")[["energy", "danceability", "acousticness"]].mean()

fig2, ax2 = plt.subplots(figsize=(12, 6))
genre_features.plot(kind="bar", colormap="Set2", ax=ax2)
ax2.set_title("Average Music Features by Genre")
ax2.set_xlabel("Genre")
ax2.set_ylabel("Average Score (0-1)")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

# Section 3 - Mood by Genre
st.header("📊 Mood (Valence) by Genre")

genre_mood = df_genres.groupby("track_genre")["valence"].mean().sort_values()
colors = cm.plasma(np.linspace(0, 1, len(genre_mood)))

fig3, ax3 = plt.subplots(figsize=(10, 6))
genre_mood.plot(kind="barh", color=colors, ax=ax3)
ax3.set_title("Average Mood (Valence) by Genre")
ax3.set_xlabel("Valence Score (0=Sad, 1=Happy)")
ax3.set_ylabel("Genre")
plt.tight_layout()
st.pyplot(fig3)# Section 2 - Genre vs Music Features
st.header("📊 Genre vs Music Features")

top_genres = df["track_genre"].value_counts().head(10).index
df_genres = df[df["track_genre"].isin(top_genres)]
genre_features = df_genres.groupby("track_genre")[["energy", "danceability", "acousticness"]].mean()

fig2, ax2 = plt.subplots(figsize=(12, 6))
genre_features.plot(kind="bar", colormap="Set2", ax=ax2)
ax2.set_title("Average Music Features by Genre")
ax2.set_xlabel("Genre")
ax2.set_ylabel("Average Score (0-1)")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

# Section 3 - Mood by Genre
st.header("📊 Mood (Valence) by Genre")

genre_mood = df_genres.groupby("track_genre")["valence"].mean().sort_values()
colors = cm.plasma(np.linspace(0, 1, len(genre_mood)))

fig3, ax3 = plt.subplots(figsize=(10, 6))
genre_mood.plot(kind="barh", color=colors, ax=ax3)
ax3.set_title("Average Mood (Valence) by Genre")
ax3.set_xlabel("Valence Score (0=Sad, 1=Happy)")
ax3.set_ylabel("Genre")
plt.tight_layout()
st.pyplot(fig3)