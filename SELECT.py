
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:******@localhost/postgres", encoding='UTF=8')

connection = engine.connect()


# количество исполнителей в каждом жанре ;

select_request = connection.execute("""
SELECT B.Название_жанра, COUNT (DISTINCT A.id_artist)
FROM Жанры_Исполнители A LEFT JOIN Жанры B
ON A.id_genre = B.id_genre
GROUP BY B.Название_жанра;
""").fetchall()

print('количество исполнителей в каждом жанре')
print(select_request)

# количество треков, вошедших в альбомы 2019-2020 годов;

select_request = connection.execute("""
SELECT COUNT(A.id_track)
FROM Треки A LEFT JOIN Альбомы B
ON A.id_album = B.id_album
WHERE B.Год_выпуска BETWEEN 2019 AND 2020;
""").fetchall()

print('количество треков, вошедших в альбомы 2019-2020 годов')
print(select_request)

# средняя продолжительность треков по каждому альбому;

select_request = connection.execute("""
SELECT B.Название_альбома, AVG(A.Длительность)
FROM Треки A LEFT JOIN Альбомы B
ON A.id_album = B.id_album
GROUP BY B.Название_альбома;
""").fetchall()

print('средняя продолжительность треков по каждому альбому')
print(select_request)


# все исполнители, которые не выпустили альбомы в 2020 году;

select_request = connection.execute("""
SELECT DISTINCT C.Имя
FROM Альбомы_Исполнители A LEFT JOIN Альбомы B
ON A.id_album = B.id_album
LEFT JOIN Исполнители C
ON A.id_artist = C.id_artist
WHERE B.Год_выпуска <> 2020;
""").fetchall()

print('количество треков, вошедших в альбомы 2019-2020 годов')
print(select_request)

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

select_request = connection.execute("""
SELECT DISTINCT A.id_collection
FROM Сборники_Треки A
LEFT JOIN Треки B
ON A.id_track = B.id_track
LEFT JOIN Альбомы C
ON B.id_album = C.id_album
LEFT JOIN Альбомы_Исполнители D
ON C.id_album = D.id_album
LEFT JOIN Исполнители E
ON D.id_artist = E.id_artist
WHERE E.Имя = 'Jakyl';
""").fetchall()

print('названия сборников, в которых присутствует конкретный исполнитель (выберите сами)')
print(select_request)

# название альбомов, в которых присутствуют исполнители более 1 жанра;

select_request = connection.execute("""
SELECT DISTINCT B.Название_альбома
FROM Альбомы_Исполнители A
LEFT JOIN Альбомы B
ON A.id_album = B.id_album
LEFT JOIN Исполнители C
ON A.id_artist = C.id_artist
LEFT JOIN (SELECT id_artist, COUNT(id_genre) AS GENRES
            FROM Жанры_Исполнители
            GROUP BY id_artist
            HAVING COUNT(id_genre) > 1) D
ON A.id_artist = D.id_artist
WHERE NOT D.GENRES IS NULL;
""").fetchall()

print('название альбомов, в которых присутствуют исполнители более 1 жанра')
print(select_request)

# наименование треков, которые не входят в сборники;

select_request = connection.execute("""
SELECT DISTINCT B.Название_трека
FROM Сборники_Треки A
JOIN Треки B
ON A.id_track <> B.id_track;
""").fetchall()

print('наименование треков, которые не входят в сборники')
print(select_request)

# исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);

select_request = connection.execute("""
SELECT B.Имя
FROM Альбомы_Исполнители A
LEFT JOIN Исполнители B
ON A.id_artist = B.id_artist
LEFT JOIN Альбомы C
ON A.id_album = C.id_album
LEFT JOIN Треки D
ON C.id_album = D.id_album
GROUP BY B.Имя , D.Длительность
HAVING D.Длительность = (SELECT MIN(Длительность) FROM Треки);
""").fetchall()

print('исполнителя(-ей), написавшего самый короткий по продолжительности трек ')
print(select_request)

# название альбомов, содержащих наименьшее количество треков.

select_request = connection.execute("""
SELECT DISTINCT B.Название_альбома, COUNT(id_track)
FROM Треки A
LEFT JOIN Альбомы B
ON A.id_album = B.id_album
GROUP BY B.Название_альбома
HAVING count(id_track) = (SELECT MAX(mycount)
FROM (SELECT B.Название_альбома, COUNT(id_track) mycount
FROM Треки A LEFT JOIN Альбомы B ON A.id_album = B.id_album
GROUP BY B.Название_альбома) foo);
""").fetchall()

print('название альбомов, содержащих наименьшее количество треков')
print(select_request)
