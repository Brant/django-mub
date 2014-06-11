Monster Under the Bed
---------------------

Monster Under the Bed (django-mub) is a static-files (css &amp; js) collector and minifier.

## Quickstart

<ol>

<li><strong>Install with pip (currently only available from github repository):</strong>
```
pip install git+https://github.com/Brant/django-noodles.git@master
```

<br/>
Or add it to your requirements.txt file:

```
# requirements.txt
git+https://github.com/Brant/django-noodles.git@master
```
<br/>
</li>

<li><strong>Add 'mub' to your INSTALLED_APPS setting:</strong>
```python
INSTALLED_APPS = (
    ...
    'mub',
    ...
)
```
<br />
</li>

<li><strong>Load the 'mub_tags' templatetags in your template:</strong>

```html
<!doctype html>
<html>{{ "{% load mub_tags " }}%}
...
```
<br/>
And use the 'add_static' tags provided by the mub_tags library:

```html
<head>
	...
	{{"{% add_static 'css'" }}%}
</head>
<body>
	...
	{{"{% add_static 'js'" }}%}
</body>
```
</li>

</ol>

To review configurable options, see the [settings documentation]({{ "/settings/" | prepend: site.baseurl }})
