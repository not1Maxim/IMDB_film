import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('IMDB-Movie-Data.csv')

df['Rating'].fillna(0.1, inplace=True)
df['Genre'] = df['Genre'].str.split(',')

df_exploded = df.explode('Genre')
df_exploded['Genre'] = df_exploded['Genre'].str.strip()

genres = sorted(df_exploded['Genre'].dropna().unique())
genre_top5_sum = {}

for genre in genres:
    top_movies = df_exploded[df_exploded['Genre'] == genre].sort_values(by='Rating', ascending=False).head(5)
    total_rating = top_movies['Rating'].sum()
    genre_top5_sum[genre] = total_rating

plt.figure(figsize=(12, 6))
bars = plt.bar(genre_top5_sum.keys(), genre_top5_sum.values(), color='skyblue')

max_genre = max(genre_top5_sum, key=genre_top5_sum.get)
bars[genres.index(max_genre)].set_color('orange')

for genre in genres:
    print(f"\nП’ять найкращих фільмів жанру '{genre}':")
    top_movies = df_exploded[df_exploded['Genre'] == genre].sort_values(by='Rating', ascending=False).head(5)
    shown_titles = set()
    for _, row in top_movies.iterrows():
        if row['Title'] not in shown_titles:
            print(f"{row['Title']} — рейтинг {row['Rating']}")
            shown_titles.add(row['Title'])

plt.xlabel('Жанр')
plt.ylabel('Сума рейтингів топ-5 фільмів')
plt.title('Сума рейтингів топ-5 фільмів у кожному жанрі')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()