from django.test import TestCase, Client, RequestFactory
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Audio, AudioAdd, User
import os
from django.conf import settings


# Create your tests here.
class UserFactory(factory.django.DjangoModelFactory):
    """Test user."""

    class Meta:
        """Meta class."""

        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')


class AudioFactory(factory.django.DjangoModelFactory):
    """Test audio new."""

    class Meta:
        """Meta class."""

        model = Audio

    path = SimpleUploadedFile(
        name='test_clip.mp3',
        content=open(
            os.path.join(settings.BASE_DIR, 'noise/static/hellew_brandon.mp3'), 'rb'
        ).read(),
        content_type='audio/mpeg'
    )

    audio_file = SimpleUploadedFile(
        name='add_clip.mp3',
        content=open(
            os.path.join(settings.BASE_DIR, 'noise/static/test_clip.mp3'), 'rb'
        ).read(),
        content_type='audio/mpeg'
    )

    topic = factory.Faker('word')
    date_published = factory.Faker('date')
    published = 'PUB'


class AudioAddFactory(factory.django.DjangoModelFactory):
    """Test audio add."""

    class Meta:
        """Meta class."""

        model = AudioAdd

    audio_file = SimpleUploadedFile(
        name='add_clip.mp3',
        content=open(
            os.path.join(settings.BASE_DIR, 'noise/static/test_clip.mp3'), 'rb'
        ).read(),
        content_type='audio/mpeg'
    )


class AudioUnitTests(TestCase):
    """Unit test audio."""

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)

        cls.request = RequestFactory()
        creator = UserFactory(username='test', email='brandon@brandon.brandon')
        creator.set_password('test1234')
        creator.save()
        cls.test_user = creator

        audio = AudioFactory.create(creator=creator)
        audio.save()

        cls.request = RequestFactory()

        audioAdd = AudioAddFactory.create(user=creator)
        audioAdd = AudioAddFactory.create(pk_master=audio)
        audioAdd.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        super(TestCase, cls)

    def test_one_audio_clip(self):
        clip = Audio.objects.first()
        self.assertIsNotNone(clip)

    def test_clip_has_topic(self):
        clip = Audio.objects.first()
        self.assertIsInstance(clip.topic, str)

    def test_has_creator(self):
        clip = Audio.objects.first()
        self.assertIsInstance(clip.creator, object)

    def test_date_published(self):
        clip = Audio.objects.first()
        self.assertIsInstance(clip.date_published, object)

    def test_string_of_clip(self):
        clip = Audio.objects.first()
        self.assertIsInstance(str(clip), str)

    def test_new_clip_view(self):
        from noise_audio.views import NewStoryForm
        request = self.request.get('')
        request.user = self.test_user
        new_story_view = NewStoryForm.as_view()
        response = new_story_view(request)
        self.assertEqual(response.status_code, 200)

    def test_add_clip_view(self):
        from noise_audio.views import ContinueStoryForm
        request = self.request.get('')
        request.user = self.test_user
        continue_story_view = ContinueStoryForm.as_view()
        response = continue_story_view(request, clip_id=1)
        self.assertEqual(response.status_code, 200)

    def test_link_view_has_content(self):
        from noise_audio.views import LinkView
        request = self.request.get('')
        request.user = self.test_user
        link_view = LinkView.as_view()
        response = link_view(request)
        self.assertEqual(response.status_code, 200)
