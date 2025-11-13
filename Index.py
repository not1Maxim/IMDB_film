import webbrowser
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator

file_path = "IMDB-Movie-Data.csv"
df = pd.read_csv(file_path)

df["Rating"].fillna(0.1, inplace=True)
df["Genre"] = df["Genre"].str.split(",")

df_exploded = df.explode("Genre")
df_exploded["Genre"] = df_exploded["Genre"].str.strip()

genres = sorted(df_exploded["Genre"].dropna().unique())
genre_top5_sum = {}

for genre in genres:
    top_movies = (
        df_exploded[df_exploded["Genre"] == genre]
        .sort_values(by="Rating", ascending=False)
        .head(5)
    )
    total_rating = top_movies["Rating"].sum()
    genre_top5_sum[genre] = total_rating

plt.figure(figsize=(12, 6))
bars = plt.bar(genre_top5_sum.keys(), genre_top5_sum.values(), color="skyblue")
max_genre = max(genre_top5_sum, key=genre_top5_sum.get)
bars[genres.index(max_genre)].set_color("orange")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("chart.png", bbox_inches="tight")
plt.close()

translation = {
    "Action": "Бойовик",
    "Adventure": "Пригоди",
    "Animation": "Анімація",
    "Biography": "Біографія",
    "Comedy": "Комедія",
    "Crime": "Кримінал",
    "Drama": "Драма",
    "Family": "Сімейний",
    "Fantasy": "Фентезі",
    "History": "Історичний",
    "Horror": "Жахи",
    "Music": "Музика",
    "Musical": "Мюзикл",
    "Mystery": "Містика",
    "Romance": "Романтика",
    "Sci-Fi": "Наукова фантастика",
    "Sport": "Спорт",
    "Thriller": "Трилер",
    "War": "Військовий",
    "Western": "Вестерн",
}

genres_ua = list(translation.values())
genres_ua.append("Діаграма рейтингів жанрів")

translator = GoogleTranslator(source="en", target="uk")

def translate_title(title):
    try:
        return translator.translate(title)
    except Exception:
        return title

html = """<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <title>Сайт за жанрами фільмів</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #ffe6f2;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    header {
      background-color: #ff66b2;
      color: white;
      text-align: center;
      width: 100%;
      padding: 20px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    h1 { margin: 0; font-size: 2em; }
    .buttons {
      margin-top: 40px;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 15px;
      max-width: 900px;
    }
    .btn {
      background-color: #ff99cc;
      border: none;
      color: white;
      padding: 12px 24px;
      font-size: 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s, transform 0.2s;
      text-decoration: none;
      display: inline-block;
    }
    .btn:hover {
      background-color: #ff66b2;
      transform: scale(1.05);
    }
    footer {
      margin-top: 60px;
      padding: 20px;
      color: #555;
    }
  </style>
</head>
<body>
  <header>
    <h1>Топ фільмів кожного жанру IMDB</h1>
  </header>

  <div class="buttons">
"""

for i, genre in enumerate(genres_ua, start=1):
    html += f'    <button class="btn" onclick="window.location.href=\'page{i}.html\'">{genre}</button>\n'

html += """  </div>
  <footer style="text-align:center; margin-top:60px; padding:20px; color:#555;">
  <p style="font-weight:bold; color:#ff66b2;">!!!Увага!!!</p>
    <p>Назви фільмів на постерах не завжди відповідають перекладу оригінальних назв</p>
    <p>Дякуємо за розуміння</p>
    <p>За нерозуміння подяки не чекайте</p>
  </footer>
</body>
</html>
"""
Path("index.html").write_text(html, encoding="utf-8")

for i, (eng_genre, ua_genre) in enumerate(zip(genres, genres_ua), start=1):
    if ua_genre == "Діаграма рейтингів жанрів":
        content = f"""
<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>{ua_genre}</title>
<style>
.btn {{
  background-color: #ff99cc;
  border: none;
  color: white;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  text-decoration: none;
  display: inline-block;
}}
.btn:hover {{
  background-color: #ff66b2;
  transform: scale(1.05);
}}
</style>
</head>
<body style="font-family:Arial; background:#ffe6f2; text-align:center; padding:50px;">
  <h1>{ua_genre}</h1>
  <img src="chart.png" alt="Діаграма рейтингів жанрів" style="max-width:90%; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.2);">
  <a href="index.html" class="btn">Назад</a>
</body>
</html>
"""
    else:
        top_movies = (
            df_exploded[df_exploded["Genre"] == eng_genre]
            .sort_values(by="Rating", ascending=False)
            .head(5)
        )

        movies_html = "<div style='display:flex; flex-wrap:wrap; justify-content:center; gap:20px; max-width:1000px; margin:auto;'>"
        for _, row in top_movies.iterrows():
            uk_title = translate_title(row["Title"])

            if row["Title"] == "The Dark Knight":
                poster_path = "The_Dark_Knight.webp"
            elif row["Title"] == "Inception":
                poster_path = "Inception.jpg"
            elif row["Title"] == "Dangal":
                poster_path = "Dangal.jpg"
            elif row["Title"] == "The Dark Knight Rises":
                poster_path = "The_Dark_Knight_Rises.webp"
            elif row["Title"] == "Bahubali: The Beginning":
                poster_path = "Bahubali_The_Beginning.webp"
            elif row["Title"] == "Interstellar":
                poster_path = "Interstellar.webp"
            elif row["Title"] == "WALL·E":
                poster_path = "WALL·E.webp"
            elif row["Title"] == "Inglourious Basterds":
                poster_path = "Inglourious_Basterds.png"
            elif row["Title"] == "Kimi no na wa":
                poster_path = "Kimi_no_na_wa.webp"
            elif row["Title"] == "Koe no katachi":
                poster_path = "Koe_no_katachi.webp"
            elif row["Title"] == "Toy Story 3":
                poster_path = "Toy_Story_3.webp"
            elif row["Title"] == "Up":
                poster_path = "Up.webp"
            elif row["Title"] == "The Intouchables":
                poster_path = "The_Intouchables.jpg"
            elif row["Title"] == "Hacksaw Ridge":
                poster_path = "Hacksaw_Ridge.webp"
            elif row["Title"] == "The Wolf of Wall Street":
                poster_path = "The_Wolf_of_Wall_Street.jpg"
            elif row["Title"] == "Into the Wild":
                poster_path = "Into_the_Wild.jpg"
            elif row["Title"] == "3 Idiots":
                poster_path = "3_Idiots.webp"
            elif row["Title"] == "La La Land":
                poster_path = "La_La_Land.webp"
            elif row["Title"] == "The Departed":
                poster_path = "The_Departed.png"
            elif row["Title"] == "Gone Girl":
                poster_path = "Gone_Girl.jpg"
            elif row["Title"] == "No Country for Old Men":
                poster_path = "No_Country_for_Old_Men.webp"
            elif row["Title"] == "Taare Zameen Par":
                poster_path = "Taare_Zameen_Par.webp"
            elif row["Title"] == "Hachi: A Dog's Tale":
                poster_path = "Hachi_A_Dog's_Tale.webp"
            elif row["Title"] == "Kubo and the Two Strings":
                poster_path = "Kubo_and_the_Two_Strings.webp"
            elif row["Title"] == "Pan's Labyrinth":
                poster_path = "Pan's_Labyrinth.jpg"
            elif row["Title"] == "Star Wars: Episode VII - The Force Awakens":
                poster_path = "Star_Wars_Episode_VII-The_Force_Awakens.webp"
            elif row["Title"] == "Harry Potter and the Deathly Hallows: Part 2":
                poster_path = "Harry_Potter_and_the_Deathly_Hallows_Part_2.jpg"
            elif row["Title"] == "The Hobbit: An Unexpected Journey":
                poster_path = "The_Hobbit_An_Unexpected_Journey.webp"
            elif row["Title"] == "12 Years a Slave":
                poster_path = "12_Years_a_Slave.jpg"
            elif row["Title"] == "There Will Be Blood":
                poster_path = "There_Will_Be_Blood.webp"
            elif row["Title"] == "Spotlight":
                poster_path = "Spotlight.webp"
            elif row["Title"] == "Straight Outta Compton":
                poster_path = "Straight_Outta_Compton.webp"
            elif row["Title"] == "Twin Peaks: The Missing Pieces":
                poster_path = "Twin_Peaks_The_Missing_Pieces.webp"
            elif row["Title"] == "Zombieland":
                poster_path = "Zombieland.webp"
            elif row["Title"] == "What We Do in the Shadows":
                poster_path = "What_We_Do_in_the_Shadows.webp"
            elif row["Title"] == "Grindhouse":
                poster_path = "Grindhouse.jpg"
            elif row["Title"] == "Busanhaeng":
                poster_path = "Busanhaeng.jpg"
            elif row["Title"] == "Whiplash":
                poster_path = "Whiplash.webp"
            elif row["Title"] == "Sing Street":
                poster_path = "Sing_Street.jpg"
            elif row["Title"] == "August Rush":
                poster_path = "August_Rush.webp"
            elif row["Title"] == "Les Misérables":
                poster_path = "Les_Misérables.webp"
            elif row["Title"] == "Sweeney Todd: The Demon Barber of Fleet Street":
                poster_path = "Sweeney_Todd_The_Demon_Barber_of_Fleet_Street.webp"
            elif row["Title"] == "Across the Universe":
                poster_path = "Across_the_Universe.webp"
            elif row["Title"] == "Mamma Mia!":
                poster_path = "Mamma_Mia!.webp"
            elif row["Title"] == "Rock of Ages":
                poster_path = "Rock_of_Ages.webp"
            elif row["Title"] == "The Prestige":
                poster_path = "The_Prestige.webp"
            elif row["Title"] == "Incendies":
                poster_path = "Incendies.jpg"
            elif row["Title"] == "El secreto de sus ojos":
                poster_path = "El_secreto_de_sus_ojos.jpg"
            elif row["Title"] == "Ah-ga-ssi":
                poster_path = "Ah-ga-ssi.webp"
            elif row["Title"] == "Shutter Island":
                poster_path = "Shutter_Island.jpg"
            elif row["Title"] == "PK":
                poster_path = "PK.jpg"
            elif row["Title"] == "The Perks of Being a Wallflower":
                poster_path = "The_Perks_of_Being_a_Wallflower.webp"
            elif row["Title"] == "Guardians of the Galaxy":
                poster_path = "Guardians_of_the_Galaxy.webp"
            elif row["Title"] == "The Avengers":
                poster_path = "The_Avengers.webp"
            elif row["Title"] == "Warrior":
                poster_path = "Warrior.webp"
            elif row["Title"] == "The Blind Side":
                poster_path = "The_Blind_Side.webp"
            elif row["Title"] == "Creed":
                poster_path = "Creed.webp"
            elif row["Title"] == "Moneyball":
                poster_path = "Moneyball.jpg"
            elif row["Title"] == "42":
                poster_path = "42.webp"
            elif row["Title"] == "The Lives of Others":
                poster_path = "The_Lives_of_Others.webp"
            elif row["Title"] == "Relatos salvajes":
                poster_path = "Relatos_salvajes.jpg"
            elif row["Title"] == "The Imitation Game":
                poster_path = "The_Imitation_Game.webp"
            elif row["Title"] == "The Boy in the Striped Pyjamas":
                poster_path = "The_Boy_in_the_Striped_Pyjamas.jpg"
            elif row["Title"] == "300":
                poster_path = "300.webp"
            elif row["Title"] == "Django Unchained":
                poster_path = "Django_Unchained.webp"
            elif row["Title"] == "True Grit":
                poster_path = "True_Grit.webp"
            elif row["Title"] == "Brimstone":
                poster_path = "Brimstone.webp"
            elif row["Title"] == "The Magnificent Seven":
                poster_path = "The_Magnificent_Seven.webp"
            elif row["Title"] == "The Lone Ranger":
                poster_path = "The_Lone_Ranger.webp"
            elif row["Title"] == "Ratatouille":
                poster_path = "Ratatouille.webp"

            movies_html += f"""
            <div style='background:white; border-radius:12px; padding:15px; width:28%; 
                        box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;'>
                <img src="{poster_path}" alt="Афіша фільму {row["Title"]}" 
                     style="width:100%; border-radius:10px; margin-bottom:10px;">
                
                <h2 style='color:#ff66b2;'>{row["Title"]}</h2>
                <h3 style='color:#555;'>{uk_title}</h3>
                <p style='font-size:20px; color:#000; margin-top:5px;'>{row["Rating"]}</p>
            </div>
            """
        movies_html += "</div>"

        content = f"""
<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>{ua_genre}</title>
<style>
.btn {{
  background-color: #ff99cc;
  border: none;
  color: white;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  text-decoration: none;
  display: inline-block;
}}
.btn:hover {{
  background-color: #ff66b2;
  transform: scale(1.05);
}}
</style>
</head>
<body style="font-family:Arial; background:#ffe6f2; text-align:center; padding:50px;">
  <h1>{ua_genre}</h1>
  {movies_html}
  <a href="index.html" class="btn" style="margin-top:40px;">⬅ Назад на головну</a>
</body>
</html>
"""
    Path(f"page{i}.html").write_text(content, encoding="utf-8")

webbrowser.open_new_tab(Path("index.html").resolve().as_uri())