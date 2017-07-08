from django.apps import Appconfig

class ImagesConfig(AppConfig):
    name = 'images'
    verbose_name = 'Image bookmarks'
    
    def ready(self):
        # import signal handlers
        import images.signals
        