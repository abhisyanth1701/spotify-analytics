import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.cm as cm
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("https://raw.githubusercontent.com/abhisyanth1701/spotify-analytics/master/data/dataset.csv")
df = df.dropna()
df = df.drop_duplicates(subset=["track_id"])

#Train ML model
features=["danceability","energy","valence","tempo","acousticness","speechiness"]
x=df[features]
y=df["popularity"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(x, y)

st.title("🎵🎶Spotify Music Trends Analyzer")
st.markdown("Analysing trends, genres and features and the moods of 114,000 songs!")

st.header("📊 Top 10 Most Popular Songs")
top10 = df.sort_values("popularity", ascending=False).drop_duplicates(subset="track_name").head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top10, x="popularity", y="track_name", hue="track_name", palette="Blues_d", legend=False, ax=ax)
ax.set_title("Top 10 Most Popular Songs")
ax.set_xlabel("Popularity Score")
ax.set_ylabel("Track Name")
plt.tight_layout()
st.pyplot(fig)

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

st.header("🎶 Song popularity predictor")
st.markdown("Move the sliders and predict how popular your song will be!")

danceability = st.slider("Danceability",0.0,1.0,0.5)
energy = st.slider("Energy",0.0,1.0,0.5)
valence = st.slider("Valence (Mood)",0.0,1.0,0.5)
tempo = st.slider("Tempo(BPM)",50,200,120)
acousticness = st.slider("Acousticness",0.0,1.0,0.5)
speechiness = st.slider("Speechiness",0.0,1.0,0.5)

input_data=[[danceability,energy,valence,tempo,acousticness,speechiness]]
prediction=model.predict(input_data)
st.subheader(f"🎵 Predicted Popularity Score: {round(prediction[0])}/100")

st.header("🔍 Song Search")
st.markdown("Type a song name to explore its audio features.")

search_query = st.text_input("Search for a song", placeholder="e.g. Blinding Lights")

if search_query:
    results = df[df["track_name"].str.contains(search_query, case=False, na=False)].drop_duplicates(subset="track_name")
    if results.empty:
        st.warning("No songs found. Try a different name.")
    else:
        selected_name = st.selectbox("Select a song", results["track_name"].tolist())
        song = results[results["track_name"] == selected_name].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Artist:** {song['artists']}")
            st.markdown(f"**Genre:** {song['track_genre']}")
            st.markdown(f"**Popularity:** {song['popularity']}/100")
        with col2:
            st.markdown(f"**Tempo:** {round(song['tempo'])} BPM")
            st.markdown(f"**Duration:** {round(song['duration_ms'] / 60000, 2)} min")
            st.markdown(f"**Explicit:** {'Yes' if song['explicit'] else 'No'}")

        radar_features = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
        values = [song[f] for f in radar_features]
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(radar_features), endpoint=False).tolist()
        angles += angles[:1]

        fig_r, ax_r = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax_r.plot(angles, values, color="#1DB954", linewidth=2)
        ax_r.fill(angles, values, color="#1DB954", alpha=0.25)
        ax_r.set_xticks(angles[:-1])
        ax_r.set_xticklabels(radar_features, size=11)
        ax_r.set_ylim(0, 1)
        ax_r.set_title(f"{selected_name}", size=13, pad=15)
        st.pyplot(fig_r)