def append_host_from_context(url, context):
    return '%s://%s%s' % (
        'https' if context.is_secure() else 'http',
        context.get_host(),
        url
    )
