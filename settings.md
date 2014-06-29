---
title: Settings
layout: page
---
There are a handful of configurable settings for django-mub.

For additional options and information when deploying to production, see the [caching documentation]({{ "/caching/" | prepend : site.baseurl }}).

## Ordering your CSS files

It's often important to be able to specifically order your CSS files. For example, you often want your media queries to come toward the end of a compiled sheet, while items such as css resets appear at the top.

**MUB_CSS_ORDER**: Defaults to ```((), ())```

*Example:*

{% highlight python %}
# settings.py
MUB_CSS_ORDER = (
    ('reset.css', 'base.css', 'main.css'), # top of sheet
    ('large-screens.css', 'print.css') # bottom of sheet
)
{% endhighlight %}

MUB_CSS_ORDER is a 2-tuple of tuples. The first set of items will appear at the top of the CSS sheet after it has been compiled and minified. The second set of items will appear at the bottom of that sheet. 

This allows you some fine-grained control over ordering your CSS (often important for specificity) when necessary without needing to specify the order of every individual sheet when it doesn't really matter.

## Manually choosing to compile/minify (or not)
You can choose whether or not to compile and minify your static files or if you'd prefer for the files to be listed individually.

**MUB_MINIFY**: Defaults to the oposite of your ```DEBUG``` setting

*Example:*
{% highlight python %}
# settings.py
MUB_MINIFY = True # this will force mub to always compile/minify
{% endhighlight %}

Presumably you develop with ```DEBUG = True```, changing it to ```True``` when deployed to production. The default setting will then leave your CSS and JS as individual files during development and compile/minify them in production.

Regardless of whether you use minification or not, the order of the files will be consistent.

