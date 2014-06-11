Monster Under the Bed
---------------------

Monster Under the Bed (django-mub) is a static-files (css &amp; js) collector and minifier.

## Quickstart

<ol>

<li><strong>Install with pip (currently only available from github repository):</strong>
{% highlight bash %}
pip install git+https://github.com/Brant/django-noodles.git@master
{% endhighlight %}

<br/>
Or add it to your requirements.txt file:

{% highlight bash %}
# requirements.txt
git+https://github.com/Brant/django-noodles.git@master
{% endhighlight %}
<br/>
</li>

<li><strong>Add 'mub' to your INSTALLED_APPS setting:</strong>
{% highlight python %}
INSTALLED_APPS = (
    ...
    'mub',
    ...
)
{% endhighlight %}
<br />
</li>

<li><strong>Load the 'mub_tags' templatetags in your template:</strong>

{% highlight html %}
<!doctype html>
<html>{{ "{% load mub_tags " }}%}
...
{% endhighlight %}
<br/>
And use the 'add_static' tags provided by the mub_tags library:

{% highlight html %}
<head>
	...
	{{"{% add_static 'css'" }}%}
</head>
<body>
	...
	{{"{% add_static 'js'" }}%}
</body>
{% endhighlight %}
</li>

</ol>

To review configurable options, see the [settings documentation]({{ "/settings/" | prepend: site.baseurl }})
