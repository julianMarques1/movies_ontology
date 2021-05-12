from src.movie import Movie
from src.birdify import graph_from_tp1
from src.metadata import Metadata
from functools import reduce
from shutil import copy
from os import getcwd
from os.path import join, isdir


class Scraper(object):
    def scrape(self, urls_list):
        """Parse structured data from a list of pages."""

        if isinstance(urls_list, list):
            for urls in urls_list:
                self.scrape_movie(urls)
        else:
            self.scrape_movie(urls_list)

    def scrape_movie(self, urls):
        if isinstance(urls, list) and len(urls) > 1:
            movie_graph = reduce(
                lambda graph, another_graph: graph + another_graph,
                [
                    Movie(Metadata(url).get_json_dl())
                    .normalize(url)
                    .to_graph()
                    for url in urls
                ],
            )
        else:
            movie_graph = Movie(Metadata(urls).get_json_dl()).to_graph()

        with open(
            join(getcwd(), "data", "tp1.json"),
            "r",
            encoding="utf8",
        ) as file:
            movie = movie_graph + graph_from_tp1(file)
            file.close()

        self.save_movie(movie)
        return movie

    def save_movie(self, movie):
        copy(
            join(getcwd(), "data", "movie.owl"),
            join(getcwd(), "data", "output.owl"),
        )
        with open(
            join(getcwd(), "data", "output.owl"),
            "a",
            encoding="utf8",
        ) as file:
            file.write(movie.serialize(format="turtle").decode("utf-8"))
            file.close()