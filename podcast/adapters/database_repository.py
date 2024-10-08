from datetime import date
from typing import List, Type

from sqlalchemy import desc, asc, func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from podcast.domainmodel.model import User, Podcast, Category, Episode, Author, Review, Playlist
from podcast.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # Functions for Podcast
    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')

        return podcast
    def get_podcasts_by_id(self, id_list: list) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).filter(Podcast._id in id_list)
        return podcasts

    def get_podcasts_by_page(self, page_number: int, page_size: int) -> List[Podcast]:
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return self._session_cm.session.query(Podcast).all()[start_index:end_index]

    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    #HOW TO SIMPLIFY THIS USING FILTERING FUNCTION???
    def get_podcasts_ids_for_category(self, category_name: str) -> List[int]:
        podcasts = self._session_cm.session.query(Podcast).all()
        matching_podcast_ids = []
        for podcast in podcasts:
            if any(category.name == category_name for category in podcast.categories):
                matching_podcast_ids.append(podcast.id)
        return matching_podcast_ids

    # Functions for pagination
    def has_next_page(self, current_page: int, page_size: int) -> bool:
        total_podcasts = self.get_number_of_podcasts()
        return current_page * page_size < total_podcasts

    def has_previous_page(self, current_page: int) -> bool:
        return current_page > 1

    def get_next_page(self, current_page: int, page_size: int) -> int:
        if self.has_next_page(current_page, page_size):
            return current_page + 1
        return current_page

    def get_previous_page(self, current_page: int) -> int:
        if self.has_previous_page(current_page):
            return current_page - 1
        return current_page

    # Functions for Category
    def get_categories(self) -> list[Type[Category]]:
        categories = self._session_cm.session.query(Category).order_by(asc(Category._name)).all()
        return categories

    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.merge(category)
            scm.commit()

    # Functions for Episode
    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def get_number_of_episodes(self) -> int:
        return self._session.cm.session.query(Episode).count()

    def get_episode(self, episode_id: int) -> Episode:
        if episode_id <= len(self.get_number_of_episodes()):
            return self._session.cm.session.query(Episode).filter(Episode.__Episode__id == episode_id)
        return None

    # Functions for Author
    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.merge(author)
            scm.commit()


    # Functions for User
    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._username == username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user


    # Functions for Playlist
    def add_to_playlist(self, username: str, episode: Episode):
        user = self.get_user(username)
        if not user:
            raise ValueError(f'User {username} is not found!')
        if user.playlist is None:
            user.create_playlist(f"{username.title()}'s Playlist")
        user.playlist.add_episode(episode)

    def get_users_playlist(self, username: str):
        user = self.get_user(username)
        if not user:
            raise ValueError(f'User {username} is not found!')
        if user.playlist is None:
            user.create_playlist(f"{username.title()}'s Playlist")
        return user.playlist

    # Functions for Review
    def add_review(self, podcast: Podcast, user: User, rating: int, description: str):
        for review in user.reviews:
            if review.podcast.id == podcast.id:
                raise ValueError(f'You already reviewed this podcast. Please try another one!')
                new_review = Review(len(self.__reviews) + 1, podcast, user, rating, description)
                self.__reviews.append(new_review)
                user.add_review(new_review)
                podcast.add_review(new_review)

    def get_users_reviews(self, username: str):
        user = self.get_user(username)
        if not user:
            raise ValueError(f'User {username} is not found!')
        return sorted(user.reviews, key=lambda review: review.rating, reverse=True)

    def delete_review(self, review_id: int):
        for review in self.__reviews:
            if review.id == review_id:
                review.reviewer.remove_review(review)
                review.podcast.remove_review(review)
                self.__reviews.remove(review)


    # Functions for search - get podcasts by title, author, lanugage or category

    def get_podcasts_by_title(self, title_string: str) -> List[Podcast]:
        try:
            searched_podcasts = self._session_cm.session.query(Podcast). \
                filter(func.lower(Podcast._title).like(f"%{title_string.lower()}%")).all()
        except NoResultFound:
            print(f'Title {title_string} was not found')
            return []
        return searched_podcasts

    def get_podcasts_by_author(self, author_name: str) -> List[Podcast]:
        try:
            searched_podcasts = self._session_cm.session.query(Podcast).join(Author). \
                filter(func.lower(Author._name).like(f"%{author_name.lower()}%")).all()
        except NoResultFound:
            return []
        return searched_podcasts

    def get_podcasts_by_category(self, category_string: str) -> List[Podcast]:
        try:
            searched_podcasts = self._session_cm.session.query(Podcast).join(Podcast._categories).all()
            podcasts = []
            for podcast in searched_podcasts:
                for category in podcast.categories:
                    if category_string.lower() in category.name.lower():
                        podcasts.append(podcast)
        except NoResultFound:
            return []
        return podcasts

    def get_podcasts_by_language(self, language_string: str) -> List[Podcast]:
        try:
            searched_podcasts = self._session_cm.session.query(Podcast). \
                filter(func.lower(Podcast._language).like(f"%{language_string.lower()}%")).all()

        except NoResultFound:
            return []
        return searched_podcasts










