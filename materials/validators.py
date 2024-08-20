import re
from rest_framework.serializers import ValidationError


def validate_links(value):
    """Проверка, что строка содержит ссылки только на youtube"""

    links = [x[0] for x in re.findall(r"((www\.|http://|https://)(www\.)*.*?(?=(www\.|http://|https://|$)))", value)]

    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    is_only_youtube_links = all(bool(re.match(youtube_regex, link)) for link in links)
    if not is_only_youtube_links:
        raise ValidationError("Запрещены ссылки на сторонние сайты")
