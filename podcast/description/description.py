from better_profanity import profanity
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import podcast.adapters.repository as repository
import podcast.description.services as services
import podcast.utilities.utilities as utilities
from podcast.authentication.authentication import login_required

description_blueprint = Blueprint('description_bp', __name__)


@description_blueprint.route('/description', methods=['GET'])
def show_description():
    podcast_id = request.args.get('podcast_id', default=1, type=int)
    form = ReviewForm()
    # Ensure podcast_id is within valid range
    if podcast_id > 1000:
        podcast_id = 1000
    if podcast_id < 1:
        podcast_id = 1
    episode_page = request.args.get('episode_page', default=1, type=int)
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    all_episodes = sorted(podcast.episodes, key=lambda ep: ep.date)
    paginated_episodes, next_episode_page, prev_episode_page, total_pages = (
        utilities.get_episodes_pagination(all_episodes, episode_page))
    categories = utilities.get_categories()['categories']
    reviews = podcast.reviews
    average_rating = utilities.calculate_average_rating(reviews)
    playlist = services.get_playlist(repository.repo_instance)
    episodes_in_playlist = utilities.get_episodes_in_playlist(paginated_episodes, playlist)
    return render_template(
        'description/podcastDescription.html',
        podcast=podcast,
        episodes=paginated_episodes,
        categories=categories,
        episode_page=episode_page,
        next_episode_page=next_episode_page,
        prev_episode_page=prev_episode_page,
        total_pages=total_pages,
        episodes_in_playlist=episodes_in_playlist,
        average_rating=average_rating,
        podcast_reviews=reviews,
        form=form
    )


@description_blueprint.route("/add_to_playlist", methods=["GET", "POST"])
@login_required
def add_to_playlist():
    episode_id = request.form.get("episode_id", type=int)
    episode = services.get_episode_by_id(repository.repo_instance, episode_id)
    try:
        services.add_to_playlist(repository.repo_instance, episode)
        flash(f'Episode "{episode.title}" added to playlist successfully!', "success")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("description_bp.show_description", podcast_id=episode.podcast.id))


@description_blueprint.route("/remove_from_playlist", methods=["GET", "POST"])
@login_required
def remove_from_playlist():
    episode_id = request.form.get("episode_id", type=int)
    episode = services.get_episode_by_id(repository.repo_instance, episode_id)
    try:
        services.remove_from_playlist(repository.repo_instance, episode)
        flash(f'Episode "{episode.title}" removed from playlist successfully!', "error")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for("description_bp.show_description", podcast_id=episode.podcast.id))


@description_blueprint.route('/add_all_to_playlist', methods=['POST'])
@login_required
def add_all_to_playlist():
    podcast_id = request.form.get('podcast_id', type=int)
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    all_episodes = podcast.episodes
    try:
        for episode in all_episodes:
            services.add_to_playlist(repository.repo_instance, episode)
        flash(f'All episodes in the podcast added to playlist successfully!', "success")
    except Exception as error:
        flash(str(error), "error")
    return redirect(url_for('description_bp.show_description', podcast_id=podcast_id))


@description_blueprint.route('/add_review', methods=['POST'])
@login_required
def add_review():
    form = ReviewForm()
    podcast_id = request.form.get('podcast_id', type=int)
    if form.validate_on_submit():
        podcast_id = form.podcast_id.data
        rating = form.rating.data
        description = form.description.data
        try:
            # Retrieve user and podcast
            username = utilities.get_username()
            user = services.get_user_by_username(repository.repo_instance, username)
            podcast = services.get_podcast_by_id(repository.repo_instance, int(podcast_id))
            # Add the review
            services.add_review(repository.repo_instance, podcast, user, rating, description)
            flash('Review added successfully!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            # Catch all other exceptions to avoid crashing the app
            flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('description_bp.show_description', podcast_id=podcast_id))

    # If form validation fails, render the form with errors
    flash('There was an error with your review submission.', 'error')
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    episode_page = request.args.get('episode_page', default=1, type=int)
    all_episodes = sorted(podcast.episodes, key=lambda ep: ep.date)
    paginated_episodes, next_episode_page, prev_episode_page, total_pages = (
        utilities.get_episodes_pagination(all_episodes, episode_page))
    categories = utilities.get_categories()['categories']
    reviews = podcast.reviews
    average_rating = utilities.calculate_average_rating(reviews)
    playlist = services.get_playlist(repository.repo_instance)
    episodes_in_playlist = utilities.get_episodes_in_playlist(paginated_episodes, playlist)
    return render_template(
        'description/podcastDescription.html',
        podcast=podcast,
        episodes=paginated_episodes,
        categories=categories,
        episode_page=episode_page,
        next_episode_page=next_episode_page,
        prev_episode_page=prev_episode_page,
        total_pages=total_pages,
        episodes_in_playlist=episodes_in_playlist,
        average_rating=average_rating,
        podcast_reviews=reviews,
        form=form
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    description = TextAreaField('description', [
        DataRequired(message='Comment is required.'),
        Length(min=2, message='Your comment is too short.'),
        ProfanityFree(message='Your comment must not contain profanity!')])
    rating = SelectField('rating', choices=[(i, str(i)) for i in range(5, 0, -1)], coerce=int,
                         validators=[DataRequired()])
    podcast_id = HiddenField('podcast_id')
    submit = SubmitField('Submit Review')
