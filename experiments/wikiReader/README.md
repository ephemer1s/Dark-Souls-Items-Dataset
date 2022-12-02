## current findings on extracting the page:


this `<title>` line exclusive indicates the item name and the original game. But the name appears at many places.
```html
<title>Crystal Sage's Rapier | Dark Souls 3 Wiki</title>
```


this `<blockquote>` block exclusively indicate the description, which is our output
```html
<blockquote> 
 <p>Thrusting Sword with tiny crystals scattered across its blade, used by the Crystal Sages for self-defence.<br><br>The crystals boost the magic damage inflicted by the sword, and the item discovery of its wielder, fruit of the lifetime of research conducted by the sages.<br><br>Skill: Stance. <br>From stance, use normal attack to back step and execute a surprise attack, or a strong attack for consecutive thrusting.</p> 
</blockquote> 
```

And this contains most of the feature we can make use of.
```html
<div class="breadcrumbs pull-left" ><div id="breadcrumbs-container">
<a href="https://darksouls3.wiki.fextralife.com/Equipment+&+Magic">Equipment & Magic</a>&nbsp;/&nbsp;<a href="https://darksouls3.wiki.fextralife.com/Weapons">Weapons</a>&nbsp;/&nbsp;<a href="https://darksouls3.wiki.fextralife.com/Thrusting+Swords">Thrusting Swords</a>
<div id="breadcrumbs-bcontainer" style="display:none;">&nbsp;&nbsp;<a id="btnCreateBreadcrumb" title="Add Breadcrumb" href="#">+</a></div></div></div>

```

the other features

## current problems and thoughts

how to effectively parse the page and traverse through the wiki

we have these options:

1. use web scrappers
2. gather all possible item names and use get request to get the page
3. open page and click view source and click save as


there are some pages (not too much) does not meet with this format.


Check this out https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string

## how to run the experiment
```bash
python main.py
```


## how to run HTMLReader
```bash
python3 HTMLReader.py <input directory> <output file path>
```

## how to run Combiner
```bash
python3 Combiner.py <input directory> <output file path>
```
