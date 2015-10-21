# Tentative de conversion en markup réutilisable

Le format ressemble à ceci:

```
Gallica est passé à son [nouveau design].
http://gallica.bnf.fr/blog/09102015/mise-jour-du-nouveau-gallica

---
L'[ancien blog] est toujours en place. Heureusement. 
http://blog.bnf.fr/gallica/index.php/2015/10/01/le-blog-gallica-change-dadresse/
---
Discussions sur le [choix du nom] au Japon pour les couples mariés.
>“The problem is that there are people who want to choose to have separate surnames but can’t. In other words, they are being forced to abandon their maiden names,” Tanamura says. “A person’s name should be protected under moral rights because a person’s name expresses who they are.”
http://www.japantimes.co.jp/life/2015/10/17/lifestyle/whats-name-japan-debates-whether-allow-spouses-adopt-separate-surnames/
```

Il doit probablement être converti en une structure de données, peut-être namedtuple.

```python
from collections import namedtuple
Link = namedtuple('Link', 'link texte quote')
grenier = [
          Link('link1', 'texte1', ''),
          Link('link2', 'texte2', 'quote2'),
]
```
