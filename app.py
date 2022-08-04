from flask import Flask, render_template, request
import scraper
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/movies/', methods=['GET'])
def movies():
    return render_template('movies.html')

@app.route('/movies/recommendations/', methods=['POST'])
def movieRecommendations():
    formData = request.form
    genres = formData.getlist("genres")
    ratings = formData.getlist("ratings")
    platforms = formData.getlist("platforms")
    tomatometerScore = int(formData["tomatometerSlider"])
    audienceScore = int(formData["audienceSlider"])
    limit = 10 if formData["limit"] == "" else int(formData["limit"])
    popular = True if "popular" in formData else False

    URLs = scraper.generateMovieURLs(
        genres, ratings, platforms, tomatometerScore, audienceScore, limit, popular
    )
    task = scraper.scrapeMovies.delay(
        URLs, tomatometerScore, audienceScore, limit
    )
    movieInfo = task.wait()
   
    if len(movieInfo[0]) == 0:
        return render_template("movieNotFound.html")

    return render_template("movieRecommendations.html", movieInfo=movieInfo)

@app.route('/tvshows/', methods=['GET'])
def tvshows():
    return render_template('tvshows.html')

@app.route('/tvshows/recommendations/', methods=['POST'])
def tvshowRecommendations():
    formData = request.form
    genres = formData.getlist("genres")
    ratings = formData.getlist("ratings")
    platforms = formData.getlist("platforms")
    tomatometerScore = int(formData["tomatometerSlider"])
    audienceScore = int(formData["audienceSlider"])
    limit = 10 if formData["limit"] == "" else int(formData["limit"])
    popular = True if "popular" in formData else False

    URLs = scraper.generateTVshowURLs(
        genres, ratings, platforms, tomatometerScore, audienceScore, limit, popular
    )
    tvShowInfo = q.enqueue(
        scraper.scrapeTVshows, URLs, tomatometerScore, audienceScore, limit
    )
    
    if len(tvShowInfo[0]) == 0:
        return render_template("tvshowNotFound.html")

    return render_template("tvshowRecommendations.html", tvShowInfo=tvShowInfo)

@app.route('/actor/', methods=['GET'])
def actor():
    return render_template('actor.html')

@app.route('/actor/recommendations/', methods=['POST'])
def actorRecommendations():
    formData = request.form

    roles = formData.getlist("role")
    if len(roles) == 0 or "all" in roles:
        roles = ["all"]
    genres = formData.getlist("genres")
    if len(genres) == 0 or "all" in genres:
        genres = ["all"]
    ratings = formData.getlist("ratings")
    if len(ratings) == 0 or "all" in ratings:
        ratings = ["all"]
    platforms = formData.getlist("platforms")
    if len(platforms) == 0 or "all" in platforms:
        platforms = ["all"]

    filterData = {
        "actorURL": formData["actorURL"],
        "category": formData["category"],
        "roles": roles,
        "oldestYear": int(formData["yearSlider"]),
        "boxOffice": int(formData["boxOffice"]),
        "genres": genres,
        "ratings": ratings,
        "platforms": platforms,
        "tomatometerScore": int(formData["tomatometerSlider"]),
        "audienceScore": int(formData["audienceSlider"]),
        "limit": 10 if formData["limit"] == "" else int(formData["limit"])
    }

    actorInfo = q.enqueue(scraper.scrapeActor, filterData)

    if actorInfo is None:
        return render_template("actorInvalid.html")
    
    if len(actorInfo[0]) == 0:
        return render_template("actorNotFound.html")

    return render_template("actorRecommendations.html", actorInfo=actorInfo)

@app.route('/director/', methods=['GET'])
def director():
    return render_template('director.html')

@app.route('/director/recommendations/', methods=['POST'])
def directorRecommendations():
    formData = request.form

    genres = formData.getlist("genres")
    if len(genres) == 0 or "all" in genres:
        genres = ["all"]
    ratings = formData.getlist("ratings")
    if len(ratings) == 0 or "all" in ratings:
        ratings = ["all"]
    platforms = formData.getlist("platforms")
    if len(platforms) == 0 or "all" in platforms:
        platforms = ["all"]

    filterData = {
        "url": formData["directorURL"],
        "category": formData["category"],
        "oldestYear": int(formData["yearSlider"]),
        "boxOffice": int(formData["boxOffice"]),
        "genres": genres,
        "ratings": ratings,
        "platforms": platforms,
        "tomatometerScore": int(formData["tomatometerSlider"]),
        "audienceScore": int(formData["audienceSlider"]),
        "limit": 10 if formData["limit"] == "" else int(formData["limit"])
    }

    directorInfo = q.enqueue(scraper.scrapeDirectorProducer, filterData, "director")

    if directorInfo is None:
        return render_template("directorInvalid.html")
    
    if len(directorInfo[0]) == 0:
        return render_template("directorNotFound.html")

    return render_template("directorRecommendations.html", directorInfo=directorInfo)

@app.route('/producer/', methods=['GET'])
def producer():
    return render_template('producer.html')

@app.route('/producer/recommendations/', methods=['POST'])
def producerRecommendations():
    formData = request.form

    genres = formData.getlist("genres")
    if len(genres) == 0 or "all" in genres:
        genres = ["all"]
    ratings = formData.getlist("ratings")
    if len(ratings) == 0 or "all" in ratings:
        ratings = ["all"]
    platforms = formData.getlist("platforms")
    if len(platforms) == 0 or "all" in platforms:
        platforms = ["all"]

    filterData = {
        "url": formData["producerURL"],
        "category": formData["category"],
        "oldestYear": int(formData["yearSlider"]),
        "boxOffice": int(formData["boxOffice"]),
        "genres": genres,
        "ratings": ratings,
        "platforms": platforms,
        "tomatometerScore": int(formData["tomatometerSlider"]),
        "audienceScore": int(formData["audienceSlider"]),
        "limit": 10 if formData["limit"] == "" else int(formData["limit"])
    }

    producerInfo = q.enqueue(scraper.scrapeDirectorProducer, filterData, "producer")

    if producerInfo is None:
        return render_template("producerInvalid.html")
    
    if len(producerInfo[0]) == 0:
        return render_template("producerNotFound.html")

    return render_template("producerRecommendations.html", producerInfo=producerInfo)

@app.route('/similar/', methods=['GET'])
def similar():
    return render_template('similar.html')

@app.route('/similar/recommendations/', methods=['POST'])
def similarRecommendations():
    formData = request.form

    platforms = formData.getlist("platforms")
    if len(platforms) == 0 or "all" in platforms:
        platforms = ["all"]

    filterData = {
        "url": formData["url"],
        "oldestYear": int(formData["yearSlider"]),
        "platforms": platforms,
        "tomatometerScore": int(formData["tomatometerSlider"]),
        "audienceScore": int(formData["audienceSlider"]),
        "limit": 10 if formData["limit"] == "" else int(formData["limit"])
    }

    similarInfo = q.enqueue(scraper.scrapeSimilar, filterData)

    if similarInfo is None:
        return render_template("similarInvalid.html")
    
    if len(similarInfo[0]) == 0:
        return render_template("similarNotFound.html")

    return render_template("similarRecommendations.html", similarInfo=similarInfo)