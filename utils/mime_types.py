expected_mime_types = (
        'text/plain',
        'application/x-javascript',
        'text/css',
        'application/json+protobuf',
        'application/javascript',
        'application/json',
        'text/javascript',
        'text/json',
        'text/html'
)

images_filename_suffix = ('.ico', '.gif', '.jpg', '.jpeg', '.pjp', '.pjpeg', '.jfif', '.png', '.svg',
                          '.webp', '.avif', '.apng',)

videos_filename_suffix = ('.mp4', '.mov', '.wmv', '.webm', '.avi', '.flv', '.mkv', '.mts',)

fonts_filename_suffix = ('.woff2', '.woff', '.ttf', '.otf',)

extensions = images_filename_suffix + videos_filename_suffix + fonts_filename_suffix
