# biblehub
A python module (Formerly BibleHubScrapper) that retrieve a single verse and the information on it from biblehub.com.
Also a simple commandline application.

## Installation
```pip3 install biblehub```

## Commandline
To retrieve all the currently available information on a reference, use the '-a' tag:

`biblehub -a [Reference]`

To only retrieve specific information, pass in the corresponding tag:
```
biblehub -c [Reference] # Also retrieves the cross-references
biblehub -t [Reference] # Also retrieves the lexicon
```
As with most cli tools, arguments can be stacked with one hyphen, such as:
```
biblehub -cl [Reference] # Retrieves the cross-references and lexicon in addition to the passage
```
To retrieve all the versions for that reference, use the `--versions` tag
```
biblehub --versions Genesis 2:4
```
## Script Usage
You can import the query and get_versions methods to use in scripts.
```
from biblehub import query, get_versions

biblehub_query = query('Genesis 1:1')
all_versions = get_versions('Genesis 1:1')
print(biblehub_query.text) # In the beginning...
print(all_versions[0].passage)
```
By default, it will query all possible fields.
You can choose not to query certain fields by indicating in the parameters
for example:
` query('Genesis 1:1', get_lexicons=False) `

## Useful fields
```
print(biblehub_query.passage) # Genesis 1:1
print(biblehub_query.version) # NIV (default)
print(biblehub_query.lexicons) # Text, Hebrew words, translit, strong, and English defintions
print(biblehub_query.crfs) # Cross References
print(biblehub_query.tos) # Treasury of Scripture
print(biblehub_query.info) # Prints all the info queried on the verse. Also the same as the __str__
```
there are also `biblehub_query.format_[field]` method that returns the specified field in an easy to read way.

## Contributing
If you feel like improving the codebase, adding a feature, or checking my grammar, feel free!
Checkout the issues I post for tasks you can help with, reference specific issues when making a PR.
Make sure to send a pull request against the development branch.
