---
title: Caching
layout: page
---

When moving your project to a production environment, you probably want to setup caching (e.g. memcache or redis)

Django-mub can take advantage of django's caching abstractions.

1. Set ```MUB_MINIFY = True``` in your settings (this is already done unless you have explicitly set it to False).
2. Add ```python manage.py mub_minify``` to your build process (django-mub's custom management command)
3. *(optional)* if your cache is unstable, add the ```mub_minify``` management command to some sort of cron job on your server.

Following those steps will store the names of your CSS and JS minified files in the cache, so that the server doesn't need to try to re-compile the files on each request.

This is a fairly important thing to configure, particularly for high-volume sites. The disk I/O is rough in a high-volume production environment.

If your cache should fail at some point though, django-mub will simply fall back to a state that doesn't require a caching layer. In other words, your static files won't break if your cache layer fails.
