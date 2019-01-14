# instasteem

A CLI tool and Python library to sync your instagram posts with your STEEM profile

# Installation

```
$ pip install instasteem
```

# Usage

- Parse the post and get the markdown output

```
instasteem <instagram_post_url> > post.md
```
***

- Parse the post and post to the STEEM blockchain

```
$ INSTASTEEM_POSTING_KEY=ASDASD instasteem <instagram_post_url> --steem-username 
```

# Including metadata

`--include-metadata 1` attaches an informational table to the post.
If you don't want that in the post body, then don't send the argument.


# Tags


`--tags'` parameter sets the post's tag on STEEM blockchain. Currently, the parser doesn't parse any tag from instagram. If you don't pass that parameter, `photography` will be used as a tag.

# Using instasteem as a Python library

`instasteem` can be also used to parse instagram posts. 

```
from instasteem.parser import InstagramPostParser


p = InstagramPostParser("https://www.instagram.com/p/BsfudqQgGlw/")
images = p.extract_images()
metadata = p.extract_metadata()

# ...
```