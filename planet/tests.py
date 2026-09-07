from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from planet.models import Post1, Planet

# 1. TEST CÁC TRANG CƠ BẢN
class StaticPagesTests(SimpleTestCase):
    def test_homepage_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


# 2. TEST MODEL
class ModelTests(TestCase):
    def test_planet_str(self):
        planet = Planet.objects.create(firstname="Nguyen", lastname="An", phone=123456)
        self.assertEqual(str(planet), "Nguyen An")

    def test_post1_creation_and_str(self):
        post = Post1.objects.create(title="Post Test Title", body="Post Content")
        self.assertEqual(str(post), "Post Test Title")
        self.assertEqual(post.body, "Post Content")


# 3. TEST XEM BÀI VIẾT VÀ BẮT LỖI 404
class PostViewTests(TestCase):
    def setUp(self):
        self.post = Post1.objects.create(
            title="Kỵ sĩ bóng đêm Test",
            body="Review phim chi tiết..."
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kỵ sĩ bóng đêm Test")
        self.assertTemplateUsed(response, 'post_list.html')

    def test_post_detail_view_success(self):
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Review phim chi tiết...")
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_detail_not_found(self):
        response = self.client.get(reverse('post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


# 4. TEST XÁC THỰC
class AuthAndSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='quangduy', 
            password='Password123'
        )

    def test_user_login_success(self):
        login_success = self.client.login(username='quangduy123', password='Password123')
        self.assertTrue(login_success)

    def test_user_login_failed(self):
        login_failed = self.client.login(username='quangduy', password='WrongPassword')
        self.assertFalse(login_failed)


# 5. TEST TẠO BÀI VIẾT CÓ FILE ĐÍNH KÈM
class PostUploadTests(TestCase):
    def test_post_with_dummy_image_and_audio(self):
        dummy_image = SimpleUploadedFile(
            name='test_img.gif',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/gif'
        )
        dummy_audio = SimpleUploadedFile(
            name='test_song.mp3',
            content=b'fake audio content',
            content_type='audio/mpeg'
        )

        post = Post1.objects.create(
            title="Bài test có file",
            body="Nội dung test file",
            image=dummy_image,
            audio=dummy_audio
        )

        # Kiểm tra model đã nhận và lưu tên file
        self.assertTrue(bool(post.image.name))
        self.assertTrue(bool(post.audio.name))