from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Review, Podcast, User, Playlist, Episode, Category, Author


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


# TODO: implement all the abstract methods with real codes in this class
class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()


    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f"Podcast {podcast_id} was not found.")

        return podcast


    def get_podcasts_by_id(self, id_list: list) -> List[Podcast]:
        podcast_list = []
        for podcast_id in id_list:
            podcast = None
            try:
                query = self._session_cm.session.query(Podcast).filter(Podcast._id == podcast_id)
                podcast = query.one()
            except NoResultFound:
                print(f"Podcast {podcast_id} was not found.")
            podcast_list.append(podcast)

        return podcast_list


    def get_podcasts_by_page(self, page: int, page_size: int) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return podcasts[start_index:end_index]


    def get_number_of_podcasts(self) -> int:
        podcasts = self._session_cm.session.query(Podcast).all()
        return len(podcasts)

    def get_podcasts_ids_for_category(self, category_name: str) -> List[int]:
        podcasts = self._session_cm.session.query(Podcast).all()
        category_podcast_ids = []
        for podcast in podcasts:
            for category in podcast.categories
                if category_name == category.name:
                    category_podcast_ids.append(podcast.id)

        return category_podcast_ids

    def has_next_page(self, current_page: int, page_size: int) -> bool:
        number_of_podcasts = self.get_number_of_podcasts()
        return current_page * page_size < number_of_podcasts

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

    def get_categories(self) -> List[Category]:
        pass

    def add_episode(self, episode: Episode):
        pass

    def get_number_of_episodes(self) -> int:
        pass

    def get_episode(self, episode_id: int) -> Episode:
        pass

    def add_author(self, author: Author):
        pass

    def add_category(self, category: Category):
        pass

    def add_user(self, username: str, password: str):
        pass

    def get_user(self, username: str) -> User:
        pass

    def get_podcasts_by_category(self, category_query: str) -> list:
        pass

    def get_podcasts_by_title(self, title: str) -> list:
        pass

    def get_podcasts_by_author(self, author: str) -> list:
        pass

    def add_to_playlist(self, username: str, episode: Episode):
        pass

    def get_users_playlist(self, username: str) -> Playlist:
        pass

    def add_review(self, podcast: Podcast, user: User, rating: int, description: str):
        pass

    def get_users_reviews(self, username: str) -> List[Review]:
        pass

    def delete_review(self, review_id: int):
        pass
