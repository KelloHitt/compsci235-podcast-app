from better_profanity import profanity
from flask import Blueprint, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.csrf import session
from wtforms.validators import ValidationError, DataRequired, Length

import podcast.adapters.repository as repository
import podcast.description.services as services
import podcast.utilities.utilities as utilities
from podcast.authentication.authentication import login_required


description_blueprint = Blueprint('description_bp', __name__)


@description_blueprint.route('/description', methods=['GET'])
def show_description():
    podcast_id = request.args.get('podcast_id', default=1, type=int)

    # Ensure podcast_id is within valid range
    if podcast_id > 1000:
        podcast_id = 1000
    if podcast_id < 1:
        podcast_id = 1

    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    episodes = sorted(podcast.episodes, key=lambda episode: episode.date)
    categories = utilities.get_categories()['categories']

    return render_template('podcastDescription.html', podcast=podcast, episodes=episodes, categories=categories)

@description_blueprint.route('/description', methods=['GET', 'POST'])
@login_required
def review_podcast():
    user_name = session['user_name']

    form = ReviewForm()

    if form.validate_on_submit():
        podcast_id = int(form.podcast_id.data)
        services.add_review(podcast_id, form.review.data, user_name, repository.repo_instance)
        podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
        if request.method == "GET":
            podcast_id = int(request.args.get('podcast'))
            form.podcast_id.data = podcast_id
        else:
            podcast_id = int(form.podcast_id.data)

        podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
        return render_template(
            'podcastDescription.html',
            title = 'Edit podcast',
            podcast=podcast,
            form=form,
            handler_url=url_for('description_bp.review_podcast')
        )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message =  message

    def call(self, form , field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)

class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [DataRequired(),
                           Length(min=5, message='Your review is too short!'),
                           ProfanityFree(message='Your review must not contain profanity!')])
    podcast_id = HiddenField("Podcast ID")
    post = SubmitField("Post")



