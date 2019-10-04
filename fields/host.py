def append_host_from_context(url, context):
    if '://' not in url:
        return '%s://%s%s' % (
            'https' if context.is_secure() else 'http',
            context.get_host(),
            url
        )
    return url


def serialize_image_field(field, info):
    try:
        return info.context.build_absolute_uri(field.url)
    except ValueError:
        return None
